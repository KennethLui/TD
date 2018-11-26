from socket import *
import os
import time

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
        #print('\nSem resposta\n')
        print(resposta_do_servidor[1:].decode('utf-8'))
    elif resposta_do_servidor.decode('utf-8') == '#SEND_FILE#':
        filename = input('\nDigite o nome do arquivo,incluindo a extenção: ')
        if os.path.isfile(filename):
            print ('\nEntrou\n')
            clienteSocket.send(filename.encode('utf-8'))
            time.sleep(0.5)
            tamanho = str(os.path.getsize(filename))
            print (tamanho)
            clienteSocket.send(tamanho.encode('utf-8'))
            time.sleep(0.5)
            with open(filename,'rb') as f:
                print('\nEntrou 2')
                bytes_para_mandar = f.read(1024)
                clienteSocket.send(bytes_para_mandar)
                time.sleep(0.5)
                while(bytes_para_mandar!=''):
                    #print('\nEntrou 3')
                    bytes_para_mandar = f.read(1024)
                    clienteSocket.send(bytes_para_mandar)
                    time.sleep(0.5)

    else:
        #print('\nDigite resoista')
        resposta_do_usuario =input(resposta_do_servidor.decode('utf-8'))
        clienteSocket.send(resposta_do_usuario.encode('utf-8'))


clienteSocket.close()