"""
Global variables for the project

Since the file contains actual directory names, it must be at the root of backend
"""

import os.path

GLOBAL_IP: str = '0.0.0.0'
PORT: int = 9999
MAX_DATA_SIZE: int = 1024

HASH_EXTENSION: str = ".hackthehill"

BACKEND_FOLDER: str = os.path.dirname(os.path.abspath(__file__))

UPLOADS_FOLDER: str = os.path.join(BACKEND_FOLDER, "uploads")
SOURCES_FOLDER: str = os.path.join(BACKEND_FOLDER, "sources")
CODE_FOLDER: str = os.path.join(BACKEND_FOLDER, "code")
TEST_FOLDER: str = os.path.join(BACKEND_FOLDER, "test")

WEBSITE_DATA: str = os.path.join(CODE_FOLDER, "website_data.json")
