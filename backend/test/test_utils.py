"""
Testing the Utilities class
"""
import hashlib
import os.path
import unittest

from code.file_tokenizer import hash_file_blocks
from code.utils import find_file, custom_hash, get_filename_by_file_id

from config import SOURCES_FOLDER, CODE_FOLDER, UPLOADS_FOLDER, HASH_EXTENSION


class TestUtils(unittest.TestCase):
    """
    Utilities class functions are generic and widely used. Their implementation is very important.
    """

    def test_custom_hash(self):
        """
        We have our own implementation for hashing utf-8 format encoding
        """

        encoded_input = "Hi Mom"

        self.assertEqual(custom_hash(encoded_input),
                         hashlib.sha256(encoded_input.encode("utf-8")).hexdigest())

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

        os.remove(testing_file)

    def test_get_filename_by_file_id_with_matching_id_returns_tuple(self):
        """
        If the hashed id is the same as the hash of .hackthehill file, we should return the
        tuple of filenames
        """

        function_name = "test_get_filename_by_file_id_with_matching_id_returns_tuple"
        testing_file = os.path.join(UPLOADS_FOLDER, f"{function_name}.txt")
        hackthehill_file = os.path.join(SOURCES_FOLDER, function_name + HASH_EXTENSION)

        with open(testing_file, "x", encoding="utf-8") as f:
            f.write(function_name)
            hash_file_blocks(testing_file)

            with open(hackthehill_file, "r", encoding="utf-8") as g:
                hackthehill_file_content = g.read()
                file_id = custom_hash(hackthehill_file_content)

            self.assertEqual(get_filename_by_file_id(file_id),
                             (os.path.basename(testing_file),
                              os.path.basename(hackthehill_file)))

        os.remove(testing_file)
        os.remove(hackthehill_file)
