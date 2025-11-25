# Broadcast Chat Application

This project implements a simple chat system using Python sockets.  
Multiple clients can connect to the server, and each client can send a broadcast message which other clients will recieve. 

---

## Project Structure
- `server.py`: Runs the chat server, accepts multiple clients, and broadcasts messages.
- `client.py`: Connects to the server, allows sending and receiving messages.

---

## 🚀 How to Run

### 1. Start the Server
Run the server script in a terminal:
```bash
python3 server.py

### 2. Start the client
To run multiple clients, just open as many terminals you want and run this script:
```bash
python3 client.py
