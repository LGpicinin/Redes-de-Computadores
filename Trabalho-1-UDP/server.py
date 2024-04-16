import socket
import sys
import math


TEST_FILE = './serverFiles/teste.txt'
NAMES_FILE = './serverFiles/names.txt'

port = 5000
host = "localhost"


def createSocket():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
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


def runServer(s):
    while 1:
        data, adress = s.recvfrom(1024)

        s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024) 
        
        if not data:
            break

        data = data.decode()
        fileToOpen = ""

        if data == "GET teste.txt":
            fileToOpen = TEST_FILE

        else:
            fileToOpen = NAMES_FILE

        file = open(fileToOpen, "rt")
        if not file:
            print("Erro ao abrir arquivo")


        i = 0
        reply = file.read(1024)

        while reply:
            s.sendto(reply.encode(), adress)
            reply = file.read(1024)
                
        finalMessage = 'game over'
        s.sendto(finalMessage.encode(), adress)

        file.close()
        #numberOfSends = math.floor(replySize/(1024*64))
        #if replySize/(1024*64) - numberOfSends != 0:
        #   numberOfSends = numberOfSends + 1
        #numberOfSends = str(numberOfSends).encode()
        
        #if replySize/1024 < 64:
        #    s.sendto(reply, adress)

        #else:


        sys.exit()



        #s.sendto(reply, adress)


def main():
    socket = createSocket()
    bindSocket(socket)

    runServer(socket)

    socket.close()
    sys.exit()


main()