import socket
import sys
from operator import itemgetter

TEST_FILE = "./clientFiles/comparando.txt"

port = 5000
host = "localhost"

TAM_SOCKET = 10050


def createSocket():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print('\nSocket created')
        return s
    except socket.error:
        print('\nFailed to create socket. Error: ' + socket.error)
        sys.exit()

def sendMessagesToServer(s):
        # pede ao usuário o nome do arquivo desejado
        text = input('\nEscreva o nome do arquivo que deseja acessar: ')
        msg = "GET " + text
        msg = msg.encode()

        # pede ao usuário se ele quer simular a perda de arquivo
        lost = input('\nDeseja simular a perda de dado(digite sim ou não)?')


        try:
            # envia requisição
            s.sendto(msg, (host, port))
            file = open(TEST_FILE, "a")
            rightSockets = []
            wrongSockets = []

            j = 0
            # começa as respostas do servidor
            while (1):
                receive = s.recv(TAM_SOCKET)
                receive = receive.decode()
                
                # caso o servidor tenha terminado de enviar os pacotes, finaliza
                if receive == "game over":
                    break
                # caso a requisição do usuário esteja errada, finaliza
                elif receive == "Formato de requisição não aceito" or receive == "Arquivo não encontrado":
                    print(receive)
                    sys.exit()

                # separa a resposta recebida em tamanho - numeração - dados
                res = receive.split("-///-")
                lenghtData = res[0]
                socketNumber = res[1]
                data = res[2]
                
                # caso queira simular a perda de pacotes, os dados recebidos são zerados
                if lost=="sim" and (j==0 or j==1):
                    data = ""
                    j = j+1

                # caso o tamanho dos dados recebidos não bata com tamanho que o servidor 
                # mandou, é guardado a numeração em uma lista de pacotes errados
                if len(data) != int(lenghtData):
                    wrongSockets.append(socketNumber)
                # caso os tamanhos batam, é guardado em uma lista de pacotes certos
                else:
                    rightSockets.append([int(socketNumber), data])
                

            # caso tenha pacotes errados, pede eles novamente
            if len(wrongSockets) > 0:
                # primeiro, é enviado as numerações dos pacotes errados para o servidor
                msg = wrongSockets[0]
                for i in range(1, len(wrongSockets)):
                    msg = msg + "," + wrongSockets[i]
                msg = msg.encode()
                s.sendto(msg, (host, port))

                # depois, é recebido os pacotes correspondentes
                for i in range(0, len(wrongSockets)):
                    receive = s.recv(TAM_SOCKET-50)
                    receive = receive.decode()
                    rightSockets.append([int(wrongSockets[i]), receive])

                #reordena os pacotes para serem adicionados ao arquivo
                rightSockets.sort(key=itemgetter(0))


            #caso contrário, manda um OK
            else:
                msg = "OK"
                msg = msg.encode()
                s.sendto(msg, (host, port))

            #escreve os dados no arquivo
            for i in range(0, len(rightSockets)):
                file.write(rightSockets[i][1])


            file.close()
            

        except socket.error:
            print(socket.error)
            sys.exit()



def main():
    socket = createSocket()
    sendMessagesToServer(socket)
    sys.exit

main()
