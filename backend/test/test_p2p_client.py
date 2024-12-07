"""
Testing the P2P Client functions
"""
import socket
import unittest

from code.client_message import ClientMessage, MessageType, MessageError
from code.p2p_client import P2PClient


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
            self.assertTrue(isinstance(test_client.__receiver_socket__, socket.socket))
            self.assertTrue(isinstance(test_client.__sender_socket__, socket.socket))

    def test_start_throws_no_exception(self):
        """
        Start function should throw no exceptions
        """

        with P2PClient() as test_client:
            test_client.start()

    def test_request_file_sends_correct_client_message(self):
        """
        We should be requesting for the correct file
        """
        
        test_file_id = 1
        
        with P2PClient() as test_client:
            test_client_message = ClientMessage()
            test_client_message.type = MessageType.REQUEST_FILE
            test_client_message.user_id = test_client.__user_id__
            test_client_message.file_id = test_file_id
            test_client_message.error = MessageError.NO_ERROR