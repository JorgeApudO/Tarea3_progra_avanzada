import socket
from threading import Thread
from random import choice

class ServerEspera():
    
    def __init__(self):

        #Pasar a parametros
        IP_SERVER=socket.gethostname()
        PUERTO_SERVER_ESPERA=2100

        print("Se ha iniciado la sección de espera del server")

        self.socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_servidor.bind((IP_SERVER, PUERTO_SERVER_ESPERA))
        self.socket_servidor.listen()
        self.clientes = {}
        self.admin=None
        self.recibiendo=True
        self.colores=["rojo", "azul", "amarillo", "verde"]

        thread_recibir_clientes = Thread(target=self.recibir_clientes, daemon=True)
        thread_recibir_clientes.start()


    def recibir_clientes(self):
        
        while self.recibiendo:

            #Citar esto, ayudantia 8

            info_cliente = self.socket_servidor.accept()
            socket_cliente = info_cliente[0]
            direccion = info_cliente[1]
            print(f'Cliente con dirección {direccion} se ha conectado al servidor de espera')
            thread_cliente = Thread(target=self.escuchar_cliente, args=(socket_cliente,))
            thread_cliente.daemon=True
            thread_cliente.start()
            pass

        pass


    def escuchar_cliente(self, socket_cliente):

        while self.recibiendo:

            largo_mensaje_bytes=socket_cliente.recv(6)

            largo_mensaje_int=int.from_bytes(largo_mensaje_bytes, byteorder="big")

            mensaje_byte=bytearray()

            while len(mensaje_byte)<largo_mensaje_int:
                mensaje_byte+=socket_cliente.recv(4096)

            mensaje_str=mensaje_byte.decode("utf-8")

            self.analizar_mensaje(mensaje_str, socket_cliente)


    def analizar_mensaje(self, mensaje, socket_cliente):
        

        if mensaje[0]=="I":
            
            color=choice(self.colores)
            self.colores.remove(color)

            info_cliente=mensaje[1:].split(",")
            
            info_jugador=[socket_cliente, info_cliente[1], len(self.clientes), color]
            self.clientes[info_cliente[0]]=info_jugador

            if self.admin==None:
                self.admin=info_cliente[0]


            enviar="jugadores,"

            for cliente in self.clientes:
                    
                enviar+=(f"{cliente};{self.clientes[cliente][3]},")

            enviar=enviar[:-1].encode("utf-8")
            largo=len(enviar).to_bytes(6, byteorder="big")
            
            for cliente in self.clientes:

                self.clientes[cliente][0].sendall(largo)
                self.clientes[cliente][0].sendall(enviar)

        elif mensaje[0]=="P":

            enviar="iniciar,"

            for x in self.clientes:
                        
                enviar+=(f"{x};{self.clientes[x][2]};{self.clientes[x][3]},")

            print("Se inicia una partida, estan los jugadores:")

            enviar=enviar[:-1].encode("utf-8")
            largo=len(enviar).to_bytes(6, byteorder="big")

            for cliente in self.clientes:

                print(cliente)
                self.clientes[cliente][0].sendall(largo)
                self.clientes[cliente][0].sendall(enviar)



                