import socket
import threading

HOST = "0.0.0.0"
PORT = 3000


clients = {}
lock = threading.Lock()


def broadcast(message, sender_username=None):
    with lock:
        for name, sock in clients.items():
            if sender_username is None:
                sock.send(message.encode())
            else:
                if name != sender_username:
                    sock.send(message.encode())


def handle_client(conn, addr):
    global clients

    username = None
    data = conn.recv(1024)
    if not data:
        conn.close()
        return

    username = data.decode().strip()
    if username == "":
        conn.close()
        return

    with lock:
        clients[username] = conn

    join_msg = "[" + username + "] joined from " + addr[0] + ":" + str(addr[1])
    print(join_msg)
    broadcast(join_msg, sender_username=username)

    # message loop
    running = True
    while running is True:
        data = conn.recv(1024)
        if not data:
            # closed connection
            running = False
        else:
            msg = data.decode().strip()
            if msg == "":
                pass
            else:
                if msg.startswith("@"):
                    parts = msg.split(" ", 1)
                    if len(parts) >= 2:
                        target_name = parts[0][1:] 
                        message_text = parts[1]

                        with lock:
                            if target_name in clients:
                                target_sock = clients[target_name]
                            else:
                                target_sock = None

                        if target_sock is not None:
                            private_msg = "[Private from " + username + "]: " + message_text
                            target_sock.send(private_msg.encode())
                        else:
                            error_msg = "User not found.\n"
                            conn.send(error_msg.encode())
                    else:
                        format_msg = "Incorrect format. Use @username message\n"
                        conn.send(format_msg.encode())
                else:
                    out = "[" + username + "]: " + msg
                    broadcast(out, sender_username=username)

    with lock:
        if username in clients:
            if clients[username] == conn:
                del clients[username]

    conn.close()

    leave_msg = "[" + username + "] has left."
    print(leave_msg)
    broadcast(leave_msg, sender_username=username)


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print("[SERVER RUNNING] Listening on " + HOST + ":" + str(PORT))

    try:
        while True:
            conn, addr = server.accept()
            print("New connection from", addr)
            t = threading.Thread(target=handle_client, args=(conn, addr))
            t.start()
    except KeyboardInterrupt:
        print("\n[SERVER SHUTTING DOWN]")

    server.close()


if __name__ == "__main__":
    main()
