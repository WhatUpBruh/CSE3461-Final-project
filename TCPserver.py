
from socket import *
import threading

def newClient(connectionSocket, addr):
    print(f'Client {addr} connected')
    try:
        while True:
            sentence = connectionSocket.recv(1024).decode()
            if not sentence or sentence.lower() == 'close':
                print(f'Client {addr} disconnected')
                break
            capitalizedSentence = sentence.upper()
            connectionSocket.send(capitalizedSentence.encode())
    finally:
        connectionSocket.close()


serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM) #creating a server side socket
serverSocket.bind(('',serverPort)) # bind() method associates a server socket witha specific address and port on the local machine
serverSocket.listen(5) #this line means server listens for the TCP connection req. (queue up to 5 clients)

print('The server is ready to receive') # printing to confirm that TCP server is up and ready
while True: #always welcoming 

    connectionSocket, addr = serverSocket.accept() #When a client knocks on this door, the program invokes the method for serverSocket,
                                                    #which creates a new socket in the server, called , dedicated to thisparticular client.
    # Create a new thread to handle this client
    client_thread = threading.Thread(target=newClient, args=(connectionSocket, addr))
    client_thread.daemon = True  # Daemon threads exit when main program exits
    client_thread.start()


