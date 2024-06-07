import socket
import sys
from operator import itemgetter

TEST_FILE = "./clientFiles/comparando.txt"

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


def Main():

    s = createSocket()
    s.connect((host,port))
 
    # message you send to server
    message = "shaurya says geeksforgeeks"
    while True:
 
        # message sent to server
        s.send(message.encode())
 
        # message received from server
        data = s.recv(1024)
 
        # print the received message
        # here it would be a reverse of sent message
        print('Received from the server :',str(data.decode()))
 
        # ask the client whether he wants to continue
        ans = input('\nDo you want to continue(y/n) :')
        if ans == 'y':
            continue
        else:
            break
    # close the connection
    s.close()
 
if __name__ == '__main__':
    Main()