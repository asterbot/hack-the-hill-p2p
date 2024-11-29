"""
Testing ClientMessage class
"""

import unittest

from code.client_message import ClientMessage, MessageType, MessageError


class TestClientMessage(unittest.TestCase):
    """
    Client Message acts like our custom API calls. It has its own JSON formatting, conditionally
    based on the type of message it is passing.
    """

    def test_load_announce(self):
        """
        Load should put correct values in a given instance given a json response that is of
        ClientMessage format with announce message type.
        """

        message_received = ClientMessage()
        message_received.type = MessageType.ANNOUNCE
        message_received.user_id = 1
        message_received.error = MessageError.NO_ERROR

        json_message_received = message_received.to_json().encode()

        message_decoded = ClientMessage()
        message_decoded.load(json_message_received)

        self.assertEqual(message_decoded, message_received)

    def test_load_request_file(self):
        """
        Load should put correct values in a given instance given a json response that is of
        ClientMessage format with request file message type.
        """

        message_received = ClientMessage()
        message_received.type = MessageType.REQUEST_FILE
        message_received.user_id = 1
        message_received.error = MessageError.NO_ERROR
        message_received.file_id = 2

        json_message_received = message_received.to_json().encode()

        message_decoded = ClientMessage()
        message_decoded.load(json_message_received)

        self.assertEqual(message_decoded, message_received)

    def test_load_response_file(self):
        """
        Load should put correct values in a given instance given a json response that is of
        ClientMessage format with response file message type.
        """

        message_received = ClientMessage()
        message_received.type = MessageType.RESPONSE_FILE
        message_received.user_id = 1
        message_received.error = MessageError.NO_ERROR
        message_received.file_id = 2
        message_received.file_name = "Arjun pookie"
        message_received.content = "Joe Mama"

        json_message_received = message_received.to_json().encode()

        message_decoded = ClientMessage()
        message_decoded.load(json_message_received)

        self.assertEqual(message_decoded, message_received)

    def test_is_type_announce(self):
        """
        Type checker for Client Message, returns correct value for announce function
        """

        client_message = ClientMessage()
        client_message.type = MessageType.ANNOUNCE

        self.assertTrue(client_message.is_type(MessageType.ANNOUNCE))
        self.assertFalse(client_message.is_type(MessageType.REQUEST_FILE))
        self.assertFalse(client_message.is_type(MessageType.RESPONSE_FILE))

    def test_is_type_request_file(self):
        """
        Type checker for Client Message, returns correct value for request file function
        """

        client_message = ClientMessage()
        client_message.type = MessageType.REQUEST_FILE

        self.assertFalse(client_message.is_type(MessageType.ANNOUNCE))
        self.assertTrue(client_message.is_type(MessageType.REQUEST_FILE))
        self.assertFalse(client_message.is_type(MessageType.RESPONSE_FILE))

    def test_is_type_response_file(self):
        """
        Type checker for Client Message, returns correct value for announce function
        """

        client_message = ClientMessage()
        client_message.type = MessageType.RESPONSE_FILE

        self.assertFalse(client_message.is_type(MessageType.ANNOUNCE))
        self.assertFalse(client_message.is_type(MessageType.REQUEST_FILE))
        self.assertTrue(client_message.is_type(MessageType.RESPONSE_FILE))

    def test_equality(self):
        """
        Test equality between two client messages
        """

        client_message_1 = ClientMessage()
        client_message_2 = ClientMessage()

        self.assertEqual(client_message_1, client_message_2)

        client_message_1.type = MessageType.ANNOUNCE
        client_message_2.type = MessageType.ANNOUNCE

        self.assertEqual(client_message_1, client_message_2)

        client_message_1.user_id = 1
        client_message_2.user_id = 1

        self.assertEqual(client_message_1, client_message_2)

        client_message_1.file_id = 2
        client_message_2.file_id = 2

        self.assertEqual(client_message_1, client_message_2)

    def test_different_type_makes_unequal(self):
        """
        Test inequality with message type
        """

        client_message_1 = ClientMessage()
        client_message_2 = ClientMessage()

        client_message_1.type = MessageType.ANNOUNCE
        client_message_2.type = MessageType.REQUEST_FILE

        self.assertNotEqual(client_message_1, client_message_2)

    def test_different_user_id_makes_unequal(self):
        """
        Test inequality with message user id
        """

        client_message_1 = ClientMessage()
        client_message_2 = ClientMessage()

        client_message_1.user_id = 2
        client_message_2.user_id = 3

        self.assertNotEqual(client_message_1, client_message_2)

    def test_different_file_id_makes_unequal(self):
        """
        Test inequality with message file id
        """

        client_message_1 = ClientMessage()
        client_message_2 = ClientMessage()

        client_message_1.file_id = 2
        client_message_2.file_id = 3

        self.assertNotEqual(client_message_1, client_message_2)

    def test_different_file_name_makes_unequal(self):
        """
        Test inequality with message file name
        """

        client_message_1 = ClientMessage()
        client_message_2 = ClientMessage()

        client_message_1.file_name = 2
        client_message_2.file_name = 3

        self.assertNotEqual(client_message_1, client_message_2)

    def test_different_content_makes_unequal(self):
        """
        Test inequality with message content
        """

        client_message_1 = ClientMessage()
        client_message_2 = ClientMessage()

        client_message_1.content = "Joe Mama"
        client_message_2.content = "Arjun pookie"

        self.assertNotEqual(client_message_1, client_message_2)

    def test_different_error_makes_unequal(self):
        """
        Test inequality with message error
        """

        client_message_1 = ClientMessage()
        client_message_2 = ClientMessage()

        client_message_1.error = MessageError.NO_ERROR
        client_message_2.error = MessageError.FILE_NOT_FOUND

        self.assertNotEqual(client_message_1, client_message_2)

    def test_str(self):
        """
        Testing that the string conversion method returns the same result as the json method
        """

        client_message = ClientMessage()
        client_message.type = MessageType.ANNOUNCE
        client_message.user_id = 1
        client_message.error = MessageError.NO_ERROR

        self.assertEqual(str(client_message), client_message.to_json())

        client_message.type = MessageType.REQUEST_FILE
        client_message.user_id = 1
        client_message.file_id = 2
        client_message.error = MessageError.NO_ERROR

        self.assertEqual(str(client_message), client_message.to_json())

        client_message.type = MessageType.RESPONSE_FILE
        client_message.user_id = 1
        client_message.file_id = 2
        client_message.file_name = "Joe Mama"
        client_message.content = "Arjun pookie"
        client_message.error = MessageError.NO_ERROR

        self.assertEqual(str(client_message), client_message.to_json())
