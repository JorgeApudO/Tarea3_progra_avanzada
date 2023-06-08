from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit,
    QMessageBox)
from PyQt5.QtGui import (QPixmap, QFont, QPalette, QBrush)
#from parametros import (RUTA_FONDO, RUTA_LOGO)
import os


class VentanaEspera(QWidget):

    senal_iniciar_juego=pyqtSignal()
    senal_abrir_juego=pyqtSignal(tuple)
    
    def __init__(self):
        
        super().__init__()

        self.admin=False
        
        #Pasar a parametros
        RUTA_FONDO = os.path.join("Sprites", "Logos", "fondo.png")

        self.setGeometry(300,100,1200,800)
        self.setWindowTitle("Ventana de espera")
        #citar https://blog.birost.com/a?ID=00850-44be7ac4-ba3a-4674-ad3c-5edb442a2557

        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap(RUTA_FONDO)))  
        self.setPalette(palette)

        self.labels_jugadores=[]

        self.crear_elementos()

    def crear_elementos(self):

        self.boton_admin=QPushButton("&Inicar Partida",self)
        self.boton_admin.setFont(QFont("Arial", 20))
        self.boton_admin.setStyleSheet("background-color: rgb(160,160,160)")
        self.boton_admin.clicked.connect(self.iniciar_partida)
        self.boton_admin.setEnabled(False)
        
        self.layout_boton=QHBoxLayout()
        self.layout_boton.addStretch(1)
        self.layout_boton.addWidget(self.boton_admin)
        self.layout_boton.addStretch(1)

        self.layout_global=QVBoxLayout()

        for x in range(4):

            self.layout_global.addStretch(1)

            self.fondo_jugador=QWidget(self)
            self.fondo_jugador.setStyleSheet("background-color:white;")

            self.layout_jugador=QHBoxLayout()
            self.layout_central_jugador=QHBoxLayout(self.fondo_jugador)


            self.nombre_jugador=QLabel(self)
            self.color_jugador=QLabel(self)
            self.ficha=QLabel(self)

            diccionario_jugador={}
            diccionario_jugador["nombre"]=self.nombre_jugador
            diccionario_jugador["color"]=self.color_jugador
            diccionario_jugador["ficha"]=self.ficha

            self.labels_jugadores.append(diccionario_jugador)
            
            self.layout_central_jugador.addWidget(self.nombre_jugador)
            self.layout_central_jugador.addStretch(1)
            self.layout_central_jugador.addWidget(self.color_jugador)
            self.layout_central_jugador.addStretch(1)
            self.layout_central_jugador.addWidget(self.ficha)

            self.layout_jugador.addStretch(1)
            self.layout_jugador.addWidget(self.fondo_jugador)
            self.layout_jugador.addStretch(1)

            self.layout_global.addLayout(self.layout_jugador)

        
        self.layout_global.addStretch(1)
        self.layout_global.addLayout(self.layout_boton)
        self.layout_global.addStretch(2)

        self.setLayout(self.layout_global)


    def mostrar(self, lista_jugadores):

        for x in range(len(lista_jugadores)):

            self.labels_jugadores[x]["nombre"]
            lista_jugadores[x][0]
            pass

            self.labels_jugadores[x]["nombre"].setText(lista_jugadores[x][0])
            self.labels_jugadores[x]["nombre"].setFont(QFont("Arial", 20))

            self.labels_jugadores[x]["color"].setText(lista_jugadores[x][1])
            self.labels_jugadores[x]["color"].setFont(QFont("Arial", 20))

            #Pasar a parametros
            RUTA_FICHA_ROJA = os.path.join("Sprites", "Fichas", "Simples", "ficha-roja.png")
            RUTA_FICHA_AZUL = os.path.join("Sprites", "Fichas", "Simples", "ficha-azul.png")
            RUTA_FICHA_AMARILLA = os.path.join("Sprites", "Fichas", "Simples", "ficha-amarilla.png")
            RUTA_FICHA_VERDE = os.path.join("Sprites", "Fichas", "Simples", "ficha-verde.png")


            if lista_jugadores[x][1]=="rojo":

                imagen_ficha=QPixmap(RUTA_FICHA_ROJA)

            elif lista_jugadores[x][1]=="azul":

                imagen_ficha=QPixmap(RUTA_FICHA_AZUL)

            elif lista_jugadores[x][1]=="amarillo":

                imagen_ficha=QPixmap(RUTA_FICHA_AMARILLA)

            elif lista_jugadores[x][1]=="verde":

                imagen_ficha=QPixmap(RUTA_FICHA_VERDE)

            self.labels_jugadores[x]["ficha"].setPixmap(imagen_ficha)
            self.labels_jugadores[x]["ficha"].setScaledContents(True)

        self.show()

    def asignar_admin(self):

        self.admin=True
        self.boton_admin.setEnabled(True)
        

    def iniciar_partida(self):

        self.senal_iniciar_juego.emit()

    def activar_partida(self, info_jugador):

        self.hide()

        self.senal_abrir_juego.emit(info_jugador)

        pass

