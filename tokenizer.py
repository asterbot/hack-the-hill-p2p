import hashlib
import sys
import os
import json

def hash_file_blocks(file_path, block_size=512):
    file_size = os.path.getsize(file_path)
    num_blocks = (file_size + block_size - 1) // block_size  # Round up division

    # Create header
    header = {
        "file_name": os.path.basename(file_path),
        "file_size": file_size,
        "number_of_blocks": num_blocks,
        "block_size": block_size
    }

    # Print header
    print("Header:")
    print(json.dumps(header, indent=2))
    print("\nBlock Hashes:")

    block_hashes = []
    with open(file_path, 'rb') as file:
        for block_num in range(num_blocks):
            block = file.read(block_size)
            block_hash = hashlib.sha256(block).hexdigest()
            block_hashes.append(block_hash)
            print(f"Block {block_num + 1}: {block_hash}")

    return header, block_hashes

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    hash_file_blocks(file_path)