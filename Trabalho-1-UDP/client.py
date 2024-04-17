import socket
import sys
from operator import itemgetter

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
 
        text = input('\nEscreva o nome do arquivo que deseja acessar: ')
        msg = "GET " + text
        msg = msg.encode()

        lost = input('\nDeseja simular a perda de dado(digite sim ou não)?')


        try:
            s.sendto(msg, (host, port))
            file = open(TEST_FILE, "a")
            rightSockets = []
            wrongSockets = []

            j = 0
            while (1):
                receive = s.recv(1050)
                receive = receive.decode()

                if receive == "game over":
                    break
                elif receive == "Formato de requisição não aceito" or receive == "Arquivo não encontrado":
                    print(receive)
                    sys.exit()

                res = receive.split("-///-")

                lenghtData = res[0]
                socketNumber = res[1]
                data = res[2]

                if lost=="sim" and (j==0 or j==1):
                    data = ""
                j = j+1

                if len(data) != int(lenghtData):
                    wrongSockets.append(socketNumber)
                else:
                    rightSockets.append([int(socketNumber), data])
                

            if len(wrongSockets) > 0:
                msg = wrongSockets[0]
                for i in range(1, len(wrongSockets)):
                    msg = msg + "," + wrongSockets[i]
                msg = msg.encode()
                s.sendto(msg, (host, port))
                for i in range(0, len(wrongSockets)):
                    receive = s.recv(1024)
                    receive = receive.decode()
                    rightSockets.append([int(wrongSockets[i]), receive])

                rightSockets.sort(key=itemgetter(0))

            else:
                msg = "OK"
                msg = msg.encode()
                s.sendto(msg, (host, port))

            for i in range(0, len(rightSockets)):
                file.write(rightSockets[i][1])


                    


            file.close()
            
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
