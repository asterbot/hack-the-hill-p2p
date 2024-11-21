"""
Our custom class for backend API messages. These messages are sent between two clients.
"""

import json
from enum import Enum
from typing import Optional


class MessageType(Enum):
    """
    Our API calls can only have these type of requests.

    1. Announce -> Telling the network devices that you can be friends 
    2. Request_File -> Self-explanatory
    3. Response_File -> Respond back with the data of the file requested.
    """

    ANNOUNCE = 'announce'
    REQUEST_FILE = 'request_file'
    RESPONSE_FILE = 'response_file'


class MessageError(Enum):
    """
    Our API calls can have the follow errors/failures
    """

    NO_ERROR = 0
    FILE_NOT_FOUND = 1


class ClientMessage:
    """
    Backend API message format, that is sent between two clients on the same network.
    """

    def __init__(self):
        self.type: Optional[MessageType] = None
        self.user_id: Optional[str] = None
        self.file_id: Optional[str] = None
        self.file_name: Optional[str] = None
        self.content: Optional[str] = None
        self.error: MessageError = MessageError.NO_ERROR

    def load(self, data_bytes: bytes) -> None:
        """
        Given the data coming from another client, we can load the data they are sending
        considering what is the type of the message.
        """

        json_message = json.loads(data_bytes.decode())
        self.type = MessageType(json_message['type']).name
        self.user_id = json_message['user_id']
        self.error = MessageError(json_message['error']).name

        assert self.type
        assert self.user_id
        assert self.error

        if self.type == MessageType.REQUEST_FILE:
            self.file_id = json_message['file_id']

            assert self.file_id

        if self.type == MessageType.RESPONSE_FILE:
            self.file_id = json_message['file_id']
            self.file_name = json_message['file_name']
            self.content = json_message['content']

            assert self.file_id
            assert self.file_name
            assert self.content

    def to_json(self) -> str:
        """
        Given the type of message we currently have, we can convert our personal message to
        a json format, ready for sending to another client as a API message.
        """

        assert self.type
        assert self.user_id
        assert self.error

        information = {
            'type': self.type.value,
            'user_id': self.user_id,
            'error': self.error.value
        }

        if self.type == MessageType.REQUEST_FILE:
            assert self.file_id

            information['file_id'] = self.file_id
        elif self.type == MessageType.RESPONSE_FILE:
            assert self.file_id
            assert self.file_name
            assert self.content

            information['file_id'] = self.file_id
            information['file_name'] = self.file_name
            information['content'] = self.content

        return json.dumps(information)

    def is_type(self, message_type: MessageType) -> bool:
        """
        Boolean checker for the message type.
        """

        return self.type == message_type
