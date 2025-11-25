import sys
from socket import *

if (len(sys.argv) < 2):
  print("Usage: python3 " + sys.argv[0] + " relay_port")
  sys.exit(1)
assert(len(sys.argv) == 2)
relay_port=int(sys.argv[1])


# Q1 TODO: Create a relay socket to listen on relay_port for new connections; Insert appropriate values for <a>, <b>  [Hint: Its a TCP socket]
relay_listener_socket = socket(AF_INET, SOCK_STREAM)

# Bind the relay's socket to relay_port
relay_listener_socket.bind(("127.0.0.1", relay_port))

# Put relay_listener_socket in LISTEN mode
relay_listener_socket.listen(1)

# Accept a connection first from relay_sender.py
(sender_socket, sender_addr) = relay_listener_socket.accept()

# Q2 TODO: Then, accept a connection from server.py
(receiver_socket, receiver_addr) = relay_listener_socket.accept()

# Receive data from sender
data=sender_socket.recv(200)

# Q3 TODO: Forward data to server
receiver_socket.send(data)

# Print data that was relayed
print("Data relayed: ", data.decode())

#Q4 TODO: Recive computed answer from server
data_receiver=receiver_socket.recv(200)

#Q5 TODO: Forward answer back to client
sender_socket.send(data_receiver)

# Print data that was relayed back
print("Data relayed back: ", data_receiver.decode())

# Close any open sockets
sender_socket.close()
receiver_socket.close()
relay_listener_socket.close()