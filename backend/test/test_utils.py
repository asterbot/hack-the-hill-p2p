"""
Testing the Utilities class
"""

import os.path
import unittest

from code.utils import find_file, custom_encoding, get_filename_by_file_id, custom_decoding
from test.common import write_to_testing_file_and_create_hackthehill, remove_files

from config import SOURCES_FOLDER, CODE_FOLDER, UPLOADS_FOLDER, HASH_EXTENSION


class TestUtils(unittest.TestCase):
    """
    Utilities class functions are generic and widely used. Their implementation is very important.
    """

    def test_custom_encoding(self):
        """
        We have our own implementation for utf-8 format encoding
        """

        standard_input = "Hi Mom"

        self.assertEqual(custom_encoding(standard_input), standard_input)

    def test_custom_decoding(self):
        """
        We have our own implementation for utf-8 format decoding
        """

        standard_input = "Hi Mom"
        encoded_input = custom_encoding(standard_input)

        self.assertEqual(custom_decoding(encoded_input), encoded_input)

    def test_find_file_with_garbage_file_name_returns_none(self):
        """
        If a file does not exist, find_file should return None
        """

        self.assertEqual(find_file("uploads", "random_file.txt"),
                         None)

    def test_find_file_with_garbage_directory_name_returns_none(self):
        """
        If a directory does not exist, find_file should return None
        """

        self.assertEqual(find_file("random_directory", "uploads.txt"),
                         None)

    def test_find_file_with_proper_director_and_file_returns_filename(self):
        """
        If a file and directory exists, and file exists inside the directory, return the
        filename
        """

        self.assertEqual(find_file(CODE_FOLDER, "utils.py"),
                         "utils.py")

    def test_get_filename_by_file_id_with_no_matching_id_returns_none(self):
        """
        If none of the hashed ids match with the file id, we should return None
        """

        function_name = "test_get_filename_by_file_id_with_no_matching_id_returns_none"
        testing_file = os.path.join(UPLOADS_FOLDER, f"{function_name}.txt")

        with open(testing_file, "x", encoding="utf-8") as f:
            f.write(function_name)
            file_id = "random-file-id"

            self.assertEqual(get_filename_by_file_id(file_id), None)

        remove_files(function_name)

    def test_get_filename_by_file_id_with_matching_id_returns_tuple(self):
        """
        If the hashed id is the same as the hash of .hackthehill file, we should return the
        tuple of filenames
        """

        function_name = "test_get_filename_by_file_id_with_matching_id_returns_tuple"
        testing_file = os.path.join(UPLOADS_FOLDER, f"{function_name}.txt")
        hackthehill_file = os.path.join(SOURCES_FOLDER, function_name + HASH_EXTENSION)

        write_to_testing_file_and_create_hackthehill(function_name, testing_file)

        with open(hackthehill_file, "r", encoding="utf-8") as g:
            hackthehill_file_content = g.read()
            file_id = custom_encoding(hackthehill_file_content)

        self.assertEqual(get_filename_by_file_id(file_id),
                         (os.path.basename(testing_file),
                          os.path.basename(hackthehill_file)))

        remove_files(function_name)
