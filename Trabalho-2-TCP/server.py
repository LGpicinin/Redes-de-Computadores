import socket
import sys
import math
import os
from time import sleep
from threading import Thread
 

TEST_FILE = './serverFiles/teste.txt'
NAMES_FILE = './serverFiles/names.txt'
PATH = './serverFiles/'

port = 5000
host = "localhost"


def createSocket():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('\nSocket created')
        return s
    except socket.error:
        print('\nFailed to create socket. Error: ' + socket.error)
        sys.exit()



def bindSocket(s):
    try:
        s.bind((host, port))
        print('\nBind socket')
    except socket.error:
        print('\nFailed to bind socket. Error: ' + socket.error)
        sys.exit()


 
# thread function
def threaded(clientSocket, addr):
    while True:
 
        # data received from client
        data = clientSocket.recv(1024)

        if not data:
            print('Bye')
            clientSocket.close()
            # lock released on exit
            break

        print("Receive data")
        print(data.decode())
 
        # reverse the given string from client
        data = data[::-1]
 
        # send back reversed string to client
        clientSocket.send(data)
 
    # connection closed
    clientSocket.close()
 
 
def Main():

    serverSocket = createSocket()
    bindSocket(serverSocket)
 
    serverSocket.listen()
    print("socket is listening")
 
    while True:
 
        # establish connection with client
        clientSocket, addr = serverSocket.accept()

        thread = Thread(target=threaded, args=(clientSocket, addr), daemon=True)
        thread.start()
 
 
if __name__ == '__main__':
    Main()
