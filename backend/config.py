"""
Global variables for the project

Since the file contains actual directory names, it must be at the root of backend
"""

import os.path

DISCOVERY_PORT: int = 5000
CHAT_PORT: int = 5001
MAX_UDP_PACKET: int = 65507
DISCOVERY_ADDRESS: str = "192.168.181.255"
HASH_EXTENSION: str = ".hackthehill"

BACKEND_FOLDER: str = os.path.dirname(os.path.abspath(__file__))

UPLOADS_FOLDER: str = os.path.join(BACKEND_FOLDER, "uploads")
SOURCES_FOLDER: str = os.path.join(BACKEND_FOLDER, "sources")
CODE_FOLDER: str = os.path.join(BACKEND_FOLDER, "code")
TEST_FOLDER: str = os.path.join(BACKEND_FOLDER, "test")

WEBSITE_DATA: str = os.path.join(CODE_FOLDER, "website_data.json")
