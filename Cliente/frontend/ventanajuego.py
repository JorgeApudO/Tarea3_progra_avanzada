from PyQt5.QtCore import (pyqtSignal, Qt, QSize)
from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QMessageBox)
from PyQt5.QtGui import (QPixmap, QFont, QPainter) 
#from parametros import (RUTA_FONDO, RUTA_LOGO)
import os

class ImagenAdaptable(QWidget):
    """Citar https://stackoverflow.com/questions/67948983/
    resizing-a-window-with-pyqt5-how-do-i-reduce-the-size-of-a-widget-to-allow-the
    /67952671#67952671"""

    def __init__(self,tamano_maximo=QSize(), pixmap=None):
        super().__init__()

        self.pixmap=None
        self._sizeHint=QSize()
        self.ratio= Qt.KeepAspectRatio
        self.transformation = Qt.SmoothTransformation
        self.setMaximumSize(tamano_maximo)
        self.setPixmap(pixmap)
        

    def setPixmap(self, pixmap):
        if self.pixmap != pixmap:
            self.pixmap = pixmap
            if isinstance(pixmap, QPixmap):
                self._sizeHint = pixmap.size()
            else:
                self._sizeHint = QSize()
            self.updateGeometry()
            self.updateScaled()

    def setAspectRatio(self, ratio):
        if self.ratio != ratio:
            self.ratio = ratio
            self.updateScaled()

    def setTransformation(self, transformation):
        if self.transformation != transformation:
            self.transformation = transformation
            self.updateScaled()

    def updateScaled(self):
        if self.pixmap:
            self.scaled = self.pixmap.scaled(self.size(), self.ratio, self.transformation)
        self.update()

    def sizeHint(self):
        return self._sizeHint

    def resizeEvent(self, event):
        self.updateScaled()

    def paintEvent(self, event):
        if not self.pixmap:
            return
        qp = QPainter(self)
        r = self.scaled.rect()
        r.moveCenter(self.rect().center())
        qp.drawPixmap(r, self.scaled)



class VentanaJuego(QWidget):

    senal_dado=pyqtSignal()
    senal_prox_turno=pyqtSignal()
    
    def __init__(self):
        
        super().__init__()

        self.admin=None

        self.setGeometry(20,40,1440,960)
        self.setWindowTitle("Ventana de juego")
        #self.setStyleSheet("background-color: rgb(17,237,245);")

        self.labels_jugadores=[]

        self.crear_elementos()


    def crear_elementos(self):

        self.boton_dado=QPushButton("&Lanzar dado",self)
        self.boton_dado.setFont(QFont("Arial", 20))
        self.boton_dado.setStyleSheet("background-color: rgb(160,160,160)")
        self.boton_dado.clicked.connect(self.lanzar_dado)
        self.boton_dado.setEnabled(False)

        #Pasar a parametros
        RUTA_DADO = os.path.join("Sprites", "Logos", "dado.png")

        ancho_max = int(self.frameGeometry().width() / (4) )
        altura_max = int(self.frameGeometry().height() / (4) )

        tamano_maximo=QSize(ancho_max, altura_max)
        
        pixmap_dado=QPixmap(RUTA_DADO)
        self.imagen_dado= ImagenAdaptable(tamano_maximo, pixmap_dado)

        self.label_resultado_dado=QLabel(self)

        self.layout_boton=QHBoxLayout()
        self.layout_boton.addStretch(1)
        self.layout_boton.addWidget(self.imagen_dado)
        self.layout_boton.addWidget(self.label_resultado_dado)
        self.layout_boton.addStretch(1)
        self.layout_boton.addWidget(self.boton_dado)

        self.jugador_actual=QLabel(self)

        self.fondo_jugador_actual=QWidget(self)
        self.fondo_jugador_actual.setStyleSheet("background-color: rgb(73,255,64);")
        self.layout_jugador_actual_color=QHBoxLayout(self.fondo_jugador_actual)
        self.layout_jugador_actual_color.addWidget(self.jugador_actual)

        self.layout_jugador_actual=QHBoxLayout()
        self.layout_jugador_actual.addWidget(self.fondo_jugador_actual)
        self.layout_jugador_actual.addStretch(1)

        self.layout_superior=QHBoxLayout()
        self.layout_superior.addLayout(self.layout_boton)
        self.layout_superior.addStretch(1)
        self.layout_superior.addLayout(self.layout_jugador_actual)


        self.layout_jugadores=QVBoxLayout()

        for x in range(4):

            self.layout_jugadores.addStretch(1)

            self.fondo_jugador=QWidget(self)
            self.fondo_jugador.setStyleSheet("background-color: rgb(17,237,245);")

            self.layout_jugador=QHBoxLayout()
            self.layout_central_jugador=QHBoxLayout(self.fondo_jugador)
            self.layout_jugador_real=QVBoxLayout()

            self.label_nombre_jugador=QLabel(self)
            self.label_turno_jugador=QLabel(self)
            self.label_ficha_fija=QLabel(self)
            self.label_fichas_base=QLabel(self)
            self.label_fichas_color=QLabel(self)
            self.label_fichas_victoria=QLabel(self)
            self.label_ficha_mueve=QLabel(self)


            diccionario_jugador={}
            diccionario_jugador["nombre"]=self.label_nombre_jugador
            diccionario_jugador["turno"]=self.label_turno_jugador
            diccionario_jugador["fichas base"]=self.label_fichas_base
            diccionario_jugador["fichas color"]=self.label_fichas_color
            diccionario_jugador["fichas victoria"]=self.label_fichas_victoria
            diccionario_jugador["ficha fija"]=self.label_ficha_fija
            diccionario_jugador["ficha mueve"]=self.label_ficha_mueve
            diccionario_jugador["color"]=""

            self.labels_jugadores.append(diccionario_jugador)
            
            self.layout_jugador_real.addWidget(self.label_nombre_jugador)
            self.layout_jugador_real.addStretch(1)
            self.layout_jugador_real.addWidget(self.label_turno_jugador)
            self.layout_jugador_real.addStretch(1)
            self.layout_jugador_real.addWidget(self.label_fichas_base)
            self.layout_jugador_real.addStretch(1)
            self.layout_jugador_real.addWidget(self.label_fichas_color)
            self.layout_jugador_real.addStretch(1)
            self.layout_jugador_real.addWidget(self.label_fichas_victoria)
            self.layout_central_jugador.addWidget(self.label_ficha_fija)
            self.layout_central_jugador.addLayout(self.layout_jugador_real)

            self.layout_jugador.addWidget(self.fondo_jugador)

            self.layout_jugadores.addLayout(self.layout_jugador)

        self.tablero=QLabel(self)

        #Pasar a parametros
        RUTA_TABLERO = os.path.join("Sprites", "Juego", "tablero.png")

        pixmap_tablero= QPixmap(RUTA_TABLERO)
        self.tablero.setPixmap(pixmap_tablero)

        self.layout_tablero= QVBoxLayout()
        self.layout_tablero.addWidget(self.tablero)
        self.tablero.setScaledContents(True)

        self.layout_central=QHBoxLayout()
        self.layout_central.addLayout(self.layout_tablero, 70)
        self.layout_central.addLayout(self.layout_jugadores, 30)

        self.layout_global=QVBoxLayout()

        self.layout_global.addLayout(self.layout_superior)
        self.layout_global.addLayout(self.layout_central)
        

        self.setLayout(self.layout_global)

        pass

    def lanzar_dado(self):

        self.boton_dado.setEnabled(False)
        self.senal_dado.emit()


    def mostrar(self, tupla_jugadores):

        #Pasar a parametros
        RUTA_FICHA_ROJA = os.path.join("Sprites", "Fichas", "Simples", "ficha-roja.png")
        RUTA_FICHA_AZUL = os.path.join("Sprites", "Fichas", "Simples", "ficha-azul.png")
        RUTA_FICHA_AMARILLA = os.path.join("Sprites", "Fichas", "Simples", "ficha-amarilla.png")
        RUTA_FICHA_VERDE = os.path.join("Sprites", "Fichas", "Simples", "ficha-verde.png")

        RUTA_FICHA_ROJA_DOBLE = os.path.join("Sprites", "Fichas", "Dobles", "fichas-rojas.png")
        RUTA_FICHA_AZUL_DOBLE = os.path.join("Sprites", "Fichas", "Dobles", "fichas-azules.png")
        RUTA_FICHA_AMARILLA_DOBLE = os.path.join("Sprites", "Fichas", "Dobles", "fichas-amarillas.png")
        RUTA_FICHA_VERDE_DOBLE = os.path.join("Sprites", "Fichas", "Dobles", "fichas-verdes.png")

        for x in range(len(tupla_jugadores)):

            
            info_jugador=tupla_jugadores[x]
            self.labels_jugadores[x]["color"]=info_jugador[2]

            self.labels_jugadores[x]["nombre"].setText(info_jugador[0])
            self.labels_jugadores[x]["nombre"].setFont(QFont("Arial", 12))
            self.labels_jugadores[x]["turno"].setText(f"Turno: {info_jugador[1]}")
            self.labels_jugadores[x]["fichas base"].setText("Fichas en base: 2")
            self.labels_jugadores[x]["fichas color"].setText("Fichas en color: 0")
            self.labels_jugadores[x]["fichas victoria"].setText("Fichas en victoria: 0")

            if info_jugador[2]=="rojo":

                imagen_ficha=QPixmap(RUTA_FICHA_ROJA)

            elif info_jugador[2]=="azul":

                imagen_ficha=QPixmap(RUTA_FICHA_AZUL)

            elif info_jugador[2]=="amarillo":

                imagen_ficha=QPixmap(RUTA_FICHA_AMARILLA)

            elif info_jugador[2]=="verde":

                imagen_ficha=QPixmap(RUTA_FICHA_VERDE)
            pass


            self.labels_jugadores[x]["ficha fija"].setPixmap(imagen_ficha)
            self.labels_jugadores[x]["ficha mueve"].setPixmap(imagen_ficha)

            self.labels_jugadores[x]["ficha mueve"].setGeometry(0,0,0,0)
            self.labels_jugadores[x]["ficha mueve"].setScaledContents(True)


        self.show()

    def mi_turno(self):

        self.boton_dado.setEnabled(True)
        self.show()
        pass

    def actualizar(self, lista_info_jugadores, jugador_actual):

        self.jugador_actual.setText(f"Jugador actual: {jugador_actual}")
        self.jugador_actual.setFont(QFont("Arial", 20))

        for lista in lista_info_jugadores:

            for diccionario in self.labels_jugadores:

                if diccionario["color"]==lista[1]:

                    #Pasar a parametros 
                    TAMANO_X_FICHA=100
                    TAMANO_Y_FICHA=100

                    coord=lista[0].split("-")
                    x=coord[0].replace("[","")
                    x=x.replace("]","")
                    x=x.replace(" ","")
                    x=int(x)
                    y=coord[1].replace("[","")
                    y=y.replace("]","")
                    y=y.replace(" ","")
                    y=int(y)

                    diccionario["ficha mueve"].setGeometry(x, y, TAMANO_X_FICHA, TAMANO_Y_FICHA)
                    diccionario["ficha mueve"].raise_()
        
        self.show()

        self.senal_prox_turno.emit()
                

    def terminar(self, ganador):

        self.pop_up= QMessageBox()
        self.pop_up.setWindowTitle("Partida terminada")

        mensaje=f"Se terminó la partida, el/la ganador@ es {ganador}"
        self.pop_up.setText(mensaje)
        self.pop_up.setIcon(QMessageBox.Information)
        ejecutar = self.pop_up.exec_()
        pass


        