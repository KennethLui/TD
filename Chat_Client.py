from socket import *

#Se o nome do serverName for localhost então a conexão se limita a servidor e cliente do
#mesmo PC. Para se conectar de PCs diferentes o nome precisa ser o endereço do Servidor
serverName = 'localhost'
serverPort = 12000

#Cria o socket do cliente
clienteSocket = socket(AF_INET, SOCK_STREAM)
#Estabelece conexão TCP com servidor
clienteSocket.connect((serverName, serverPort))

mensagem = input('frase de mensagem do cliente: ')
clienteSocket.send(mensagem)

resposta_do_servidor=clienteSocket.recv(1024)
print ('Resposta do servidor: ', resposta_do_servidor)
clienteSocket.close()