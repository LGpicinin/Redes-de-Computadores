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

def sendMessagesToServer(s):
    while(1):
        msg = input('\nEnter message to send: ')
        msg = msg.encode()

        try:
            s.sendto(msg, (host, port))

            data, adress = s.recvfrom(1024)
            
            print('\nServer reply: ')
            print(data)

        except socket.error:
            print(socket.error)
            sys.exit()



def main():
    socket = createSocket()
    sendMessagesToServer(socket)
    sys.exit

main()
