from PyQt5.QtCore import pyqtSignal, QObject
import socket
from threading import Thread

class LogicaJuego(QObject):

    senal_abrir_ventana=pyqtSignal(list)
    senal_mi_turno=pyqtSignal()
    senal_terminar_juego=pyqtSignal(str)
    senal_actualizar_pantalla=pyqtSignal(list, str)
    
    def __init__(self):

        super().__init__()

        self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #PASAR A PARAMETROS
        IP_SERVER=socket.gethostname()
        PUERTO_SERVER_JUEGO=2200

        self.sock.connect((IP_SERVER, PUERTO_SERVER_JUEGO))
        self.nombre=""
        self.turno=0
        self.color=""
        self.jugando=True

        self.fichas_en_base=2
        self.fichas_victoria=0
        self.fichas_en_color=0

        self.info_fichas=[self.fichas_en_base, self.fichas_victoria, self.fichas_en_color]




        self.thread_jugar = Thread(target=self.jugar, daemon=True)

    def jugar(self):

        while self.jugando:

            info_server=self.recibir_info_server()

            if info_server[0]=="P":

                numero_turno=int(info_server[1])
                jugadores_totales=int(info_server[2])
                valor=numero_turno%jugadores_totales

                if valor==0:
                    valor=jugadores_totales

                if valor==self.turno:
                    self.senal_mi_turno.emit()
                    pass

            elif info_server[0]=="F":

                jugador_actual=info_server[1]

                info=info_server[2:]

                lista_info=[]

                for string in info:

                    lista_info.append(string.split(";"))
                    pass

                self.senal_actualizar_pantalla.emit(lista_info, jugador_actual)
                self.senal_terminar_juego.emit(info_server[1])

            elif info_server[0]=="A":

                jugador_actual=info_server[1]

                info=info_server[2:]

                lista_info=[]

                for string in info:

                    lista_info.append(string.split(";"))
                    pass

                self.senal_actualizar_pantalla.emit(lista_info, jugador_actual)

        pass

    def abrir_juego(self, tupla_jugador):

        self.nombre=tupla_jugador[0]

        info_jugadores=tupla_jugador[1]

        mensaje=(f"P{self.nombre}").encode("utf-8")
        largo=len(mensaje).to_bytes(6, byteorder="big")

        self.sock.sendall(largo)
        self.sock.sendall(mensaje)

        lista_info_jugadores=[]

        for jugador in info_jugadores:

            lista_info_jugadores.append(jugador.split(";"))

            if lista_info_jugadores[-1][0]==self.nombre:

                self.turno=int(lista_info_jugadores[-1][1]) + 1
                self.color=lista_info_jugadores[-1][2]

        self.senal_abrir_ventana.emit(lista_info_jugadores)

        self.thread_jugar.start()


    def recibir_info_server(self):

        largo_mensaje_bytes=self.sock.recv(6)

        largo_mensaje_int=int.from_bytes(largo_mensaje_bytes, byteorder="big")

        mensaje_byte=bytearray()

        while len(mensaje_byte)<largo_mensaje_int:
            mensaje_byte+=self.sock.recv(4096)

        mensaje_str=mensaje_byte.decode("utf-8")

        lista_info=mensaje_str.split(",")

        return lista_info


    def dado_a_server(self):

        mensaje=(f"T{self.nombre},{self.color}").encode("utf-8")
        largo=len(mensaje).to_bytes(6, byteorder="big")

        self.sock.sendall(largo)
        self.sock.sendall(mensaje)
        pass

    def prox_turno(self):

        mensaje=(f"J{self.nombre},{self.color}").encode("utf-8")
        largo=len(mensaje).to_bytes(6, byteorder="big")

        self.sock.sendall(largo)
        self.sock.sendall(mensaje)

        pass