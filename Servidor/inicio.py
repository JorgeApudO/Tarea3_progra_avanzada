import socket
from threading import Thread


class ServerInicio():
    
    def __init__(self):

        #Pasar a parametros
        IP_SERVER=socket.gethostname()
        PUERTO_SERVER_INICIO=2000

        print("Se ha iniciado la sección del inicio del server")

        self.socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_servidor.bind((IP_SERVER, PUERTO_SERVER_INICIO))
        self.socket_servidor.listen()
        self.admin=None
        self.recibiendo=True
        self.clientes=[]

        thread_recibir_clientes = Thread(target=self.recibir_clientes, daemon=True)
        thread_recibir_clientes.start()


    def recibir_clientes(self):
        
        while self.recibiendo:

            #Citar esto, ayudantia 8

            info_cliente = self.socket_servidor.accept()
            socket_cliente = info_cliente[0]
            direccion = info_cliente[1]
            print(f'Cliente con dirección {direccion} se ha conectado al servidor de inicio')
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
     
        if mensaje[0]=="N":

            es_alfa=mensaje[1:].isalnum()
            largo_no_adecuado=len(mensaje[1:])>10 or len(mensaje[1:])<1
            nombre_repetido=mensaje[1:] in self.clientes

            if not es_alfa:

                enviar=("malo,no_alfa").encode("utf-8")
                print(f"Se ingresó {mensaje[1:]} como nombre de usuario pero no es valido")
                pass

            elif largo_no_adecuado:

                enviar=("malo,largo").encode("utf-8")
                print(f"Se ingresó {mensaje[1:]} como nombre de usuario pero no es valido")

            elif nombre_repetido:

                enviar=("malo,repetido").encode("utf-8")
                print(f"Se ingresó {mensaje[1:]} como nombre de usuario pero no es valido")

            else:

                enviar=("bueno,nada").encode("utf-8")
                print(f"Se ingresó {mensaje[1:]} como nombre de usuario y si es valido")

        elif mensaje[0]=="E":

            #Pasar a parametros
            MAXIMO_JUGADORES=4

            sala_llena= (len(self.clientes)==MAXIMO_JUGADORES)

            if sala_llena:

                enviar=("lleno,nada").encode("utf-8")

            else:

                no_hay_admin= self.admin==None
                ultimo_jugador= len(self.clientes)==MAXIMO_JUGADORES-1

                if no_hay_admin:

                    enviar=("entrar,admin").encode("utf-8")
                    self.admin=mensaje[1:]

                elif ultimo_jugador:

                    enviar=("entrar,ultimo").encode("utf-8")

                elif (not no_hay_admin) and (not ultimo_jugador):

                    enviar=("entrar,normal").encode("utf-8")

                self.clientes.append(mensaje[1:])

        largo=len(enviar).to_bytes(6, byteorder="big")
        socket_cliente.sendall(largo)
        socket_cliente.sendall(enviar)



        
        
