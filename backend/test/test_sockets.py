"""
Testing that Sender and Receiver sockets work
"""
import threading
import unittest

from code.receiver_socket import ReceiverSocket
from code.sender_socket import SenderSocket


class TestSockets(unittest.TestCase):
    """
        Testing sockets
    """
    
    def setUp(self):
        self.data_received: str = ""

        self.receiver = ReceiverSocket()
        self.thread = self.background_process(self.receiver)

        self.sender = SenderSocket()
    
    def tearDown(self):
        self.thread.join()
        self.sender.close()
        self.receiver.close()

    def start_receiving(self, receiver: ReceiverSocket):
        data: bytes

        while True:
            data, addr = receiver.receive()

            print(data.decode())

    def background_process(self, receiver: ReceiverSocket):
        receive_thread = threading.Thread(target=self.start_receiving,
                                          kwargs={'receiver': receiver},
                                          daemon=True)
        receive_thread.start()

        return receive_thread

    def test_instance_of_sending_and_receiving(self):
        """
        Confirming that the data flow is alright
        """

        test_data = "test_instance_of_sending_and_receiving"
        self.sender.send(test_data)
        self.assertEqual(self.data_received, test_data)