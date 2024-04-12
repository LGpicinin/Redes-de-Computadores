import socket
import sys

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
        
        if not data:
            break

        data = data.decode()

        reply = 'Ok...' + data
        reply = reply.encode()

        s.sendto(reply, adress)


def main():
    socket = createSocket()
    bindSocket(socket)

    runServer(socket)

    socket.close()
    sys.exit()


main()