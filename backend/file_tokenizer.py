"""
TODO
"""

import hashlib
import os
import json

from pathlib import Path


class SenderTokenizer:
    """
    TODO
    """

    def __init__(self, file_path):
        self.file_path = file_path

    def hash_file_blocks(self, block_size=512):
        """
        Takes the original file, creates a .hackthehill file containing a header and a dictionary 
        of keys with hashes. The header contains information regarding the original file and the 
        hashed contents. Information in the header is as follows: name of the file, size of the 
        file, number of hashed blocks present inside the .hackthehill file, size of each block 
        (information that they contain) in bytes. 

        :param block_size: Integer. The default competition block size was 512 bytes, change this 
        to change how large one block can be.
        :return: A hash of the .hackthehill file created, this hashed name of the .hackthehill file 
        be used to hide the nature of the file in communication
        """

        file_size: int = os.path.getsize(self.file_path)
        num_blocks = (file_size + block_size -
                      1) // block_size  # Round up division

        # Create header
        header = {
            "header": {
                "file_name": os.path.basename(self.file_path),
                "file_size": file_size,
                "number_of_blocks": num_blocks,
                "block_size": block_size,
            },
            "blocks": {}
        }

        block_hashes = {}

        with open(self.file_path, 'rb') as file:
            for index in range(num_blocks):
                block = file.read(block_size)
                block_hash = hashlib.sha256(block).hexdigest()
                block_hashes[index] = block_hash

        header["blocks"] = block_hashes

        hash_block = json.dumps(header, indent=2)

        with open("./sources/" + Path(self.file_path).stem + ".hackthehill",
                  'w', encoding="utf-8") as f:
            f.write(hash_block)

        return hashlib.sha256(json.dumps(header).encode('utf-8')).hexdigest()


class RecieverTokenizer:
    """
    TODO
    """

    def __init__(self, file_path):
        self.file_path = file_path

    def get_block_content(self, block_index: int, block_size: int = 512) -> bytes:
        """
        Should take in the hashed file content from .hackthehill file and return back the normal 
        file byte content

        :param file_path: String. String of the file path provided in .hackthehill file.
        :param block_index: Integer. The dictionary index of the block with respect to other 
        blocks in the sequence, from the .hackthehill file 
        :param block_size: Integer. The default competition block size was 512 bytes, change this 
        to change how large one block can be.
        :return: bytes. Particular portion of the original file content.
        """

        file_size = os.path.getsize(self.file_path)
        num_blocks = (file_size + block_size - 1) // block_size

        if block_index < 0 or block_index >= num_blocks:
            raise ValueError(
                f"Block index out of range. Valid range: 0 to {num_blocks - 1}")

        with open(self.file_path, 'rb') as file:
            file.seek(block_index * block_size)
            block_content = file.read(block_size)

        return block_content
