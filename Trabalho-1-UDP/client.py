import socket
import sys

TEST_FILE = "./clientFiles/outroTeste.txt"

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
 
        msg = input('\nEnter message to send: ')
        msg = msg.encode()

        try:
            s.sendto(msg, (host, port))


            receive = open(TEST_FILE, "a")

            while (1):
                data = s.recv(1024)
                data = data.decode()
                if(data == "game over"):
                    break
                receive.write(data)

            receive.close()
            
            #print('\nServer reply: ')
            #print(data)

        except socket.error:
            print(socket.error)
            sys.exit()



def main():
    socket = createSocket()
    sendMessagesToServer(socket)
    sys.exit

main()
