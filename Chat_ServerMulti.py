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

#Diciomario que salva o socket para cada endereço
socket_clientes = {}

#Vetor que salva os usuarios na sala, onde
# o primeiro elemento é o nome da sala
#sala=[]

#Vetor que salva objetos criados para cada sala existente
lista_salas=[]

mostra_salas={}

dic = {}

def atualiza_mostra_salas():
    mostra_salas.clear()
    for k in lista_salas:
        dic = {}
        dic.setdefault(k.get_nome(),[]).append(k.get_num_usuarios())
        dic.setdefault(k.get_nome(),[]).append(k.get_privado())
        mostra_salas.update(dic)

def buscar_sala(conexao):
    msg = '\nSalas disponíveis:\n'
    #msg_espera = '\nApera em qualquer tecla e pressione enter para continuar\n'
    conexao.send(msg.encode())
    #for k in lista_salas:
    #    dic = {}
    #    dic.setdefault(k.get_nome(),[]).append(k.get_num_usuarios())
    #    dic.setdefault(k.get_nome(),[]).append(k.get_privado())
    #    mostra_salas.update(dic)

    atualiza_mostra_salas()

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
        print ('\nstrV0 é: ',str(v[0]),' V[0] é: ',v[0])

    #conexao.send(msg_espera.encode())
    #espera = conexao.recv(1024)

def entrar_sala(conexao,endereco):
    msg = '!\nSalas disponíveis:\n'
    msg_op = '\nDigite a opção da sala desejada: '
    msg_senha = '\nDigite a senha da sala: '
    msg_senha_incorreta = '!\nSenha incorreta\n'
    msg_boas_vindas = '!\nVocê agora está na sala: '
    msg_digite = '\nDigite uma mensagem(para sair digite "sair"): '
    msg_despedida = '!\nVocê saiu da sala\n'
    cont=0
    conexao.send(msg.encode())
    time.sleep(0.5)

    atualiza_mostra_salas()

    for k in mostra_salas:
        printado = '!Opção ' + str(cont) + ': ' + str(k) + '\n'
        conexao.send(printado.encode('utf-8'))
        time.sleep(0.5)
        cont = cont+1

    time.sleep(0.5)
    #Sala1.get_usuarios(clientes)
    conexao.send(msg_op.encode('utf-8'))
    time.sleep(2)
    op = conexao.recv(1024).decode('utf-8')

    it = lista_salas[int(op)]
    #VERIFICAR SE TEM SENHA E PEDIR SE TIVER

    privado = it.get_privado()
    if it.get_senha() != None:
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

    it.get_usuarios(clientes)

    conexao.send((msg_boas_vindas+it.get_nome()).encode())
    time.sleep(0.5)
    msg_tipo = '\nO que deseja enviar?\n1 - Arquivo\n2 - Mensagem\nOpção: '
    msg_filename = '\nDigite o nome do arquivo, incluindo a extenção: '
    msg_SENDFILE = '#SEND_FILE#'
    msg_RECVFILE = '#RECV_FILE#'
    while True:
        conexao.send(msg_tipo.encode())
        time.sleep(0.5)
        resposta = conexao.recv(1024).decode('utf-8')

        if resposta == '1':
            conexao.send(msg_SENDFILE.encode())
            filename = conexao.recv(1024).decode()
            tamanho = conexao.recv(1024).decode()
            print(filename,'  ',tamanho)
            f = open('novo_'+filename,'wb')
            dados = conexao.recv(1024)
            total_recebido = len(dados)
            f.write(dados)
            while total_recebido < int(tamanho):
                print('\nDADO RECEBIDO')
                dados = conexao.recv(1024)
                total_recebido += len(dados)
                f.write(dados)
            print('\nDownload completo\nComeçando o envio...\n')

        else:
            conexao.send(msg_digite.encode())
            mensagem = conexao.recv(1024).decode('utf-8')
            time.sleep(0.5)

            if mensagem == 'sair':
                break

            usuarios = it.get_vet_usuarios()

            for k in usuarios:
                broadcast_msg = socket_clientes.get(k)
                broadcast_msg.send((mensagem+'\n').encode())

    conexao.send(msg_despedida.encode())
    time.sleep(0.5)
    it.del_user(endereco,clientes)

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
            sala_nova = sala(nome_sala,privada,senha)
            conexao.send(msg_confirmacao.encode('utf-8'))
            time.sleep(0.5)

        elif resposta == '2':
            privada = False
            loop = False
            sala_nova = sala(nome_sala)
            conexao.send(msg_confirmacao.encode('utf-8'))
            time.sleep(0.5)
        else:
            conexao.send(msg_erro.encode())
    
    lista_salas.append(sala_nova)

def apagar_sala(conexao):
    msg_opcoes = '!\nSalas existentes:\n'
    msg_op = '\nDigite a opção da sala que deseja apagar(O número de usuários precisa ser 0): '
    msg_erro_num = '!\nO número de usuários não é 0\n'
    time.sleep(0.5)

    atualiza_mostra_salas()

    while True:
        conexao.send(msg_opcoes.encode())
        cont = 0
        for k in mostra_salas:
            v = mostra_salas[k]
            printado = ''
            printado = '!Opção ' + str(cont) + ' :' + str(k) + '\t' + 'Número de usuários: ' + str(v[0]) + '\n'
            conexao.send(printado.encode('utf-8'))
            time.sleep(0.5)
            cont = cont+1

        time.sleep(0.5)

        conexao.send(msg_op.encode('utf-8'))
        time.sleep(0.5)
        op = conexao.recv(1024).decode('utf-8')

        it = lista_salas[int(op)]

        if it.get_num_usuarios == 0:
            conexao.send(msg_erro_num.encode())
        else:
            print ('\nSala ',it.get_nome(),' apagada')
            msg_apagar = '!\nSala ' + it.get_nome() + ' apagada\n'
            conexao.send(msg_apagar.encode())
            time.sleep(0.5)
            lista_salas.remove(it)
            atualiza_mostra_salas()

            for p in lista_salas:
                print ('\n',p.get_nome())

            break

def menu(conexao,endereco):
    time.sleep(1)
    msg = '\n\nMenu:\n1 - Buscar informações sobre as salas\n2 - Entrar em e sair de uma sala existente\n3 - Criação de salas públicas e privadas\n4 - Apagar salas\n5 - Sair e desligar o servidor\n\nOpção: '
    msg_espera = '\nPressione qualquer tecla e em seguida pressione enter para continuar\n'
    erro = '!Resposta inválida. Escolha uma das opções de 1 a 5\n\n'
    sair = 'quit'
    flag = False
    print('\nPassou pelo menu\n')
    while not flag:
        print('\nEntrou no loop do menu\nEsperando Escolha do usuario')
        conexao.send(msg_espera.encode())
        espera = conexao.recv(1024)
        time.sleep(0.5)
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
            apagar_sala(conexao)

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
        msg3 = '!\nCadastro efetuado\n'
        msg4 = '\nNoma já cadastrado\n'
        msg5 = '!\nRealizar cadastro\n'
        msg6 = '\nQual o seu apelido: '
        msg7 = '!\nNome não encontrado\n'
        
        conexao.send(msg1.encode())
        resposta = conexao.recv(1024).decode('utf-8')
        print('\nResposta recebida do usuário: ',resposta)
        if resposta=='1':
            conexao.send(msg6.encode())
            resposta = (conexao.recv(1024)).decode('utf-8')
            resposta = resposta.upper()
            for subst,nome in clientes.values():
                if nome == resposta:
                    clientes.pop(subst)
                    clientes.update({endereco:resposta})
                    cadastrado = True
                else:
                    conexao.send(msg7.encode())
                    time.sleep(0.5)
        elif resposta=='2':
            print('Resposta de cadastro ainda não efetuado')
            cadastrado = True
            conexao.send(msg5.encode())
            time.sleep(1)
            conexao.send(msg2.encode())
            resposta = conexao.recv(1024).decode('utf-8')
            resposta = resposta.upper()
            #Salva o endereço e apelido
            clientes.update({endereco:resposta})
            #Salva o endereço e o socket
            socket_clientes.update({endereco:conexao})
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