"""
Testing the File Tokenizer functions.
"""
import json
import os.path
import unittest

from code.file_tokenizer import hash_file_blocks
from code.utils import custom_hash
from config import UPLOADS_FOLDER, SOURCES_FOLDER, HASH_EXTENSION


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

        testing_file = os.path.join(
            UPLOADS_FOLDER,
            "test_hash_file_blocks_with_empty_file_returns_correct_value.txt"
        )
        hackthehill_file = os.path.join(
            SOURCES_FOLDER,
            "test_hash_file_blocks_with_empty_file_returns_correct_value" + HASH_EXTENSION
        )
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
                                 custom_hash(json.dumps(hackthehill_file_content)))

        os.remove(testing_file)
        os.remove(hackthehill_file)
