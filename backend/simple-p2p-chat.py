import socket
import threading
import json
import time
from os import listdir
import hashlib
import tokenizer

DISCOVERY_PORT = 5000
CHAT_PORT = 5001

existing_files = dict()


def hash(input):
    return hashlib.sha256(input.encode("utf-8")).hexdigest()


class P2PClient:
    def __init__(self):
        self.ip = socket.gethostbyname(socket.gethostname())
        self.peers = {}
        self.discovery_socket = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM)
        self.discovery_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.discovery_socket.bind(('', DISCOVERY_PORT))
        self.chat_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.chat_socket.bind(('', CHAT_PORT))

    def start(self):
        threading.Thread(target=self.discover_peers, daemon=True).start()
        threading.Thread(target=self.listen_for_messages, daemon=True).start()
        threading.Thread(target=self.announce_presence, daemon=True).start()

    def discover_peers(self):
        while True:
            data, addr = self.discovery_socket.recvfrom(1024)
            message = json.loads(data.decode())
            if message['type'] == 'announce' and message['ip'] != self.ip:
                self.peers[message['ip']] = addr[0]

    def announce_presence(self):
        while True:
            message = json.dumps({
                'type': 'announce',
                'ip': self.ip
            })
            self.discovery_socket.sendto(
                message.encode(), ('192.168.211.255', DISCOVERY_PORT))
            time.sleep(2)

    # Ask all discovered peers for the file fingerprint
    def request_file_fingerprint(self, message):
        file_id = message["file_id"]

        for ip in self.peers.values():
            message = json.dumps({
                'origin_ip': self.ip,
                'type': 'request_file_fingerprint',
                'file_id': file_id
            })
            self.chat_socket.sendto(message.encode(), (ip, CHAT_PORT))

    # Answering the file fingeprint request
    def response_file_fingerprint(self, message):
        file_id = message["file_id"]
        caller_ip = message["origin_ip"]
        if (file_id in existing_files):
            file_fingerprint_name = './sources/' + existing_files[file_id]
            with open(file_fingerprint_name, "r") as f:

                message = json.dumps({
                    'origin_ip': self.ip,
                    'type': 'reponse_file_fingerprint',
                    'content': f.read()
                })
                self.chat_socket.sendto(
                    message.encode(), (caller_ip, CHAT_PORT))

    # Ask all discovered peers for the block data
    def request_block(self, message):
        file_id = message["file_id"]
        block_index = message["block_index"]

        # asking all peers for the file_id
        # TODO make it so that only one returns it at the time
        for ip in self.peers.values():
            message = json.dumps({
                'origin_ip': self.ip,
                'type': 'request_block',
                'file_id': file_id,
                'block_index': block_index
            })
            self.chat_socket.sendto(message.encode(), (ip, CHAT_PORT))

    def response_block(self, message):
        file_id = message["file_id"]
        block_index = message["block_index"]
        target_file_name = existing_files[file_id][0]

        block_data = tokenizer.get_block_content(
            "./sources/" + target_file_name, block_index)

        message = json.dumps({
            'origin_ip': self.ip,
            'type': 'respond_block',
            'file_id': file_id,
            'block_index': block_index,
            'block_data': block_data
        })

        caller_ip = message["origin_ip"]

        self.chat_socket.sendto(message.encode(), (caller_ip, CHAT_PORT))

    def listen_for_messages(self):
        while True:
            data, addr = self.chat_socket.recvfrom(1024)
            message = json.loads(data.decode())
            print(message)

            if (message["type"] == "request_file_fingerprint"):
                self.request_file_fingerprint(message)
            elif (message["type"] == "request_block"):
                self.request_block(message)
            elif (message["type"] == "response_file_fingerprint"):
                self.response_file_fingerprint(message)
            elif (message["type"] == "response_block"):
                self.response_block(message)
            else:
                print("Invalid message type: " + message["type"])


if __name__ == "__main__":

    for fingerprint_file_name in listdir("./sources/"):
        with open("./sources/" + fingerprint_file_name, "r") as f:
            file_fingerprint_content = f.read()
            file_fingerprint_data = json.loads(file_fingerprint_content)

            file_fingerprint_hash = hash(file_fingerprint_content)
            target_file_name = file_fingerprint_data["header"]["file_name"]

            existing_files[file_fingerprint_hash] = [
                target_file_name, fingerprint_file_name]

    client = P2PClient()
    client.start()
