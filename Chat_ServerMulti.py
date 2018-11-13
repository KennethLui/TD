import time, _thread as thread

from socket import *

serverName = 'localhost'
serverPort = 12000

#Cria o socket do cliente
serverSocket = socket(AF_INET, SOCK_STREAM)
#Estabelece conexão TCP com servidor

#Associa o socket criado acima ao numero de porta
serverSocket.bind((serverName,serverPort))

serverSocket.listen(10)

clientes={}

def buscar():

def entrar():

def criar():

def apagar():

def menu(conexao):
    msg = 'Menu:\n1 - Buscar informações sobre as salas\n2 - Entrar em e sair de uma sala existente\n3 - Criação de salas públicas e privadas\n4 - Apagar salas\n5 - Sair e desligar o servidor\n\nOpção: '
    erro = 'Resposta inválida. Escolha uma das opções de 1 a 5\n\nOpção: '
    sair = 'sair'
    conexao.send(msg.encode())
    flag = True
    while flag = True
        resposta = conexao.recv(1024)
        if resposta == 1:
            buscar()
            flag = False
        elif resposta == 2:
            entrar()
            flag = False
        elif resposta == 3:
            criar()
            flag = False
        elif resposta == 4:
            apagar()
            flag = False
        elif resposta == 5:
            conexao.send(sair.encode())
            flag = False
        else:
            conexao.send(erro.encode())

def tempo():
    return time.ctime(time.time())

def cadastro(conexao,endereco):
    cadastrado = False
    while not cadastrado:
        msg1 = 'Já possui cadastro?\n1 - Sim\n2 - Não\n\nResposta: '
        msg2 = 'Digite o apelido desejado\nApelido: '
        msg3 = 'Cadastro efetuado'
        msg4 = 'Noma já cadastrado'
        msg5 = 'Realizar cadastro'
        conexao.send(msg1.encode())

        resposta = conexao.recv(1024)

        if resposta==1:
            cadastrado = True
        else:
            print('Resposta de cadastro ainda não efetuado')
            cadastrado = True
            conexao.send(msg5.encode())
            conexao.send(msg2.encode())
            resposta = conexao.recv(1024)
            clientes.update({endereco:resposta.decode('utf-8')})
            conexao.send(msg3.encode())

def lidacliente(conexao, endereco):
    time.sleep(5)
    cadastro(conexao,endereco)
    print('Saiu do cadastro')
    msg_sair = 'sair'
    while True:
        dado = conexao.recv(1024)

        if not dado: break

        if "sair" in str(dado):
            conexao.send(msg_sair.encode())
            break

        resposta = 'Eco==>%s as %s' % (dado,tempo())

        conexao.send(resposta.encode())

    print('Fechando conexão com', endereco)
    conexao.close()

    print('Lista de clientes: ')
    #for addr in clientes:
    #    print (addr)

    print(clientes.items())

def despacha():

    print ('Servidor rodando')
    while True:
        conexao, endereco = serverSocket.accept()
        print('Server conectado por', endereco, end='')
        print('as',tempo())

        #if endereco not in clientes:
        #    clientes.append(endereco)

        thread.start_new_thread(lidacliente,(conexao,endereco,))

despacha()