"""
Testing the P2P Client functions
"""

import unittest

from code.client_message import ClientMessage, MessageType, MessageError
from code.p2p_client import P2PClient
from code.receiver_socket import ReceiverSocket
from code.sender_socket import SenderSocket
from config import GLOBAL_IP


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

        test_file_id = "test_start_and_request_with_no_friends_throws_no_exception"

        with P2PClient() as test_client:
            test_client.start()
            test_client.request_file(test_file_id)

    def test_start_and_request_with_friends_throws_no_exception(self):
        """
        We should be requesting for the correct file, with friend
        """

        test_file_id = "test_start_and_request_with_no_friends_throws_no_exception"

        with P2PClient() as test_client:
            test_client.start()
            test_client.__friends__ = {'friend': GLOBAL_IP}
            test_client.request_file(test_file_id)
