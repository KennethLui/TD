import socketserver, time

serverName = 'localhost'
serverPort = 12000

def agora():
    return time.ctime(time.time())

class LidaComCliente(socketserver.BaseRequestHandler):
    def handle(self):

        #imprime a identificação do cliente e o tempo
        print(self.client_address,agora())

        time.sleep(5)

        while True:
            #Recebe a data do cliente
            infodata = self.request.recv(1024)
            if not infodata: break

            resposta = 'Eco=>%s as %s' % (infodata,agora())
            self.request.send(resposta.encode())
        self.request.close()

meuendrç = (serverName, serverPort)
server = socketserver.ThreadingTCPServer(meuendrç,LidaComCliente)
server.serve_forever()