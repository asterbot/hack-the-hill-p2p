import socket
import json
import sys


class ClientSocket:
    def __init__(self, host='localhost', port=8000):
        self.host = host
        self.port = port
        self.socket = None

    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            print(f"Connected to server at {self.host}:{self.port}")
        except Exception as e:
            print(f"Failed to connect to server: {e}")
            sys.exit(1)

    def send_command(self, command):
        try:
            self.socket.send(json.dumps(command).encode('utf-8'))
            response = self.socket.recv(1024).decode('utf-8')
            return json.loads(response)
        except Exception as e:
            print(f"Error sending command: {e}")
            return None

    def publish(self, id, ip):
        command = {
            "type": "publish",
            "id": id,
            "Ip": ip
        }
        response = self.send_command(command)
        if response:
            print(f"Publish response: {response}")

    def retrieve(self, id):
        command = {
            "type": "retrieve",
            "Id": id
        }
        response = self.send_command(command)
        if response:
            print(f"Retrieve response: {response}")

    def close(self):
        if self.socket:
            self.socket.close()
            print("Disconnected from server")


def main():
    client = ClientSocket()
    client.connect()

    while True:
        print("\nAvailable commands:")
        print("1. Publish")
        print("2. Retrieve")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            id = input("Enter ID: ")
            ip = input("Enter IP:port: ")
            client.publish(id, ip)
        elif choice == '2':
            id = input("Enter ID to retrieve: ")
            client.retrieve(id)
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

    client.close()


if __name__ == "__main__":
    main()
