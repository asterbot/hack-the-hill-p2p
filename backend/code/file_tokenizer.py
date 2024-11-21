"""
This file helps in creating and interpreting a .hackthehill file
"""

import os
import json

from pathlib import Path

from code.utils import custom_encoding, custom_decoding
from config import SOURCES_FOLDER, HASH_EXTENSION


def hash_file_blocks(file_path: str, block_size: int = 512):
    """
    Takes the original file, creates a .hackthehill file containing a header and a dictionary
    of keys with hashes. The header contains information regarding the original file and the
    hashed contents. Information in the header is as follows: name of the file, size of the
    file, number of hashed blocks present inside the .hackthehill file, size of each block
    (information that they contain) in bytes.

    :param file_path: str. The path to the original file.
    :param block_size: Integer. The default competition block size was 512 bytes, change this
    to change how large one block can be.
    :return: A hash of the .hackthehill file created, this hashed name of the .hackthehill file
    be used to hide the nature of the file in communication.
    """

    hackthehill_file = Path(file_path).stem + HASH_EXTENSION
    file_size: int = os.path.getsize(file_path)
    num_blocks = (file_size + block_size - 1) // block_size

    # Create header
    header = {
        "header": {
            "file_name": os.path.basename(file_path),
            "file_size": file_size,
            "number_of_blocks": num_blocks,
            "block_size": block_size,
        },
        "blocks": {}
    }

    block_hashes = {}

    with open(file_path, "r", encoding="utf-8") as file:
        for index in range(num_blocks):
            block = file.read(block_size)
            block_hash = custom_encoding(block)
            block_hashes[index] = block_hash

    header["blocks"] = block_hashes

    hash_block = json.dumps(header, indent=2)

    with open(os.path.join(SOURCES_FOLDER, hackthehill_file), 'w', encoding="utf-8") as f:
        f.write(hash_block)

    return custom_encoding(json.dumps(header))


def get_block_content(hackthehill_file: str, block_index: int) -> str:
    """
    Should take in the hashed file content from .hackthehill file and return back the normal
    file byte content

    :param hackthehill_file: str. The path to the .hackthehill file.
    :param block_index: Integer. The dictionary index of the block with respect to other
    blocks in the sequence, from the .hackthehill file.
    :return: bytes. Particular portion of the original file content.
    """

    with open(hackthehill_file, "r", encoding="utf-8") as f:
        file_content = json.loads(f.read())
        num_blocks = file_content["header"]["number_of_blocks"]

        if block_index < 0 or block_index >= num_blocks:
            raise ValueError(
                f"Block index out of range. Valid range: 0 to {num_blocks - 1}")

        encoded_content = file_content["blocks"][str(block_index)]
        block_content = custom_decoding(encoded_content)

    return block_content
