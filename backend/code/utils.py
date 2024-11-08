"""
TODO
"""

import os
import hashlib

from pathlib import Path


def custom_hash(encode_input):
    """
    TODO
    """

    return hashlib.sha256(encode_input.encode("utf-8")).hexdigest()


def find_file(directory, filename):
    """
    TODO
    """

    if os.path.exists(directory):
        for file in os.listdir(directory):
            name, ext = os.path.splitext(file)
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


def idk():
    """
    TODO
    """

    client = 'ok'
    while True:
        x = int(input(
            "Enter 1 to request file fingerprint, 2 to request block, 3 hash the file: "))
        if x == 1:
            file_id = input("File id: ")
            client.request_file_fingerprint(file_id)
        if x == 2:
            file_id = input("File id: ")
            block_index = input("Block index: ")
            client.request_block(file_id, block_index)
        if x == 3:
            with open(os.path.join('sources', 'file.hackthehill'), 'r', encoding="utf-8") as f:
                print(custom_hash(f.read()))
