import socket
import sys
from hashlib import md5
import os

PATH = "./clientFiles/"

port = 5000
host = "localhost"

# cria socket
def createSocket():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('\nSocket created')
        return s
    except socket.error:
        print('\nFailed to create socket. Error: ' + socket.error)
        sys.exit()

# Arquivo - roda até cliente receber todo o arquivo
def optionArq(socket):

    os.system('cls' if os.name == 'nt' else 'clear')

    # digita nome do arquivo e envia
    print("Digite o nome do arquivo desejado:")
    nomeArq = input()
    message = "Arquivo " + nomeArq
    socket.send(message.encode())

    # recebe retorno do servidor
    res = socket.recv(1024)
    res = res.decode()

    if res == "NOT FOUND":
        print("O arquivo requisitado não existe")
        print("\nAperte a tecla ENTER para continuar")
        input()
        return
    
    # caso de sucesso - divide resposta em número de pacotes e hash do arquivo
    resList = res.split(" ")
    numberPackets = int(resList[1])
    checkServer = resList[0]
    i = 0
    
    # abre arquivo e inicia hash do cliente
    file = open(PATH + nomeArq , "wb")
    checkClient = md5()


    while i<numberPackets:

        # recebe resposta e divide em hash e dados
        res = socket.recv(1024)
        hashServer = res[0:16]
        data = res[17:]

        # verifica se as hash são iguais e pede de novo até dar certo
        while md5(data).digest() != hashServer:
            message = "NOK"
            socket.send(message.encode())
            res = socket.recv(1024)
            hashServer = res[0:16]
            data = res[17:]
        
        # atualiza hash do cliente
        checkClient.update(data)
        
        # manda retorno positivo e escreve data no arquivo
        message = "OK"
        socket.send(message.encode())
        file.write(data)
        i = i + 1

    # verifica se hash cliente = hash server
    if checkClient.hexdigest() != checkServer:
        print("O arquivo não é confiável")

    print("\nAperte a tecla ENTER para continuar")

    input()

    file.close()


# Chat - Roda até cliente digitar ADEUS
def optionChat(socket):
    os.system('cls' if os.name == 'nt' else 'clear')

    print("Iniciando conversa com o servidor. Para encerrar, digite ADEUS:\n\n")

    print("Você: ")
    message = input()

    while message != "ADEUS":

        socket.send(message.encode())

        message = socket.recv(1024)

        print("\nChat:\n" + message.decode())
        
        print("\nVocê: ")
        message = input()

    socket.send(message.encode())


def Main():

    # cria socket e anexa a uma porta
    socket = createSocket()
    socket.connect((host,port))
 
    # enaquanto não for selecionada a opção de Sair
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')

        message = ""

        print("Selecione uma ação:\n1 - Sair\n2 - Receber arquivo\n3 - Chat")

        option = input()
        option = int(option)

        # Sair
        if option == 1:
            message = "Sair"
            socket.send(message.encode())
            socket.close()
            break
        
        # Arquivo
        elif option == 2:
            optionArq(socket)

        # Chat
        elif option == 3:
            message = "Chat"
            socket.send(message.encode())
            optionChat(socket)
        
        else:
            print("Opção inválida")
            continue
 
 
if __name__ == '__main__':
    Main()