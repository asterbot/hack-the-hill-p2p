"""
Global variables for the project

Since the file contains actual directory names, it must be at the root of backend
"""

import os.path

DISCOVERY_PORT = 5000
CHAT_PORT = 5001
MAX_UDP_PACKET = 65507
DISCOVERY_ADDRESS = '192.168.181.255'

BACKEND_FOLDER = os.path.dirname(os.path.abspath(__file__))

UPLOADS_FOLDER = os.path.join(BACKEND_FOLDER, "uploads")
SOURCES_FOLDER = os.path.join(BACKEND_FOLDER, "sources")
CODE_FOLDER = os.path.join(BACKEND_FOLDER, "code")
TEST_FOLDER = os.path.join(BACKEND_FOLDER, "test")
