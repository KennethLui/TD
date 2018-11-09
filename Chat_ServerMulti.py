import time, _thread as thread

from socket import *

serverName = 'localhost'
serverPort = 12000

#Cria o socket do cliente
serverSocket = socket(AF_INET, SOCK_STREAM)
#Estabelece conexão TCP com servidor

#Associa o socket criado acima ao numero de porta
servidorSocket.bind((serverName,serverPort))

servidorSocket.listen(10)

def tempo():
    return time.ctime(time.time())

def lidacliente(conexao):
    time.sleep(5)

    while True:
        data = conexao.recv(1024)

        if not dado: break

        resposta = 'Eco==>%s as %s' % (data,tempo())

        conexao.send(resposta.encoder())

    conexao.close()

    def despacha():
        while True:
            conexao, endereco = serverSocket.accept()
            print('Server conectado por', endereco, end='')
            print('as',tempo())

            thread.start_new_thread(lidacliente,(conexao,))