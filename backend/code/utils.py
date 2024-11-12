"""
Utilities Class

Generic functions used throughout the project that don't belong to a particular class
"""

import os
import hashlib

from pathlib import Path
from typing import Optional


def custom_hash(encode_input):
    """
    Using the hashlib sha256 encoding, we specifically hash the utf-8 encoding for 
    text files. This is our custom hash function we use in the entire project, we should not
    use the inbuilt hash() function
    """

    return hashlib.sha256(encode_input.encode("utf-8")).hexdigest()


def find_file(directory: str, filename: str) -> Optional[str]:
    """
    Helper function for get_filename_by_file_id
    
    Given a directory and a filename, check if the directory exists, and if the file
    exists inside the given directory. If yes, return the file name, otherwise return
    None
    
    :param directory: str
    :param filename: str
    :returns: Either string or None
    """

    if os.path.exists(directory):
        for file in os.listdir(directory):
            name, _ = os.path.splitext(file)
            if name == filename:
                return file
    return None


def get_filename_by_file_id(file_id):
    """
    TODO
    """

    for fingerprint_file_name in os.listdir("sources"):
        with open(os.path.join("sources", fingerprint_file_name), "r", encoding="utf-8") as f:
            file_fingerprint_content = f.read()

            if file_id == custom_hash(file_fingerprint_content):
                file_name = find_file(
                    "uploads", Path(fingerprint_file_name).stem)
                if file_name is not None:
                    return [file_name, fingerprint_file_name]
    return None
