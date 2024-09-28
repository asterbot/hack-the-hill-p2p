import socket
import json
import threading
from collections import defaultdict


class CentralServer:
    def __init__(self, host='0.0.0.0', port=8000):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        # Maps ID to a set of IP:port strings
        self.connections = defaultdict(set)

    def start(self):
        self.server_socket.listen(5)
        print(f"Server listening on {self.host}:{self.port}")
        while True:
            client_socket, address = self.server_socket.accept()
            client_thread = threading.Thread(
                target=self.handle_client, args=(client_socket, address))
            client_thread.start()

    def handle_client(self, client_socket, address):
        while True:
            try:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                request = json.loads(data)
                response = self.process_request(request, address)
                client_socket.send(json.dumps(response).encode('utf-8'))
            except json.JSONDecodeError:
                response = {"status": "error", "message": "Invalid JSON"}
                client_socket.send(json.dumps(response).encode('utf-8'))
            except Exception as e:
                response = {"status": "error", "message": str(e)}
                client_socket.send(json.dumps(response).encode('utf-8'))

        self.handle_disconnect(address)
        client_socket.close()

    def process_request(self, request, address):
        if request['type'] == 'publish':
            return self.handle_publish(request, address)
        elif request['type'] == 'retrieve':
            return self.handle_retrieve(request)
        else:
            return {"status": "error", "message": "Invalid request type"}

    def handle_publish(self, request, address):
        id = request['id']
        ip_port = request['Ip']
        self.connections[id].add(ip_port)
        return {"status": "ok"}

    def handle_retrieve(self, request):
        id = request['Id']
        if id in self.connections:
            return {"status": "ok", "Ip": list(self.connections[id])}
        else:
            return {"status": "error", "message": "ID not found"}

    def handle_disconnect(self, address):
        disconnected_ip = f"{address[0]}:{address[1]}"
        # very optimized omg
        for id, ip_set in self.connections.items():
            if disconnected_ip in ip_set:
                ip_set.remove(disconnected_ip)
        # Remove any empty sets
        self.connections = {k: v for k, v in self.connections.items() if v}


if __name__ == "__main__":
    server = CentralServer()
    server.start()
