"""
TODO
"""

import socket

from config import GLOBAL_IP, PORT


class SenderSocket:
    """
    TODO
    """

    def __init__(self):
        self.__sender_socket__ = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def close(self):
        """
        TODO
        """

        self.__sender_socket__.close()

    def send(self, data: str, ip=GLOBAL_IP):
        """
        TODO
        """

        self.__sender_socket__.sendto(data.encode(), (ip, PORT))
