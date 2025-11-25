import sys
import os
import random
import string
from socket import *

if (len(sys.argv) < 2):
  print("Usage: python3 " + sys.argv[0] + " relay_port")
  sys.exit(1)
assert(len(sys.argv) == 2)
relay_port=int(sys.argv[1])

#Q8 TODO: Create a TCP socket for the server  [preferably with name <receiver_socket> to be complaint with the rest of the code]
receiver_socket = socket(AF_INET, SOCK_STREAM)

#Q9 TODO: Connect this socket to the relay at relay_port
receiver_socket.connect(("127.0.0.1", relay_port))

# Receive any data relayed from the relay (i.e., any data sent by the sender to the relay)
data = receiver_socket.recv(200)

# Print debugging information
print("Data received: ", data.decode())

#Q10 Convert received number to binary; feel free to use inbuilt function
send_data = bin(int(data.decode()))[2:]

# Send computed answer back to relay
receiver_socket.send(send_data.encode())

# Print debugging information
print("Data sent back: ", send_data)

# Close any open sockets
receiver_socket.close()
