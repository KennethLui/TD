from sala import sala

clientes={}

x = {'277.277.277.277':'John'}
y = {'000.000.000.000':'Steve'}
z = {'111.111.111.111':'Rio'}
clientes.update(x)
clientes.update(y)
clientes.update(z)

print(clientes.items(),'\n')

privado = True
endereco = '277.277.277.277'
name = 'Salinha de bate papo'
Sala1 = sala(name,endereco,privado)
Sala1.get_nome()
Sala1.get_usuarios(clientes)
bool = Sala1.get_privado()
if bool == True:
    print('\nSala privada')
else:
    print('\nSala pública')

print(list(clientes.keys())[list(clientes.values()).index('Rio')])

Sala1.add_user(list(clientes.keys())[list(clientes.values()).index('Rio')],clientes)

print('\nNova lista de usuários depois de adicionar Rio:\n')
Sala1.get_usuarios(clientes)

print('\nNova lista depois de deleter Rio\n')
Sala1.del_user(list(clientes.keys())[list(clientes.values()).index('Rio')],clientes)
Sala1.get_usuarios(clientes)