"""
TODO
"""

import socket

from config import GLOBAL_IP, PORT, MAX_DATA_SIZE


class ReceiverSocket:
    """
    TODO
    """
    
    def __init__(self):
        self.__receiver_socket__ = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__receiver_socket__.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__receiver_socket__.bind((GLOBAL_IP, PORT))

    def close(self):
        self.__receiver_socket__.close()
        
    def receive(self, size=MAX_DATA_SIZE) -> tuple[bytes, tuple[str, int]]:
        return self.__receiver_socket__.recvfrom(size)