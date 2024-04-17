import socket
import sys
import math
import os
from time import sleep

TEST_FILE = './serverFiles/teste.txt'
NAMES_FILE = './serverFiles/names.txt'
PATH = './serverFiles/'

port = 5000
host = "localhost"

TAM_SOCKET = 10000


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
        # recebe requisição do cliente
        data, adress = s.recvfrom(1024)
        print("Nova requisição de cliente")
        
        if not data:
            break

        data = data.decode()
        data = data.split(" ")

        # verifica se o formato é válido
        if data[0] != "GET":
            msg = "Formato de requisição não aceito"
            msg = msg.encode()
            s.sendto(msg, adress)
            continue

        fileToOpen = ""
        fileToOpen = PATH + data[1]


        # verifica se arquivo o requisitado existe
        if not os.path.exists(fileToOpen):
            msg = "Arquivo não encontrado"
            msg = msg.encode()
            s.sendto(msg, adress)
            continue

        # abre o arquivo requisitado
        file = open(fileToOpen, "rt")
        i = 1
        dataToSend = file.read(TAM_SOCKET)


        # começa a enviar o arquivo
        print("Enviando sockets")
        while dataToSend:
            lenght = str(len(dataToSend))
            socketNumber = str(i)

            # envia no formato: tamanho - numeração - dados
            reply = lenght + "-///-" + socketNumber + "-///-" + dataToSend
            reply = reply.encode()

            s.sendto(reply, adress)
            dataToSend = file.read(TAM_SOCKET)
            i = i + 1
        
        # envia uma mensagem para avisar que acabou de enviar
        sleep(1)
        finalMessage = 'game over'
        s.sendto(finalMessage.encode(), adress)

        

        # recebe uma mensagem de verificação do cliente para saber se tudo está certo
        data, adress = s.recvfrom(1024)
        data = data.decode()
        # se está certo, recebe um OK
        if data == "OK":
            print("Envio realizado com sucesso \n\n")
        
        # se não, recebe uma lista de números que representam os sockets
        # que não chegaram ao cliente corretamente
        else:
            print("\nReenvio de arquivos necessário")
            file = open(fileToOpen, "rt")
            if not file:
                print("Erro ao abrir arquivo")
                sys.exit()

            data = data.split(",")
            dataLenght = len(data)
            j = 0
            i = 1
            reply = file.read(TAM_SOCKET)
            while j<dataLenght:
                if int(data[j]) == i:
                    #print(reply)
                    s.sendto(reply.encode(), adress)
                    j = j + 1
                reply = file.read(TAM_SOCKET)
                i = i + 1
            print("Finalizando reenvio de arquivos \n\n")

        file.close()




def main():
    socket = createSocket()
    bindSocket(socket)

    runServer(socket)

    socket.close()
    sys.exit()


main()