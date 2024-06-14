import socket
import sys
import os
import time
from hashlib import md5
from threading import Thread
 

TEST_FILE = './serverFiles/teste.txt'
NAMES_FILE = './serverFiles/names.txt'
PATH = './serverFiles/'

PORT = 5000
HOST = "localhost"


# cria socket
def createSocket():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('\nSocket created')
        return s
    except socket.error:
        print('\nFailed to create socket. Error: ' + socket.error)
        sys.exit()

# anexa socket a uma porta
def bindSocket(s):
    try:
        s.bind((HOST, PORT))
        print('\nBind socket')
    except socket.error:
        print('\nFailed to bind socket. Error: ' + socket.error)
        sys.exit()


def getCheckSumAndLength(file):

    # começa a ler o arquivo e inicia hash
    data = file.read(1000)
    check = md5()
    length = 0

    # enquanto tiver dados no arquivo para ler
    while data:
        # atualiza hash e aumenta número de pacotes
        check.update(data)
        length = length + 1
        data = file.read(1000)

    # retorna a hash e o número de pacotes
    return check.hexdigest(), length


def optionArq(socket, dataList):

    fileName = dataList[1]

    fileToOpen = PATH + fileName


    # verifica se arquivo o requisitado existe
    if not os.path.exists(fileToOpen):
        msg = "NOT FOUND"
        msg = msg.encode()
        socket.send(msg)
        return
    
    # abre arquivo
    file = open(fileToOpen, "rb")

    # calcula hash de todo o arquivo e também o número de pacotes que serã enviados
    check, numberPackets = getCheckSumAndLength(file)

    # envia as informações calculadas
    dataToSend = check + " " + str(numberPackets)
    socket.send(dataToSend.encode())

    time.sleep(0.1)

    # abre o arquivo novamente e começa a ler
    file = open(fileToOpen, "rb")
    data = file.read(1000)

    # enquanto tiver dados no arquivo para ler
    while data:
        
        # calcula hash da parte que será enviada
        hashServer = md5(data).digest()

        # monta mensagem
        dataToSend = b" ".join([hashServer, data])

        # envia mensagem e recebe o retorno do cliente
        socket.send(dataToSend)
        res = socket.recv(1024)

        # se a hash tiver falhado, envia de novo até dar certo
        while res.decode() == "NOK":
            hashServer = md5(data).digest()
            dataToSend = b" ".join([hashServer, data])
            socket.send(dataToSend)
            res = socket.recv(1024)

        # continua lendo o arquivo
        data = file.read(1000)

        if not data:
            time.sleep(0.1)




def optionChat(socket, threadNumber):

    threadNumber = str(threadNumber)

    # recebe mensagem e decodifica
    message = socket.recv(1024)
    message = message.decode()

    # enquanto mensagem não for ADEUS 
    while message!="ADEUS":

        # imprime mensagem e manda a do server
        print("\nUsuário " + threadNumber + ":\n" + message)
        print("\nServer respondendo " + threadNumber + ": ")
        message = input()
        socket.send(message.encode())

        # recebe mensagem e decodifica
        message = socket.recv(1024)
        message = message.decode()


 
# função principal que roda na thread
def threaded(clientSocket, threadNumber):
    while True:
 
        # recebe mensagem e decodifica
        data = clientSocket.recv(1024)
        data = data.decode()
        dataList = data.split(" ")

        if dataList[0] == "Sair":
            clientSocket.close()
            break

        elif dataList[0] == "Arquivo":
            optionArq(clientSocket, dataList)

        elif dataList[0] == "Chat":
            optionChat(clientSocket, threadNumber)


 
 
 
def Main():

    # cria socket e começa a ouvir porta
    serverSocket = createSocket()
    bindSocket(serverSocket)
 
    serverSocket.listen()
    print("socket is listening")
    i = 0

    while True:
            
        # aceita requisição do cliente
        clientSocket, addr = serverSocket.accept()

        # cria thread pro cliente e inicia função principal
        thread = Thread(target=threaded, args=(clientSocket, i), daemon=True)
        thread.start()
        i = i+1
 
 
if __name__ == '__main__':
    Main()
