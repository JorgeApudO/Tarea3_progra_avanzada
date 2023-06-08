from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit,
    QMessageBox)
from PyQt5.QtGui import (QPixmap, QFont, QPalette, QBrush)
#from parametros import (RUTA_FONDO, RUTA_LOGO)
import os


class VentanaInicio(QWidget):

    senal_nombre=pyqtSignal(str)
    senal_espera=pyqtSignal(tuple)
    
    def __init__(self):
        
        super().__init__()
        
        #Pasar a parametros
        RUTA_FONDO = os.path.join("Sprites", "Logos", "fondo.png")

        self.setGeometry(300,100,1200,800)
        self.setWindowTitle("Ventana de inicio")
        #citar https://blog.birost.com/a?ID=00850-44be7ac4-ba3a-4674-ad3c-5edb442a2557

        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap(RUTA_FONDO)))  
        self.setPalette(palette)
        self.crear_elementos()


    def crear_elementos(self):

        self.logo=QLabel(self)
        
        #Pasar a parametros
        RUTA_LOGO = os.path.join("Sprites", "Logos", "logo.png")

        imagen_logo=QPixmap(RUTA_LOGO)

        self.logo.setPixmap(imagen_logo)

        self.layout_logo=QHBoxLayout()
        self.layout_logo.addStretch(3)
        self.layout_logo.addWidget(self.logo)
        self.layout_logo.addStretch(3)

        self.boton_jugar=QPushButton("&Jugar",self)
        self.boton_jugar.setFont(QFont("Arial", 20))
        self.boton_jugar.setStyleSheet("background-color: rgb(160,160,160)")
        
        self.layout_boton=QHBoxLayout()
        self.layout_boton.addStretch(1)
        self.layout_boton.addWidget(self.boton_jugar)
        self.layout_boton.addStretch(1)

        self.edit_nombre = QLineEdit("Nombre de Usuario:", self)
        self.edit_nombre.setFont(QFont("Arial", 25))
        self.edit_nombre.setStyleSheet("background-color: rgb(160,160,160)")

        self.layout_nombre=QHBoxLayout()
        self.layout_nombre.addStretch(1)
        self.layout_nombre.addWidget(self.edit_nombre)
        self.layout_nombre.addStretch(1)


        self.layout_global=QVBoxLayout()
        self.layout_global.addStretch(4)
        self.layout_global.addLayout(self.layout_logo)
        self.layout_global.addStretch(2)
        self.layout_global.addLayout(self.layout_nombre)
        self.layout_global.addStretch(1)
        self.layout_global.addLayout(self.layout_boton)
        self.layout_global.addStretch(2)

        self.setLayout(self.layout_global)

        #conectar botones

        self.boton_jugar.clicked.connect(self.enviar_nombre)
        pass

    def enviar_nombre(self):

        self.senal_nombre.emit(self.edit_nombre.text())
        pass

    def corregir_nombre(self, error):

        self.pop_up= QMessageBox()
        self.pop_up.setWindowTitle("Error nombre de usuario")

        if error=="no_alfa":

            mensaje="El nombre de usuario debe ser alfanumerico"

        elif error=="largo":

            mensaje="El largo del nombre debe estar entre 1 y 10 caracteres"

        elif error=="repetido":

            mensaje="Ya existe un usuario con este nombre"

        self.pop_up.setText(mensaje)
        self.pop_up.setIcon(QMessageBox.Warning)
        ejecutar = self.pop_up.exec_()

    def sala_llena(self):

        self.pop_up= QMessageBox()
        self.pop_up.setWindowTitle("Sala llena")

        self.pop_up.setText("La sala de juego se encuentra llena")
        self.pop_up.setIcon(QMessageBox.Warning)
        ejecutar = self.pop_up.exec_()

    def abrir_espera(self, tupla_informacion):

        self.hide()

        self.senal_espera.emit(tupla_informacion)
        
        pass
        

