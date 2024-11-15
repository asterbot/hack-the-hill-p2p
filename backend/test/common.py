"""
Common Code for testing class
"""

import os

from code.file_tokenizer import hash_file_blocks
from config import UPLOADS_FOLDER, SOURCES_FOLDER, HASH_EXTENSION


def write_to_testing_file_and_create_hackthehill(function_name: str, testing_file: str) -> None:
    """
    Write the function name to the testing file (which is generated as a side effect) and 
    generate the hackthehill function (also a side effect).
    """

    with open(testing_file, "x", encoding="utf-8") as f:
        f.write(function_name)
        hash_file_blocks(testing_file)


def remove_files(function_name: str):
    """
    Remove the files generated while testing components
    """

    testing_file = os.path.join(UPLOADS_FOLDER, f"{function_name}.txt")
    hackthehill_file = os.path.join(SOURCES_FOLDER, function_name + HASH_EXTENSION)

    if os.path.exists(testing_file):
        os.remove(testing_file)

    if os.path.exists(hackthehill_file):
        os.remove(hackthehill_file)
