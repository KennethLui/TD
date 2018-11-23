class sala:

    def __init__(self,name,endereco,private=None):
        self.nome = name
        self.usuarios = [endereco]
        if private==None:
            self.privado = False
        else:
            self.privado = True
            self.senha=input('\nDefina uma senha\nSenha: ')
            print('\nSenha definida: ',self.senha)
        print ('\nSala criada!')
        
    def get_nome(self):
        print('\nNome da sala: ',self.nome)

    def get_usuarios(self,clientes):
        print('\nLista de usuários na sala:\n')
        for k in self.usuarios:
            print(clientes.get(k))

    def get_privado(self):
        if self.privado == False:
            return False
        else:
            return True

    def add_user(self,endereco,clientes):
        self.usuarios.append(endereco)
        print ('\nUsuário ',clientes.get(endereco),' adicionado à sala')

    def del_user(self,endereco,clientes):
        if self.usuarios.count(endereco) == 0:
            print('\nEste não está na sala')
        else:
            self.usuarios.remove(endereco)
            print ('\nUsuário ',clientes.get(endereco),' removido da sala')