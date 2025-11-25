import socket
import threading

HOST = '127.0.0.1'
PORT = 3000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Function to receive messages from the server
def receive_messages():
    while True:
        # Handle incoming messages from server
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(f"\nReceived: {message}")
            print("You: ", end='', flush=True)
        except:
            print("Connection closed.")
            break

# Function to send messages to the server
def send_messages():
    while True:
        message = input("You: ")
        # Exit on 'quit' or 'exit'
        if message.lower() in ("quit", "exit"):
            client_socket.close()
            print("You left the chat.")
            break
        client_socket.send(message.encode())

# Start threads to receive messages
threading.Thread(target=receive_messages, daemon=True).start()

# Background thread to send messages
try:
    send_messages()
except KeyboardInterrupt:
    client_socket.close()
    print("\nClient closed.")

