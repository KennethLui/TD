from socket import *

serverName = 'localhost'

#Numero de porta escolhida de acordo com o exemplo fornecido no livro
serverPort = 12000

servidorSocket = socket(AF_INET, SOCK_STREAM)
#AF_INET significa que o protcolo de endereço IP
#SOCK_STREAM significa que o protocolo de transferencia é TCP
#Entao o servidor é TCP/IP

#Associa o socket criado acima ao numero de porta
servidorSocket.bind((serverName,serverPort))

#10 conexoes por vez
servidorSocket.listen(10)

print ('Servidor escutando')

while 1:
    #aceita a conexao a cria um novo socket para conexao com cliente. É estabelecido uma conexão TCP
    socket_de_conexao, endereco = servidorSocket.accept()
    print ('Servidor conectado ao endereço',  endereco)

    while True:
        #Recebe os 2014 bytes de informação
        dados = socket_de_conexao.recv(1024)

        #Quando nao houver mais dados o loop é quebrado
        if not dados:break

        resposta = dados.upper()
        socket_de_conexao.send(resposta)

    #Fecha a conexão do socket_de_conexão
    print('Encerrando conexão')
    socket_de_conexao.close()