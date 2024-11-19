"""
P2P Connection and TCP File Sharing
"""

import os
import socket
import threading
import time
import uuid
from pathlib import Path

from code.client_message import ClientMessage, MessageType
from code.utils import get_filename_by_file_id, save_file
from config import DISCOVERY_PORT, CHAT_PORT, MAX_UDP_PACKET, DISCOVERY_ADDRESS, HASH_EXTENSION, \
    SOURCES_FOLDER


class P2PClient:
    """
    P2P client is the main application that creates P2P connection between two users, and uses TCP
    for file sharing. Note that this class uses threads and async functions extensively.

    For getting a new file across, we have the following transitions.

    1. Client requests their friends for the .hackthehill file.
    2. Client's friends respond with the .hackthehill file for that particular file id
    3. Client receives the .hackthehill file, saves it and uses to get the original file back
    """

    def __init__(self):
        self.__user_id__: str = uuid.uuid4().__str__()
        self.__friends__: dict[str, any] = {}

        self.__discovery_socket__ = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__discovery_socket__.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.__discovery_socket__.bind(('', DISCOVERY_PORT))

        self.__chat_socket__ = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__chat_socket__.bind(('', CHAT_PORT))
        self.__chat_socket__.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, MAX_UDP_PACKET)
        self.__chat_socket__.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, MAX_UDP_PACKET)

    def start(self) -> None:
        """
        Run these processes in the background constantly (daemon) on different threads.

        1. We constantly search for friends
        2. We constantly keep listening to messages our friends have for us
        3. We constantly keep telling everyone on our network that we are open to being friends.
        """

        threading.Thread(target=self.__discover_friends__, daemon=True).start()
        threading.Thread(target=self.__listen_for_messages__, daemon=True).start()
        threading.Thread(target=self.__announce_presence__, daemon=True).start()

    def request_file(self, file_id: str) -> None:
        """
        Send everyone on your network list a request for a file that has this particular
        file id. Note that since we get the file id from the sender directly, only they should
        have a file with the same file id.

        :param file_id: String. File id of the file that you want to request from your friends.
        """

        client_message = ClientMessage()
        client_message.type = MessageType.REQUEST_FILE
        client_message.user_id = self.__user_id__
        client_message.file_id = file_id
        response = client_message.to_json()

        for friend in self.__friends__.values():
            self.__chat_socket__.sendto(response.encode(), (friend, CHAT_PORT))

    def __discover_friends__(self) -> None:
        """
        Continuously search for people in your network, and if you find them, add their ip to your
        dictionary.
        """

        while True:
            data, addr = self.__discovery_socket__.recvfrom(MAX_UDP_PACKET)
            client_message = ClientMessage()
            client_message.load(data)

            if client_message.is_announce() and client_message.user_id != self.__user_id__:
                self.__friends__[client_message.user_id] = addr[0]

    def __announce_presence__(self) -> None:
        """
        Every 2 seconds we announce our presence to the network of people in our network.
        """

        client_message = ClientMessage()
        client_message.type = MessageType.ANNOUNCE
        client_message.user_id = self.__user_id__
        response = client_message.to_json()

        while True:
            self.__discovery_socket__.sendto(response.encode(), (DISCOVERY_ADDRESS, DISCOVERY_PORT))
            time.sleep(2)

    def __response_file__(self, friend_message: ClientMessage) -> None:
        """
        Someone has requested for a file id that you shared; and hence, you should send back a
        response containing the .hackthehill file so that they can create the base file from 
        scratch.

        :param friend_message: ClientMessage. Contains your friend's request for a .hackthehill file
        """

        client_message = ClientMessage()
        client_message.type = MessageType.RESPONSE_FILE
        client_message.user_id = self.__user_id__
        client_message.file_id = friend_message.file_id

        files = get_filename_by_file_id(client_message.file_id)

        if files is None:
            print("No such file: " + client_message.file_id)
            return

        file_name = files[0]
        hackthehill_file = os.path.join(SOURCES_FOLDER, Path(file_name).stem + HASH_EXTENSION)

        with open(hackthehill_file, "r", encoding='utf-8') as f:
            client_message.file_name = file_name
            client_message.content = f.read()

            response = client_message.to_json()
            friend_ip = self.__friends__[friend_message.user_id]
            self.__chat_socket__.sendto(response.encode(), (friend_ip, CHAT_PORT))

    def __listen_for_messages__(self):
        """
        Listen for new messages from your friends.

        If they request for a file, you must respond to your friends.

        If they respond regarding a file, you must save the data sent.
        """

        while True:
            data, _ = self.__chat_socket__.recvfrom(MAX_UDP_PACKET)
            friend_message = ClientMessage()
            friend_message.load(data)

            print(friend_message)

            if friend_message.user_id in self.__friends__:
                if friend_message.is_request_file():
                    self.__response_file__(friend_message)
                elif friend_message.is_response_file():
                    save_file(friend_message)
                else:
                    print("Invalid message type")
            else:
                print("User id " + friend_message.user_id + " is not in the peers")
