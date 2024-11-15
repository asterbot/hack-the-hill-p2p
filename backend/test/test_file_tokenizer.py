"""
Testing the File Tokenizer functions.
"""
import json
import os.path
import unittest

from code.file_tokenizer import hash_file_blocks, get_block_content
from code.utils import custom_encoding
from config import UPLOADS_FOLDER, SOURCES_FOLDER, HASH_EXTENSION
from test.common import write_to_testing_file_and_create_hackthehill, remove_files


class TestFileTokenizer(unittest.TestCase):
    """
    File Tokenizer functions are the core of project, as how they convert data and de-hash it is
    very important to how our application is looking at files. The better the hash and de-hashing,
    the better quality of file sharing we provide.
    """

    def test_hash_file_blocks_with_empty_file_returns_correct_value(self):
        """
        We should only see the header.
        """

        function_name = "test_hash_file_blocks_with_empty_file_returns_correct_value"
        testing_file = os.path.join(UPLOADS_FOLDER, f"{function_name}.txt")
        hackthehill_file = os.path.join(SOURCES_FOLDER, function_name + HASH_EXTENSION)
        test_header = {
            "header": {
                "file_name": os.path.basename(testing_file),
                "file_size": 0,
                "number_of_blocks": 0,
                "block_size": 512,
            },
            "blocks": {}
        }

        with open(testing_file, "x", encoding="utf-8") as _:
            hackthehill_file_hashed_content = hash_file_blocks(testing_file)

            with open(hackthehill_file, "r", encoding="utf-8") as g:
                hackthehill_file_content = json.loads(g.read())

                self.assertEqual(hackthehill_file_content, test_header)
                self.assertEqual(hackthehill_file_hashed_content,
                                 custom_encoding(json.dumps(hackthehill_file_content)))

        remove_files(function_name)

    def test_hash_file_blocks_with_non_empty_file_returns_correct_value(self):
        """
        We should see the correct header plus the correct hashed blocks
        """

        function_name = "test_hash_file_blocks_with_non_empty_file_returns_correct_value"
        testing_file = os.path.join(UPLOADS_FOLDER, f"{function_name}.txt")
        hackthehill_file = os.path.join(SOURCES_FOLDER, function_name + HASH_EXTENSION)
        block_size = 1024
        test_header = {
            "header": {
                "file_name": os.path.basename(testing_file),
                "file_size": 0,
                "number_of_blocks": 0,
                "block_size": block_size,
            },
            "blocks": {}
        }

        with open(testing_file, "x", encoding="utf-8") as f:
            f.write(function_name)

        file_size = os.path.getsize(testing_file)
        num_blocks = (file_size + block_size - 1) // block_size

        test_header["header"]["file_size"] = file_size

        with open(testing_file, "r", encoding="utf-8") as f:
            hackthehill_file_hashed_content = hash_file_blocks(testing_file, block_size)

            for index in range(num_blocks):
                block = f.read(block_size)
                block_hash = custom_encoding(block)
                test_header["blocks"][str(index)] = str(block_hash)
                test_header["header"]["number_of_blocks"] += 1

            with open(hackthehill_file, "r", encoding="utf-8") as g:
                hackthehill_file_content = json.loads(g.read())

                self.assertEqual(hackthehill_file_content, test_header)
                self.assertEqual(hackthehill_file_hashed_content,
                                 custom_encoding(json.dumps(hackthehill_file_content)))

        remove_files(function_name)

    def test_get_block_content_block_out_index_throws_error(self):
        """
        For block index out of range, we should raise ValueError
        """

        function_name = "test_get_block_content_block_out_index_throws_error"
        testing_file = os.path.join(UPLOADS_FOLDER, f"{function_name}.txt")
        hackthehill_file = os.path.join(SOURCES_FOLDER, function_name + HASH_EXTENSION)

        write_to_testing_file_and_create_hackthehill(function_name, testing_file)

        self.assertRaises(ValueError, get_block_content, hackthehill_file, -1)
        self.assertRaises(ValueError, get_block_content, hackthehill_file, 1)

        remove_files(function_name)

    def test_get_block_content_returns_correct_value(self):
        """
        Remember that the indexing starts at 0. Given the encoding function, we should see the 
        correct decoding being applied, such that we don't need to original file to decode the 
        .hackthehill's content. Now, the data transmission totally depends on the encoding and 
        decoding.
        """

        function_name = "test_get_block_content_returns_correct_value"
        testing_file = os.path.join(UPLOADS_FOLDER, f"{function_name}.txt")
        hackthehill_file = os.path.join(SOURCES_FOLDER, function_name + HASH_EXTENSION)

        with open(testing_file, "x", encoding="utf-8") as f:
            f.write(function_name)

        hash_file_blocks(testing_file)

        encoded_text = custom_encoding(function_name)

        self.assertEqual(get_block_content(hackthehill_file, 0), encoded_text)

        remove_files(function_name)
