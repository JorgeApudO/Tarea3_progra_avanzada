from PyQt5.QtCore import pyqtSignal, QObject
import socket

class LogicaInicio(QObject):

    senal_abrir_espera=pyqtSignal(tuple)
    senal_corregir_nombre=pyqtSignal(str)
    senal_error=pyqtSignal()
    
    def __init__(self):

        super().__init__()
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #PASAR A PARAMETROS
        IP_SERVER=socket.gethostname()
        PUERTO_SERVER_INICIO=2000

        self.sock.connect((IP_SERVER, PUERTO_SERVER_INICIO))


    def recibir_nombre(self, nombre):

        mensaje=("N"+nombre).encode("utf-8")
        largo=len(mensaje).to_bytes(6, byteorder="big")
        
        self.sock.sendall(largo)
        self.sock.sendall(mensaje)


        info_server=self.recibir_info_server()

        if info_server[0]=="bueno":

            self.espera(nombre)

        elif info_server[0]=="malo":

            self.senal_corregir_nombre.emit(info_server[1])



    def recibir_info_server(self):

        largo_mensaje_bytes=self.sock.recv(6)

        largo_mensaje_int=int.from_bytes(largo_mensaje_bytes, byteorder="big")

        mensaje_byte=bytearray()

        while len(mensaje_byte)<largo_mensaje_int:
            mensaje_byte+=self.sock.recv(4096)

        mensaje_str=mensaje_byte.decode("utf-8")

        lista_info=mensaje_str.split(",")

        return lista_info



        pass

    def espera(self,nombre):

        mensaje=("E"+nombre).encode("utf-8")
        largo=len(mensaje).to_bytes(6, byteorder="big")
        
        self.sock.sendall(largo)
        self.sock.sendall(mensaje)

        info_server=self.recibir_info_server()


        if info_server[0]=="lleno":

            self.senal_error.emit()

        elif info_server[0]=="entrar":

            self.senal_abrir_espera.emit((nombre, info_server[1]))

        pass

