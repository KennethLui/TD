from socket import *

#Se o nome do serverName for localhost então a conexão se limita a servidor e cliente do
#mesmo PC. Para se conectar de PCs diferentes o nome precisa ser o endereço do Servidor
serverName = 'localhost'
serverPort = 12000

#Cria o socket do cliente
clienteSocket = socket(AF_INET, SOCK_STREAM)
#Estabelece conexão TCP com servidor
clienteSocket.connect((serverName, serverPort))

#mensagem = [b'Liruleibe',b'Totoro']

#for linha in mensagem:
#    clienteSocket.send(linha)

#    resposta_do_servidor=clienteSocket.recv(1024)
#    print ('Resposta do servidor: ', resposta_do_servidor.decode('utf-8'))

sair = False

while not sair:

    resposta_do_servidor=clienteSocket.recv(1024)
    
    if "quit" in str(resposta_do_servidor):
        sair = True
        break

    if resposta_do_servidor.decode('utf-8')[:1]=='!':
        print('\nSem resposta\n')
        print(resposta_do_servidor[1:].decode('utf-8'))
    else:
        print('\nDigite resoista')
        resposta_do_usuario =input(resposta_do_servidor.decode('utf-8'))
        clienteSocket.send(resposta_do_usuario.encode('utf-8'))


clienteSocket.close()