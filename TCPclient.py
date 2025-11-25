
from socket import *
serverName = "127.0.0.1" #or local host "127.0.0.1"#"192.168.1.2"#'hostname'#server's IP address (preciselyIPv4)'servername'
serverPort = 12000 #un-reserved port #

clientSocket = socket(AF_INET, SOCK_STREAM) #creates client side TCP socket

clientSocket.connect((serverName,serverPort)) # initiates TCP connection . Afterthis line is executed, three-way handshake is performed and a

userInput = input('Enter your broadcast message or \'close\' to end chat: ')
while userInput.lower() != 'close':
    clientSocket.send(userInput.encode()) #sends user input to server after encoding
    modifiedMessage = clientSocket.recv(1024) #receives modified message from server
    print('From Server: ', modifiedMessage.decode()) #decodes and prints the modified message
    userInput = input('Enter your broadcast message or \'close\' to end chat: ')

clientSocket.close() #closes the socket when user types 'close'

# TCP connection is established
# sentence = input('Input lowercase sentence:') #reads the string from client sideuser

# clientSocket.send(sentence.encode()) # this line encodes and sends the string

# modifiedSentence = clientSocket.recv(1024) # the string is received here aftergetting modified from server. recv() method receives data from a socket and stores it in a buffer

# print('From Server: ', modifiedSentence.decode()) # the string (now in UPPERCASE)is received from server, and decoded.

# clientSocket.close() # this closes the socket
