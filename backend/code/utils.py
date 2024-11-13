"""
Utilities Class

Generic functions used throughout the project that don't belong to a particular class
"""

import os
import hashlib

from pathlib import Path
from typing import Optional

from config import SOURCES_FOLDER, UPLOADS_FOLDER


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
            if name == Path(filename).stem:
                return file
    return None


def get_filename_by_file_id(file_id: str) -> Optional[tuple[str, str]]:
    """
    Given the unique file id we have, we check if original file which is related to
    that particular file id exists or not. Returns None if file does not exist in that directory
    Note that by our convention, .hackthehill files exist in backend/sources and the
    original files exist in backend/uploads.

    :param file_id: str
    :returns: tuple[str, str] | None
    """

    for hackthehill_file in os.listdir(SOURCES_FOLDER):
        with open(os.path.join(SOURCES_FOLDER, hackthehill_file), "r", encoding="utf-8") as f:
            hackthehill_file_content = f.read()

            if file_id == custom_hash(hackthehill_file_content):
                original_file_name = find_file(UPLOADS_FOLDER, hackthehill_file)
                if original_file_name is not None:
                    return original_file_name, hackthehill_file
    return None
