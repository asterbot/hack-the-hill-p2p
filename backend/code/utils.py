"""
Utilities Class

Generic functions used throughout the project that don't belong to a particular class
"""

import os
import hashlib

from pathlib import Path
from typing import Optional

from config import SOURCES_FOLDER, UPLOADS_FOLDER


def custom_encoding(normal_input: any) -> str:
    """
    Using utf-8 encoding. This is our custom encoding function we use in the entire project, 
    we should not use the inbuilt functions.

    TODO Correct Implementation has to be written
    """

    return normal_input


def custom_decoding(encoded_string: bytes) -> str:
    """
    Assuming that the encoding is utf-8. We should not read the file to get back the original value.

    TODO Correct Implementation has to be written
    """

    return str(encoded_string)


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

            if file_id == custom_encoding(hackthehill_file_content):
                original_file_name = find_file(UPLOADS_FOLDER, hackthehill_file)
                if original_file_name is not None:
                    return original_file_name, hackthehill_file
    return None
