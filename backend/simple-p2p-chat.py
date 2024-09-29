import socket
import threading
import json
import time
import uuid

DISCOVERY_PORT = 5000
CHAT_PORT = 5001

class P2PClient:
    def __init__(self):
        self.user_id = uuid.uuid1().__str__()
        self.peers = {}
        self.discovery_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.discovery_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.discovery_socket.bind(('', DISCOVERY_PORT))
        self.chat_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.chat_socket.bind(('', CHAT_PORT))

    def start(self):
        threading.Thread(target=self.discover_peers, daemon=True).start()
        threading.Thread(target=self.listen_for_messages, daemon=True).start()
        threading.Thread(target=self.announce_presence, daemon=True).start()
        # self.announce_presence()
        self.chat_loop()

    def discover_peers(self):
        while True:
            data, addr = self.discovery_socket.recvfrom(1024)
            message = json.loads(data.decode())
            if message['type'] == 'announce' and message['user_id'] != self.user_id:
                self.peers[message['user_id']] = addr[0]
                # print(f"Discovered peer: {message['user_id']} at {addr[0]}")

    def announce_presence(self):
        while True:
            message = json.dumps({
                'type': 'announce',
                'user_id': self.user_id
            })
            self.discovery_socket.sendto(message.encode(), ('192.168.211.255', DISCOVERY_PORT))
            time.sleep(2)

    def listen_for_messages(self):
        while True:
            data, addr = self.chat_socket.recvfrom(1024)
            print(type(data))
            message = json.loads(data.decode())
            print(f"\n{message['from']}: {message['content']}")

    def request_id(self, file_id):
        for ip in self.peers.values():
            message = json.dumps({
                'from': self.user_id,
                'content': file_id
            })
            self.chat_socket.sendto(message.encode(), (ip, CHAT_PORT))

    def chat_loop(self):
        while True:
            to_user_id = input("Send to (or 'quit' to exit): ")
            # if to_user_id.lower() == 'quit':
            #     break
            file_id = input("Enter file id: ")
            self.request_id(file_id)

if __name__ == "__main__":
    # user_id = input("Enter your user_id: ")
    client = P2PClient()
    client.start()
