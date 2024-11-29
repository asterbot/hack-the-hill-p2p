"""
Testing the P2P Client functions
"""
import socket
import unittest

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
            self.assertTrue(isinstance(test_client.__discovery_socket__, socket.socket))
            self.assertTrue(isinstance(test_client.__chat_socket__, socket.socket))

    def test_start_runs_threads_in_correct_order(self):
        """
        Start function should throw no exceptions
        """

        with P2PClient() as test_client:
            test_client.start()
