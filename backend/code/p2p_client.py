"""
TODO
"""

import socket
import threading
import json
import time
import uuid
import os

from pathlib import Path

from code.utils import get_filename_by_file_id
from code.file_tokenizer import get_block_content
from config import DISCOVERY_PORT, CHAT_PORT, MAX_UDP_PACKET, DISCOVERY_ADDRESS, UPLOADS_FOLDER, \
    HASH_EXTENSION, SOURCES_FOLDER


class P2PClient:
    """
    TODO
    """

    def __init__(self):
        self.user_id = uuid.uuid1().__str__()
        self.peers = {}
        self.discovery_socket = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM)
        self.discovery_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.discovery_socket.bind(('', DISCOVERY_PORT))
        self.chat_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.chat_socket.bind(('', CHAT_PORT))

        self.chat_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_RCVBUF, MAX_UDP_PACKET)
        self.chat_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_SNDBUF, MAX_UDP_PACKET)

    def start(self):
        """
        TODO
        """

        threading.Thread(target=self.discover_peers, daemon=True).start()
        threading.Thread(target=self.listen_for_messages, daemon=True).start()
        threading.Thread(target=self.announce_presence, daemon=True).start()

    def discover_peers(self):
        """
        TODO
        """

        while True:
            data, addr = self.discovery_socket.recvfrom(MAX_UDP_PACKET)
            message = json.loads(data.decode())
            if message['type'] == 'announce' and message['user_id'] != self.user_id:
                self.peers[message['user_id']] = addr[0]

    def announce_presence(self):
        """
        TODO
        """

        while True:
            response = json.dumps({
                'type': 'announce',
                'user_id': self.user_id,
            })
            self.discovery_socket.sendto(
                response.encode(), (DISCOVERY_ADDRESS, DISCOVERY_PORT))
            time.sleep(2)

    def request_file_fingerprint(self, file_id):
        """
        TODO
        """

        for ip in self.peers.values():
            response = json.dumps({
                'user_id': self.user_id,
                'type': 'request_file_fingerprint',
                'file_id': file_id
            })
            self.chat_socket.sendto(response.encode(), (ip, CHAT_PORT))

    def request_block(self, file_id, block_index):
        """
        TODO
        """

        for ip in self.peers.values():
            message = json.dumps({
                'user_id': self.user_id,
                'type': 'request_block',
                'file_id': file_id,
                'block_index': block_index,
            })
            self.chat_socket.sendto(message.encode(), (ip, CHAT_PORT))

    def response_file_fingerprint(self, message):
        """
        TODO
        """

        file_id = message["file_id"]

        try:
            caller_ip = self.peers[message["user_id"]]
            files = get_filename_by_file_id(file_id)

            if files is None:
                print("No such file: " + file_id)
                return

            file_name = files[0]
            hackthehill_file = os.path.join(SOURCES_FOLDER, Path(file_name).stem + HASH_EXTENSION)
            with open(hackthehill_file, "r", encoding='utf-8') as f:
                response = json.dumps({
                    'file_name': file_name,
                    'user_id': self.user_id,
                    'type': 'response_file_fingerprint',
                    'content': f.read(),
                    'file_id': file_id
                })
                self.chat_socket.sendto(
                    response.encode(), (caller_ip, CHAT_PORT))
        except Exception as e:
            print(e)

    def response_block(self, message):
        """
        TODO
        """

        file_id = message["file_id"]
        block_index = message["block_index"]
        files = get_filename_by_file_id(file_id)

        if files is None:
            print("File not found: " + file_id)
            return

        target_file_name = files[0]

        block_data = get_block_content(os.path.join(UPLOADS_FOLDER, target_file_name), block_index)

        response = json.dumps({
            'file_name': target_file_name,
            'user_id': self.user_id,
            'type': 'response_block',
            'file_id': file_id,
            'block_index': block_index,
            'block_data': str(block_data, 'utf-8')
        })

        caller_ip = self.peers[message["user_id"]]

        self.chat_socket.sendto(response.encode(), (caller_ip, CHAT_PORT))

    def save_fingerprint_file(self, message):
        """
        TODO
        """

        hackthehill_file = os.path.join(SOURCES_FOLDER,
                                        Path(message['file_name']).stem + HASH_EXTENSION)
        with open(hackthehill_file, 'w', encoding="utf-8") as f:
            f.write(message['content'])

    def save_block(self, message):
        """
        TODO
        """

        tmp_file_path = os.path.join(UPLOADS_FOLDER, Path(message['file_name']).stem + '.tmp')
        with open(tmp_file_path, 'w+', encoding="utf-8") as f:
            file_content = f.read()
            if len(file_content) > 0:
                content = json.loads(file_content)
                if message['block_index'] not in content:
                    content[message['block_index']] = message['block_data']
                    f.seek(0)
                    f.write(json.dumps(content))
                    f.truncate()
            else:
                d = {message['block_index']: message['block_data']}
                f.write(json.dumps(d))

    def get_all_blocks(self, message):
        """
        TODO
        """

        file_id = message['file_id']
        hackthehill_file = os.path.join(SOURCES_FOLDER,
                                        Path(message['file_name']).stem + HASH_EXTENSION)
        with open(hackthehill_file, 'r', encoding="utf-8") as f:
            d = json.loads(f.read())
            for block_index in range(int(d['header']['number_of_blocks'])):
                self.request_block(file_id, block_index)

    def listen_for_messages(self):
        """
        TODO
        """

        while True:
            data, _ = self.chat_socket.recvfrom(MAX_UDP_PACKET)
            message = json.loads(data.decode())
            print(message)

            user_id = message["user_id"]
            if user_id in self.peers:
                if message["type"] == "request_file_fingerprint":
                    self.response_file_fingerprint(message)
                elif message["type"] == "request_block":
                    self.response_block(message)
                elif message["type"] == "response_file_fingerprint":
                    self.save_fingerprint_file(message)
                    self.get_all_blocks(message)
                elif message["type"] == "response_block":
                    self.save_block(message)
                    self.tmp_to_file(os.path.join(
                        'uploads', Path(message['file_name']).stem + '.tmp'))
                else:
                    print("Invalid message type: " + message["type"])
            else:
                print("User id " + user_id + " is not in the peers")

    def tmp_to_file(self, tmp_file_path):
        """
        TODO
        """
        with open(tmp_file_path, 'r', encoding="utf-8") as f:
            content = json.loads(f.read())

        file_path = os.path.join(SOURCES_FOLDER, Path(tmp_file_path).stem + HASH_EXTENSION)

        with open(file_path, 'r', encoding="utf-8") as f:
            file_with_extension = json.loads(f.read())['header']['file_name']

        # print("CONTENT:", content)
        s = content.values().join()

        with open(os.path.join('uploads', file_with_extension), 'w+', encoding="utf-8") as f:
            f.write(s)

        os.remove(tmp_file_path)
