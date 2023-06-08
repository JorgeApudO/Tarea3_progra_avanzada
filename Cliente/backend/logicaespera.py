from PyQt5.QtCore import pyqtSignal, QObject
import socket
from threading import Thread

class LogicaEspera(QObject):

    senal_abrir_ventana=pyqtSignal(list)
    senal_admin=pyqtSignal()
    senal_activar_partida=pyqtSignal(tuple)
    
    def __init__(self):

        super().__init__()

        self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #PASAR A PARAMETROS
        IP_SERVER=socket.gethostname()
        PUERTO_SERVER_ESPERA=2100

        self.sock.connect((IP_SERVER, PUERTO_SERVER_ESPERA))
        self.nombre=""
        self.rol=""
        self.esperando=True

        self.thread_esperar = Thread(target=self.esperar, daemon=True)
        

    def esperar(self):

        while self.esperando:

            info_server=self.recibir_info_server()

            if info_server[0]=="jugadores":
                
                info_jugadores=[]

                for jugador in info_server[1:]:

                    info_jugadores.append(jugador.split(";"))
                    pass

                self.senal_abrir_ventana.emit(info_jugadores)

            elif info_server[0]=="iniciar":

                self.activar_partida(info_server[1:])


    def iniciar_espera(self, tupla_info):

        self.nombre=tupla_info[0]
        self.rol=tupla_info[1]

        mensaje=(f"I{self.nombre},{self.rol}").encode("utf-8")
        largo=len(mensaje).to_bytes(6, byteorder="big")
        
        self.sock.sendall(largo)
        self.sock.sendall(mensaje)

        if self.rol=="admin":

            self.senal_admin.emit()
            pass

        elif self.rol=="ultimo":

            self.iniciar_partida()

        self.thread_esperar.start()


    def recibir_info_server(self):

        largo_mensaje_bytes=self.sock.recv(6)

        largo_mensaje_int=int.from_bytes(largo_mensaje_bytes, byteorder="big")

        mensaje_byte=bytearray()

        while len(mensaje_byte)<largo_mensaje_int:
            mensaje_byte+=self.sock.recv(4096)

        mensaje_str=mensaje_byte.decode("utf-8")

        lista_info=mensaje_str.split(",")

        return lista_info

    def iniciar_partida(self):

        mensaje=("P").encode("utf-8")
        largo=len(mensaje).to_bytes(6, byteorder="big")
        
        self.sock.sendall(largo)
        self.sock.sendall(mensaje)

        pass

    def activar_partida(self, info_jugador):

        self.senal_activar_partida.emit((self.nombre, info_jugador))


        


