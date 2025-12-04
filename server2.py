import socket
import threading

# Dictionary to store username -> socket
clients = {}
lock = threading.Lock()

def handle_client(conn, addr):
    global clients

    try:
        # Receive username from client
        username = conn.recv(1024).decode().strip()

        with lock:
            clients[username] = conn
        print(f"{username} connected from {addr}")

        # Main loop to receive messages
        while True:
            msg = conn.recv(1024).decode()
            if not msg:
                break

            # Message should be in format: @username message text
            if msg.startswith("@"):
                try:
                    split_msg = msg.split(" ", 1)
                    name = split_msg[0][1:]     # remove @
                    message = split_msg[1]

                    with lock:
                        if name in clients:
                            # send only to target
                            clients[name].send(
                                f"[message from {username}]: {message}".encode()
                            )
                        else:
                            conn.send("User not found.\n".encode())
                except:
                    conn.send("Incorrect format. Use @username message\n".encode())
            else:
                conn.send("Incorrect format. Use @username message\n".encode())

    except Exception as e:
        print(f"Error: {e}")

    finally:
        with lock:
            if username in clients:
                del clients[username]
        conn.close()
        print(f"{username} disconnected")


HOST = "0.0.0.0"
PORT = 9000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print(f"[SERVER RUNNING] Listening on {HOST}:{PORT}")

while True:
    conn, addr = server.accept()
    threading.Thread(target=handle_client, args=(conn, addr)).start()



