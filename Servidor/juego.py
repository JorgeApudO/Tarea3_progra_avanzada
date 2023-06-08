import socket
from threading import Thread
from random import choice
from clases import (Cuadro, Camino)

class ServerJuego():
    
    def __init__(self):

        #Pasar a parametros
        IP_SERVER=socket.gethostname()
        PUERTO_SERVER_JUEGO=2200

        print("Se ha iniciado la sección del juego del server")

        self.socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_servidor.bind((IP_SERVER, PUERTO_SERVER_JUEGO))
        self.socket_servidor.listen()
        self.clientes = {}
        self.admin=None
        self.recibiendo=True
        self.turno=1
        self.avisando=False
        self.opciones_dado=[1, 2, 3]
        self.jugadores_totales=0

        #El camino parte desde la esquina superior izquierda, es una lista ligada
        #y saca ramas para los colores

        self.camino=Camino()

        #Pasar a parametros
        INICIO_X=200
        INICIO_Y=75
        TAMANO_CUADRO=150


        x=INICIO_X
        y=INICIO_Y

        for i in range(16):

            coordenadas=[x, y]

            cuadro=Cuadro(coordenadas)

            self.camino.anadir_cuadro_normal(cuadro)


            if i==0:

                cuadro=Cuadro([x-TAMANO_CUADRO, y])
                cuadro.siguiente=self.camino.ultimo
                self.camino.bases["azul"]=cuadro
                x += TAMANO_CUADRO

            elif i>0 and i<3:
                x += TAMANO_CUADRO 
                pass
            elif i==3:

                y_color = y + TAMANO_CUADRO 

                for a in range(3):

                    cuadro_color=Cuadro([x, y_color])
                    cuadro_color.color="amarillo"

                    self.camino.anadir_cuadro_color(cuadro_color)

                    y_color+=TAMANO_CUADRO

                self.camino.ultimo_color=None

                x += TAMANO_CUADRO
                y += TAMANO_CUADRO

            elif i>=4 and i<7:

                if i==4:

                    cuadro=Cuadro([x, y-TAMANO_CUADRO])
                    cuadro.siguiente=self.camino.ultimo
                    self.camino.bases["amarillo"]=cuadro
                    pass

                y += TAMANO_CUADRO

            elif i==7:

                x_color = x - TAMANO_CUADRO 

                for a in range(3):

                    cuadro_color=Cuadro([x_color, y])
                    cuadro_color.color="verde"

                    self.camino.anadir_cuadro_color(cuadro_color)

                    x_color-=TAMANO_CUADRO
                
                self.camino.ultimo_color=None

                x -= TAMANO_CUADRO
                y += TAMANO_CUADRO

            elif i>=8 and i<11:

                if i==8:

                    cuadro=Cuadro([x+TAMANO_CUADRO, y])
                    cuadro.siguiente=self.camino.ultimo
                    self.camino.bases["verde"]=cuadro

                    pass

                x -= TAMANO_CUADRO

            elif i==11:

                y_color = y - TAMANO_CUADRO 

                for a in range(3):

                    cuadro_color=Cuadro([x, y_color])
                    cuadro_color.color="rojo"

                    self.camino.anadir_cuadro_color(cuadro_color)

                    y_color-=TAMANO_CUADRO
                
                self.camino.ultimo_color=None

                x -= TAMANO_CUADRO
                y -= TAMANO_CUADRO

            elif i>=12 and i<15:

                if i==12:

                    cuadro=Cuadro([x, y+TAMANO_CUADRO])
                    cuadro.siguiente=self.camino.ultimo
                    self.camino.bases["rojo"]=cuadro
                    pass

                y -= TAMANO_CUADRO

            elif i==15:

                x_color = x + TAMANO_CUADRO 

                for a in range(3):

                    cuadro_color=Cuadro([x_color, y])
                    cuadro_color.color="azul"

                    self.camino.anadir_cuadro_color(cuadro_color)

                    y_color+=TAMANO_CUADRO

                self.camino.ultimo_color=None

        self.camino.ultimo.siguiente=self.camino.primero


        thread_recibir_clientes = Thread(target=self.recibir_clientes, daemon=True)
        thread_recibir_clientes.start()


    def recibir_clientes(self):
        
        while self.recibiendo:

            #Citar esto, ayudantia 8

            info_cliente = self.socket_servidor.accept()
            socket_cliente = info_cliente[0]
            direccion = info_cliente[1]
            print(f'Cliente con dirección {direccion} se ha conectado al servidor del juego')
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
        self.jugadores_totales=len(self.clientes)
        if mensaje[0]=="P":

            for base in self.camino.bases:

                self.camino.bases[base].jugador=base
                self.camino.bases[base].jugador_nombre=mensaje[1:]

                pass

            self.clientes[mensaje[1:]]=socket_cliente
            self.jugadores_totales=len(self.clientes)

            enviar=f"P,1,{self.jugadores_totales}".encode("utf-8")
            largo=len(enviar).to_bytes(6, byteorder="big")

            socket_cliente.sendall(largo)
            socket_cliente.sendall(enviar)

        elif mensaje[0]=="T":

            info_cliente=mensaje[1:].split(",")

            jugador_actual=info_cliente[0]
            print(f"Es el turno de {jugador_actual}")
            color=info_cliente[1]

            res_dado=choice(self.opciones_dado)

            for base in self.camino.bases:

                if self.camino.bases[base].jugador==color:

                    cuadro_actual=self.camino.bases[base]
                    
            for cuadro in self.camino.cuadros:

                if cuadro.jugador==color:
                    
                    cuadro_actual=cuadro
             
            avanzar=self.camino.avanzar_jugador(cuadro_actual, res_dado, color)

            if type(avanzar)==str:
                
                mandar=f"F,{jugador_actual},"
                print(f"{jugador_actual} ha ganado")

            elif type(avanzar)==tuple:

                mandar=f"A,{jugador_actual},"
                print(f"{avanzar[1]} se ha comido a {avanzar[0]} al avanzar {res_dado} casillas")

            else:

                mandar=f"A,{jugador_actual},"
                print(f"{jugador_actual} ha avanzado {res_dado} casillas")

            info_jugadores=[]

            for base in self.camino.bases:

                if self.camino.bases[base].jugador!=None:

                    coord=str(self.camino.bases[base].coordenadas).replace(",", "-")
                    color=self.camino.bases[base].jugador

                    info=f"{coord};{color}"

                    info_jugadores.append(info)

            for cuadro in self.camino.cuadros:

                if cuadro.jugador!=None:

                    coord=str(cuadro.coordenadas).replace(",", "-")
                                
                    info=f"{coord};{cuadro.jugador}"
                    info_jugadores.append(info)

            
            for info in info_jugadores:

                mandar+= f"{str(info)},"

            
            enviar=mandar[:-1].encode("utf-8")
            largo=len(enviar).to_bytes(6, byteorder="big")

            self.turno+=1

            for cliente in self.clientes:

                self.clientes[cliente].sendall(largo)
                self.clientes[cliente].sendall(enviar)
                pass

        elif mensaje[0]=="J":

            self.avisando=True

            enviar=f"P,{str(self.turno)},{str(self.jugadores_totales)}".encode("utf-8")
            largo=len(enviar).to_bytes(6, byteorder="big")

            socket_cliente.sendall(largo)
            socket_cliente.sendall(enviar)


            