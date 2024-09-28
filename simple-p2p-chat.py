import socket
import threading
import json

DISCOVERY_PORT = 5000
CHAT_PORT = 5001

class P2PClient:
    def __init__(self, username):
        self.username = username
        self.peers = {}
        self.discovery_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.discovery_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.discovery_socket.bind(('', DISCOVERY_PORT))
        self.chat_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.chat_socket.bind(('', CHAT_PORT))
        
        self.thread1=None
        self.thread2=None

    def start(self):
        self.thread1=threading.Thread(target=self.discover_peers, daemon=True).start()
        self.thread2=threading.Thread(target=self.listen_for_messages, daemon=True).start()
        self.announce_presence()
        self.chat_loop()

    def discover_peers(self):
        while True:
            data, addr = self.discovery_socket.recvfrom(1024)
            message = json.loads(data.decode())
            if message['type'] == 'announce' and message['username'] != self.username:
                self.peers[message['username']] = addr[0]
                print(f"Discovered peer: {message['username']} at {addr[0]}")

    def announce_presence(self):
        message = json.dumps({
            'type': 'announce',
            'username': self.username
        })
        self.discovery_socket.sendto(message.encode(), ('<broadcast>', DISCOVERY_PORT))

    def listen_for_messages(self):
        while True:
            data, addr = self.chat_socket.recvfrom(1024)
            if self.thread1 and self.thread2:
                self.thread1.stop()
                self.thread1.join()
                self.thread2.stop()
                self.thread2.join()
                
                self.thread1.start()
                self.thread2.start()
            else:
                print("empty threads")    
            
            message = json.loads(data.decode())
            print(f"\n{message['from']}: {message['content']}")

    def send_message(self, to_username, content):
        if to_username not in self.peers:
            print(f"Peer {to_username} not found")
            return
        message = json.dumps({
            'from': self.username,
            'content': content
        })
        self.chat_socket.sendto(message.encode(), (self.peers[to_username], CHAT_PORT))

    def chat_loop(self):
        while True:
            to_username = input("Send to (or 'quit' to exit): ")
            if to_username.lower() == 'quit':
                break
            content = input("Message: ")
            self.send_message(to_username, content)

if __name__ == "__main__":
    username = input("Enter your username: ")
    client = P2PClient(username)
    client.start()
