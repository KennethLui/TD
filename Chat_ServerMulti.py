import time, _thread as thread
from sala import sala
from socket import *

serverName = 'localhost'
serverPort = 12000

#Cria o socket do cliente
serverSocket = socket(AF_INET, SOCK_STREAM)
#Estabelece conexão TCP com servidor

#Associa o socket criado acima ao numero de porta
serverSocket.bind((serverName,serverPort))

serverSocket.listen(10)

#Dicionario que salva os enderecos e nomes dos clientes
clientes={}

#Vetor que salva os usuarios na sala, onde
# o primeiro elemento é o nome da sala
#sala=[]

#Vetor que salva objetos criados para cada sala existente
lista_salas=[]

mostra_salas={}

dic = {}

def buscar_sala(conexao):
    msg = '\nSalas disponíveis:\n'
    msg_espera = '\nApera em qualquer tecla e pressione enter para continuar\n'
    conexao.send(msg.encode())
    for k in lista_salas:
        #mostra_salas[k.get_nome()] = {k.get_num_usuarios,k.get_privado}
        #dic = {k.get_nome():k.get_num_usuarios()}
        dic.setdefault(k.get_nome(),[]).append(k.get_num_usuarios())
        dic.setdefault(k.get_nome(),[]).append(k.get_privado())
        #print ('\nKey:',k.get_nome(),'\tValor: ',dic.get(k.get_nome()))
        mostra_salas.update(dic)
        #v = mostra_salas
        #print(v)

    #print('\nMostrando tabela de usuarios')

    for k in mostra_salas:
        v = mostra_salas[k]
        #print(k,'\t',v)
        if v[1] == True:
            tipo = 'Privado'
        else:
            tipo = 'Pública'
        printado = ''
        printado = '!' + str(k) + '\t' + 'Número de usuários: ' + str(v[0]) + '\tTipo de sala: ' + tipo + '\n'
        conexao.send(printado.encode('utf-8'))

    conexao.send(msg_espera.encode())
    espera = conexao.recv(1024)

def entrar_sala(conexao,endereco):
    msg = '!\nSalas disponíveis:\n'
    msg_op = '\nDigite a opção da sala desejada: '
    msg_senha = '\nDigite a senha da sala: '
    msg_senha_incorreta = '\nSenha incorreta\n'
    cont=0
    conexao.send(msg.encode())
    for k in mostra_salas:
        printado = '!Sala ' + str(cont) + ': ' + str(k) + '\n'
        conexao.send(printado.encode('utf-8'))
        cont = cont+1

    time.sleep(0.5)
    #Sala1.get_usuarios(clientes)
    conexao.send(msg_op.encode('utf-8'))
    time.sleep(2)
    op = conexao.recv(1024).decode('utf-8')

    it = lista_salas[int(op)]
    #VERIFICAR SE TEM SENHA E PEDIR SE TIVER

    privado = it.get_privado()
    senha = it.get_senha()

    if privado == True:
        #print(it.get_senha())
        conexao.send(msg_senha.encode())
        passw = conexao.recv(1024)
        if passw == senha:
            it.add_user(endereco,clientes)
        else:
            conexao.send(msg_senha_incorreta.encode())
    else:
        it.add_user(endereco,clientes)


def criar_sala(conexao,endereco):
    msg_nome_sala = '\nFunção CRIAR SALA\n\nDigite o nome da sala:\nNome: '
    msg_privada = '\nEsta sala deve ser privada?\n1 - Sim\n2 - Não\nOpção: '
    msg_erro = '\nOpção inválida\nEscolha uma das opções:\n1 - Sim\n2 - Não\nOpção: '
    msg_senha = '\nDefina uma senha:\nSenha: '
    msg_confirmacao = '!\nSala criada com sucesso!\n'

    conexao.send(msg_nome_sala.encode())
    nome_sala=conexao.recv(1024).decode('utf-8')

    loop = True

    conexao.send(msg_privada.encode())

    while loop == True:
        resposta = conexao.recv(1024).decode('utf-8')
        if resposta == '1':
            privada = True
            loop = False
            conexao.send(msg_senha.encode())
            senha=conexao.recv(1024)
            sala_nova = sala(nome_sala,endereco,privada,senha)
            conexao.send(msg_confirmacao.encode('utf-8'))
            time.sleep(0.5)

        elif resposta == '2':
            privada = False
            loop = False
            sala_nova = sala(nome_sala,endereco)
            conexao.send(msg_confirmacao.encode('utf-8'))
            time.sleep(0.5)
        else:
            conexao.send(msg_erro.encode())
    
    lista_salas.append(sala_nova)

def apagar_sala():
    return

def menu(conexao,endereco):
    msg = '\n\nMenu:\n1 - Buscar informações sobre as salas\n2 - Entrar em e sair de uma sala existente\n3 - Criação de salas públicas e privadas\n4 - Apagar salas\n5 - Sair e desligar o servidor\n\nOpção: '
    erro = '!Resposta inválida. Escolha uma das opções de 1 a 5\n\n'
    sair = 'quit'
    flag = False
    print('\nPassou pelo menu\n')
    while not flag:
        print('\nEntrou no loop do menu\nEsperando Escolha do usuario')
        conexao.send(msg.encode())
        resposta = conexao.recv(1024).decode('utf-8')
        if resposta == '1':
            print('\nEntrou na Função Buscar Sala\n')
            buscar_sala(conexao)

        elif resposta == '2':
            print('\nEntrou na Função Entrar Sala\n')
            entrar_sala(conexao,endereco)

        elif resposta == '3':
            print('\nEntrou na Função Criar Sala\n')
            criar_sala(conexao,endereco)

        elif resposta == '4':
            print('\nEntrou na Função Apagar Sala\n')
            apagar_sala()

        elif resposta == '5':
            print('\nEntrou na Função Sair\n')
            conexao.send(sair.encode())
            flag = True
        else:
            conexao.send(erro.encode())

def tempo():
    return time.ctime(time.time())

def cadastro(conexao,endereco):
    cadastrado = False
    while not cadastrado:
        msg1 = 'Já possui cadastro?\n1 - Sim\n2 - Não\n\nResposta: '
        msg2 = '\nDigite o apelido desejado\nApelido: '
        msg3 = '\nCadastro efetuado\n'
        msg4 = '\nNoma já cadastrado\n'
        msg5 = '\nRealizar cadastro\n'
        conexao.send(msg1.encode())

        resposta = conexao.recv(1024).decode('utf-8')
        print('\nResposta recebida do usuário: ',resposta)
        if resposta=='1':
            cadastrado = True
        elif resposta=='2':
            print('Resposta de cadastro ainda não efetuado')
            cadastrado = True
            conexao.send(msg5.encode())
            conexao.send(msg2.encode())
            resposta = conexao.recv(1024)
            clientes.update({endereco:resposta.decode('utf-8')})
            conexao.send(msg3.encode())
        else:
            print('\nOpção inválida')

def lidacliente(conexao, endereco):
    time.sleep(5)
    cadastro(conexao,endereco)
    print('Saiu do cadastro')
    msg_sair = 'quit'
    menu(conexao,endereco)
    print ('\nSaiu do Menu')
    while True:
        dado = conexao.recv(1024)

        if not dado: break

        if "quit" in str(dado):
            conexao.send(msg_sair.encode())
            break

        resposta = 'Eco==>%s as %s' % (dado,tempo())

        conexao.send(resposta.encode())

    print('Fechando conexão com', endereco)
    conexao.close()

    print('Lista de clientes: ')
    print ("{:<24} {:<15}".format('Endereço','Apelido'))
    for endereco,nome in clientes.items():
        #print ("{:<15} {:<15}".format(k, clientes[k]))
        print(endereco,'\t',nome)
    #print(clientes.items())

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