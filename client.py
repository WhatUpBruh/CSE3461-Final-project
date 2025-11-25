import sys
import os
import random
import string
from socket import *

if (len(sys.argv) < 3):
  print("Usage: python3 " + sys.argv[0] + " relay_port integer_to_send")
  sys.exit(1)
assert(len(sys.argv) == 3)
relay_port=int(sys.argv[1])

# Read integer
data=sys.argv[2]

# Create a socket for the sender
sender_socket=socket(AF_INET, SOCK_STREAM)

#Q6 TODO: Connect client to the relay at the relay_port; fill the values of <c> and <d>
sender_socket.connect(("127.0.0.1", relay_port))

# Wait until the server has also connected to the relay
input("Press enter to start transmissions")

# Send this to the relay server for it to relay to the receiver
sender_socket.send(data.encode())

# print debugging information
print("Data sent: " + data)

#Q7 TODO: Receive computed answer from relay
newData = sender_socket.recv(200)

# Print received answer
print("Data received: ", newData.decode())

# Close any open sockets
sender_socket.close()
