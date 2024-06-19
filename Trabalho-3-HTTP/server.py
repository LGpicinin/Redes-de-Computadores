import socket
import sys
import os
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


def getLength(file):

    # começa a ler o arquivo
    data = file.read(1000)
    length = 0

    # enquanto tiver dados no arquivo para ler
    while data:

        length = length + 1000
        data = file.read(1000)

    file.close()
    return length


def enviaResposta(socket, fileName, message):

    file = open(PATH + fileName, "rb")
    length = getLength(file)
    file = open(PATH + fileName, "rb")

    contentType = "Content-Type: text/html; charset=UTF-8\r\n"
    data = file.read(length)

    # monta mensagem
    length = str(len(data))
    contentLength = "Content-Length: " + length + "\r\n\r\n"
    header = message + contentType + contentLength
    dataToSend = b"".join([header.encode(), data])
    # envia mensagem
    socket.send(dataToSend)
    file.close()



def abreArq(socket, dataList):

    fileName = dataList.split("/")
    fileToOpen = PATH + fileName[1]


    # verifica se arquivo o requisitado existe
    if not os.path.exists(fileToOpen):

        enviaResposta(socket, "notFound.html", "HTTP/1.1 404 Not Found\r\n")
        return
    

    enviaResposta(socket, fileName[1], "HTTP/1.1 200 OK\r\n")
    

 
# função principal que roda na thread
def threaded(clientSocket, threadNumber):
        
    # recebe mensagem e decodifica
    data = clientSocket.recv(1024)
    data = data.decode()
    print("Recebendo requisição da thread " + str(threadNumber))
    lines = data.split("\n")
    line1 = lines[0].split(" ")

    if line1[0] == "GET":
        abreArq(clientSocket, line1[1])
    
    else:
        message = "HTTP/1.1 400 Bad Request"
        clientSocket.send(message.encode())

    clientSocket.close()

 
 
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
