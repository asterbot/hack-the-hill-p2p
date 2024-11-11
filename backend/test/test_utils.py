"""
TODO
"""

import unittest
from code.utils import find_file


class TestUtils(unittest.TestCase):
    """
    TODO
    """

    def test_find_file_with_garbage_file_name_returns_none(self):
        """
        If a file does not exist, find_file should return None
        """

        self.assertEqual(find_file("uploads", "random_file.txt"), None)

    def test_find_file_with_garbage_directory_name_returns_none(self):
        """
        If a directory does not exist, find_file should return None
        """

        self.assertEqual(find_file("random_directory", "uploads.txt"), None)
