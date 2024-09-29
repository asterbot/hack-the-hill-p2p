import socket
import threading
import json
import time
import hashlib
import tokenizer
import uuid
from pathlib import Path
import os

DISCOVERY_PORT = 5000
CHAT_PORT = 5001

existing_files = dict()
MAX_UDP_PACKET = 65507


def hash(input):
    return hashlib.sha256(input.encode("utf-8")).hexdigest()


class P2PClient:
    def __init__(self):
        self.user_id = uuid.uuid1().__str__()
        self.peers = dict()
        self.discovery_socket = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM)
        self.discovery_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.discovery_socket.bind(('', DISCOVERY_PORT))
        self.chat_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.chat_socket.bind(('', CHAT_PORT))

        self.index_files()

        self.chat_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_RCVBUF, MAX_UDP_PACKET)
        self.chat_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_SNDBUF, MAX_UDP_PACKET)

    def start(self):
        threading.Thread(target=self.discover_peers, daemon=True).start()
        threading.Thread(target=self.listen_for_messages, daemon=True).start()
        threading.Thread(target=self.announce_presence, daemon=True).start()

    def discover_peers(self):
        while True:
            data, addr = self.discovery_socket.recvfrom(MAX_UDP_PACKET)
            message = json.loads(data.decode())
            if message['type'] == 'announce' and message['user_id'] != self.user_id:
                self.peers[message['user_id']] = addr[0]

    def announce_presence(self):
        while True:
            response = json.dumps({
                'type': 'announce',
                'user_id': self.user_id,
            })
            self.discovery_socket.sendto(
                response.encode(), ('192.168.211.255', DISCOVERY_PORT))
            time.sleep(2)

    def request_file_fingerprint(self, file_id):
        for ip in self.peers.values():
            response = json.dumps({
                'user_id': self.user_id,
                'type': 'request_file_fingerprint',
                'file_id': file_id
            })
            self.chat_socket.sendto(response.encode(), (ip, CHAT_PORT))

    def request_block(self, file_id, block_index):
        for ip in self.peers.values():
            message = json.dumps({
                'user_id': self.user_id,
                'type': 'request_block',
                'file_id': file_id,
                'block_index': block_index,
            })
            self.chat_socket.sendto(message.encode(), (ip, CHAT_PORT))

    def response_file_fingerprint(self, message):
        file_id = message["file_id"]

        caller_ip = self.peers[message["user_id"]]
        # if (file_id in existing_files):
        try:
            file_name = existing_files[file_id][0]
            with open(os.path.join('sources', Path(file_fingerprint_name).stem + ".hackthehill"), "r") as f:
                response = json.dumps({
                    'file_name': file_fingerprint_name,
                    'user_id': self.user_id,
                    'type': 'response_file_fingerprint',
                    'content': f.read(),
                    'file_id': file_id
                })
                self.chat_socket.sendto(
                    response.encode(), (caller_ip, CHAT_PORT))
        except:
            # file doesn't exist error, doesn't need to show
            print("GUYSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
            pass

    def response_block(self, message):
        file_id = message["file_id"]
        block_index = message["block_index"]
        target_file_name = existing_files[file_id][0]

        block_data = tokenizer.get_block_content(
            os.path.join("uploads", target_file_name), block_index)

        response = json.dumps({
            'file_name': target_file_name,
            'user_id': self.user_id,
            'type': 'response_block',
            'file_id': file_id,
            'block_index': block_index,
            'block_data': str(block_data, 'utf-8')
        })

        caller_ip = self.peers[message["user_id"]]

        self.chat_socket.sendto(response.encode(), (caller_ip, CHAT_PORT))

    def save_fingerprint_file(self, message):
        with open(os.path.join('sources',  Path(message['file_name']).stem + '.hackthehill'), 'w') as f:
            f.write(message['content'])

        existing_files[message['file_id']] = [
            message['file_name'], Path(message['file_name']).stem + '.hackthehill']

    def save_block(self, message):
        tmp_file_path = os.path.join('uploads', Path(
            message['file_name']).stem + '.tmp')
        with open(tmp_file_path, 'w+') as f:
            file_content = f.read()
            if len(file_content) > 0:
                content = json.loads(file_content)
                if message['block_index'] not in content:
                    content[message['block_index']] = message['block_data']
                    f.seek(0)
                    f.write(json.dumps(content))
                    f.truncate()
            else:
                d = {message['block_index']: message['block_data']}
                f.write(json.dumps(d))

    def get_all_blocks(self, message):
        print(message)
        file_id = message['file_id']
        with open(os.path.join('sources', Path(message['file_name']).stem + '.hackthehill'), 'r') as f:
            d = json.loads(f.read())
            for block_index in range(int(d['header']['number_of_blocks'])):
                self.request_block(file_id, block_index)

    def listen_for_messages(self):
        while True:
            data, addr = self.chat_socket.recvfrom(MAX_UDP_PACKET)
            message = json.loads(data.decode())
            print(message)

            if (message["type"] == "request_file_fingerprint"):
                self.response_file_fingerprint(message)
            elif (message["type"] == "request_block"):
                self.response_block(message)
            elif (message["type"] == "response_file_fingerprint"):
                self.save_fingerprint_file(message)
                self.get_all_blocks(message)
            elif (message["type"] == "response_block"):
                self.save_block(message)
                self.tmp_to_file(os.path.join(
                    'uploads', Path(message['file_name']).stem+'.tmp'))

            else:
                print("Invalid message type: " + message["type"])

    def index_files(self):
        for fingerprint_file_name in os.listdir("sources"):
            with open(os.path.join("sources", fingerprint_file_name), "r") as f:
                file_fingerprint_content = f.read()
                file_fingerprint_data = json.loads(file_fingerprint_content)

                file_fingerprint_hash = hash(file_fingerprint_content)
                target_file_name = file_fingerprint_data["header"]["file_name"]

                existing_files[file_fingerprint_hash] = [
                    target_file_name, fingerprint_file_name]

    def tmp_to_file(self, tmp_file_path):
        with open(tmp_file_path, 'r') as f:
            content = json.loads(f.read())

        filePath = os.path.join('sources', Path(
            tmp_file_path).stem + '.hackthehill')

        with open(filePath, 'r') as f:
            fileWithExtension = json.loads(f.read())['header']['file_name']

        print("CONTENT:", content)
        s = ""
        for value in content.values():
            print("value:", value)
            s += value

        with open(os.path.join('uploads', fileWithExtension), 'w+') as f:
            f.write(s)

        os.remove(tmp_file_path)


def idk():
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
            with open(os.path.join('sources', 'file.hackthehill'), 'r') as f:
                print(hash(f.read()))
