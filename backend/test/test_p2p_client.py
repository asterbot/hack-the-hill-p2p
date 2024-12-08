"""
Testing the P2P Client functions
"""
import os
import unittest
from pathlib import Path

from code.client_message import ClientMessage
from code.file_tokenizer import hash_file_blocks
from code.p2p_client import P2PClient
from code.receiver_socket import ReceiverSocket
from code.sender_socket import SenderSocket
from code.utils import custom_encoding
from config import GLOBAL_IP, SOURCES_FOLDER, HASH_EXTENSION, UPLOADS_FOLDER


class TestP2PClient(unittest.TestCase):
    """
    This is the most crucial class to test in this entire project. Make sure to include all the
    edge cases even if they don't contribute to coverage.
    """

    def test_init(self):
        """
        Just making sure that init function sets up correct types.
        """

        with P2PClient() as test_client:
            # Asserting types
            self.assertTrue(isinstance(test_client.__user_id__, str))
            self.assertTrue(isinstance(test_client.__friends__, dict))
            self.assertTrue(isinstance(test_client.__receiver_socket__, ReceiverSocket))
            self.assertTrue(isinstance(test_client.__sender_socket__, SenderSocket))

    def test_start_with_no_friends_throws_no_exception(self):
        """
        Start with no friends function should throw no exceptions
        """

        with P2PClient() as test_client:
            test_client.start()

    def test_start_with_friends_throws_no_exception(self):
        """
        Start with a friend function should throw no exceptions
        """

        with P2PClient() as test_client:
            test_client.__friends__ = {'friend': GLOBAL_IP}
            test_client.start()

    def test_start_and_request_with_no_friends_throws_no_exception(self):
        """
        We should be requesting for the correct file, but with no friends
        """

        test_file_name = "test_start_and_request_with_no_friends_throws_no_exception"
        test_file_id = custom_encoding(test_file_name)

        with P2PClient() as test_client:
            test_client.start()
            test_client.request_file(test_file_id)

    def test_start_and_request_with_friends_throws_no_exception(self):
        """
        We should be requesting for the correct file, with friend
        """

        test_file_name = "test_start_and_request_with_no_friends_throws_no_exception"
        test_file_id = custom_encoding(test_file_name)

        with P2PClient() as test_client:
            test_client.start()
            test_client.__friends__ = {'friend': GLOBAL_IP}
            test_client.request_file(test_file_id)

    def test_start_and_response_when_file_does_not_exist_throws_no_exception(self):
        """
            We should be responding correctly to a file, requested file does not exist.
        """

        test_file_name = "test_start_and_response_when_file_does_not_exist_throws_no_exception"
        test_file_id = custom_encoding(test_file_name)

        with P2PClient() as test_client:
            test_friend_message = ClientMessage()

            test_friend_message.file_name = test_file_name
            test_friend_message.user_id = "friend"
            test_friend_message.file_id = test_file_id

            test_client.__response_file__(test_friend_message)

    def test_start_and_response_when_file_does_exist_throws_no_exception(self):
        """
            We should be responding correctly to a file, requested file exist.
        """

        test_file_name = "test_start_and_response_when_file_does_exist_throws_no_exception.txt"
        test_file_id: str

        test_file = os.path.join(UPLOADS_FOLDER, test_file_name)
        test_hackthehill_file = os.path.join(SOURCES_FOLDER,
                                             Path(test_file_name).stem + HASH_EXTENSION)

        with open(test_file, 'x') as f:
            f.write(test_file_name)

        hash_file_blocks(test_file)

        with open(test_hackthehill_file, 'r') as f:
            test_file_id = custom_encoding(f.read())

        with P2PClient() as test_client:
            test_friend_message = ClientMessage()

            test_friend_message.file_name = test_file_name
            test_friend_message.user_id = "friend"
            test_friend_message.file_id = test_file_id

            test_client.__friends__["friend"] = GLOBAL_IP

            test_client.__response_file__(test_friend_message)

        os.remove(test_file)
        os.remove(test_hackthehill_file)
