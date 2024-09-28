import socket
import threading

HEADER = 64 # length of incoming message in the header
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT" # should be sent by clients if they're disconnecting from the server

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    """
    Handles communication between client and server
    """
    print(f"[NEW CONNECTION] {addr} connected")
    
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT) # receive message from client (header)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            
            conn.send("Msg received".encode(FORMAT))
            print(f"[{addr}] {msg}")

def start():
    """
    Handles connections and distributes them where they need to go
    """
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target = handle_client, args = (conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("[STARTING] server is starting...")
start()
