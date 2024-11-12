"""
Testing the Utilities class
"""
import hashlib
import unittest
from code.utils import find_file, custom_hash


class TestUtils(unittest.TestCase):
    """
    Utilities class functions are generic and widely used. Their implementation is very important.
    """
    
    def test_custom_hash(self):
        """
        We have our own implementation for hashing utf-8 format encoding
        """
        
        encoded_input = "Hi Mom"
        
        self.assertEqual(custom_hash(encoded_input), hashlib.sha256(encoded_input.encode("utf-8")).hexdigest())

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
    
    def test_find_file_with_proper_director_and_file_returns_filename(self):
        """
        If a file and directory exists, and file exists inside the directory, return the 
        filename
        """
        
        self.assertEqual(find_file("code", "utils"), "utils.py")
        
     