
import socket
import threading

HOST = '127.0.0.1'
PORT = 3000

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((HOST, PORT))
serverSocket.listen()

clients = []  # track connected sockets
addresses = {}  # map socket → address string

def broadcast(message, sender_socket=None):
    # send message to all clients except the sender
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                client.close()
                if client in clients:
                    clients.remove(client)

def handle_client(client_socket):
    addr = addresses[client_socket]
    # listen for messages from client
    try:
        while True:
            message = client_socket.recv(1024)
            if not message:
                break
            broadcast(message, client_socket)
    except:
        pass
    finally:
        # client disconnected
        clients.remove(client_socket)
        client_socket.close()
        leave_msg = f"[{addr}] has left".encode()
        broadcast(leave_msg)

print(f"Server listening on {HOST}:{PORT}...")

try:
    while True:
        # Accept new connections and send a broadcase message to all clients
        client_socket, addr = serverSocket.accept()
        addr_str = f"{addr[0]}:{addr[1]}"
        print(f"New connection from {addr_str}")
        clients.append(client_socket)
        addresses[client_socket] = addr_str

        # announce join to all the clients in the chat
        join_msg = f"[{addr_str}] has joined.".encode()
        broadcast(join_msg, sender_socket=None)

        # Threading is used to handle multiple clients simultaneously
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()
except KeyboardInterrupt:
    print("\nServer shutting down...")
    for client in clients:
        client.close()
    serverSocket.close()
