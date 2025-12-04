import socket
import threading

def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(1024).decode()
            if not msg:
                break
            print(msg)
        except:
            print("[Disconnected from server]")
            break


def start_client():
    HOST = input("Enter server IP: ")
    PORT = 9000

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    print(f"[Connected] Local address: {sock.getsockname()}")

    # Send username
    username = input("Enter your username: ")
    sock.send(username.encode())

    # Start background receiver thread
    threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()

    # Main thread: send messages
    while True:
        msg = input()
        if msg.lower() == "quit":
            break

        sock.send(msg.encode())

    sock.close()


if __name__ == "__main__":
    start_client()
