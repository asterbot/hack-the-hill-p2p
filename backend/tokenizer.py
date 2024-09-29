import hashlib
import sys
import os
import json
from pathlib import Path


def hash_file_blocks(file_path, block_size=512):
    file_size = os.path.getsize(file_path)
    num_blocks = (file_size + block_size -
                  1) // block_size  # Round up division

    # Create header
    header = {
        "header": {
            "file_name": os.path.basename(file_path),
            "file_size": file_size,
            "number_of_blocks": num_blocks,
            "block_size": block_size,
        },
        "blocks": dict()
    }

    # Print header
    # print("Header:")
    # print("\nBlock Hashes:")

    block_hashes = dict()
    index = 0

    with open(file_path, 'rb') as file:
        for block_num in range(num_blocks):
            block = file.read(block_size)
            block_hash = hashlib.sha256(block).hexdigest()
            block_hashes[index] = block_hash
            index += 1

    header["blocks"] = block_hashes
    
    hash_block = json.dumps(header, indent=2)

    with open("./sources/" + Path(file_path).stem + ".hackthehill", 'w') as f:
        f.write(hash_block)

    return hashlib.sha256(json.dumps(header).encode('utf-8')).hexdigest()


def get_block_content(file_path, block_index, block_size=512):
    block_index = int(block_index)
    file_size = os.path.getsize(file_path)
    num_blocks = (file_size + block_size - 1) // block_size

    if block_index < 0 or block_index >= num_blocks:
        raise ValueError(
            f"Block index out of range. Valid range: 0 to {num_blocks - 1}")

    with open(file_path, 'rb') as file:
        file.seek(block_index * block_size)
        block_content = file.read(block_size)

    return block_content


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <file_path> [block_index]")
        sys.exit(1)

    file_path = sys.argv[1]

    if len(sys.argv) == 2:
        # If only file path is provided, run the hash_file_blocks function
        file_hash = hash_file_blocks(file_path)
        print(file_hash)
    elif len(sys.argv) == 3:
        # If both file path and block index are provided, run the get_block_content function
        try:
            block_index = int(sys.argv[2])
            block_content = get_block_content(file_path, block_index)
            print(f"Content of block {block_index}:")
            print(block_content)
        except ValueError as e:
            print(f"Error: {e}")
    else:
        print(
            "Too many arguments. Usage: python script.py <file_path> [block_index]")
        sys.exit(1)
