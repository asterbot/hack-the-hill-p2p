"""
Testing that Sender and Receiver sockets work
"""

import threading
import unittest
from time import sleep

from code.receiver_socket import ReceiverSocket
from code.sender_socket import SenderSocket


class TestSockets(unittest.TestCase):
    """
    Testing sockets
    """

    def setUp(self):
        self.data_received: str = ""
        self.receiver = ReceiverSocket()
        self.sender = SenderSocket()
        self.background_process()

    def tearDown(self):
        self.receive_thread.join()
        self.sender.close()
        self.receiver.close()

    def start_receiving(self):
        """
        TODO
        """

        while True:
            data, _ = self.receiver.receive()

            if data.decode() != "":
                self.data_received = data.decode()
                break

    def background_process(self):
        """
        TODO
        """

        self.receive_thread = threading.Thread(target=self.start_receiving, daemon=True)
        self.receive_thread.start()

    def test_instance_of_sending_and_receiving(self):
        """
        Confirming that the data flow is alright
        """

        test_data = "test_instance_of_sending_and_receiving"
        self.sender.send(test_data)
        sleep(0.01)
        self.assertEqual(self.data_received, test_data)
