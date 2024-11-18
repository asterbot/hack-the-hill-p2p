"""
TODO
"""

import json
from enum import Enum
from typing import Optional


class MessageType(Enum):
    """
    TODO
    """

    ANNOUNCE = 0
    REQUEST_FILE = 1
    RESPONSE_FILE = 3


class ClientMessage:
    """
    TODO
    """

    def __init__(self):
        self.type: Optional[MessageType] = None
        self.user_id: Optional[str] = None
        self.file_id: Optional[str] = None
        self.file_name: Optional[str] = None
        self.content: Optional[str] = None

    def load(self, data_bytes: bytes):
        """
        TODO
        """

        json_message = json.loads(data_bytes.decode())
        self.type = json_message['type']
        self.user_id = json_message['user_id']

        if self.type == MessageType.REQUEST_FILE:
            self.file_id = json_message['file_id']

        if self.type == MessageType.RESPONSE_FILE:
            self.file_id = json_message['file_id']
            self.file_name = json_message['file_name']
            self.content = json_message['content']

    def to_json(self) -> str:
        """
        TODO
        """

        information = {}

        if self.type == MessageType.ANNOUNCE:
            information = {
                'type': self.type,
                'user_id': self.user_id
            }
        elif self.type == MessageType.REQUEST_FILE:
            information = {
                'type': self.type,
                'user_id': self.user_id,
                'file_id': self.file_id
            }
        elif self.type == MessageType.RESPONSE_FILE:
            information = {
                'type': self.type,
                'user_id': self.user_id,
                'file_id': self.file_id,
                'file_name': self.file_name,
                'content': self.content
            }

        return json.dumps(information)

    def is_announce(self) -> bool:
        """
        TODO
        """

        return self.type == MessageType.ANNOUNCE

    def is_request_file(self) -> bool:
        """
        TODO
        """

        return self.type == MessageType.REQUEST_FILE

    def is_response_file(self) -> bool:
        """
        TODO
        """

        return self.type == MessageType.RESPONSE_FILE
