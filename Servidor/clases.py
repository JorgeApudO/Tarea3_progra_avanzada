class Cuadro:
    def __init__(self, coordenadas):

        self.siguiente=None
        self.jugador=None
        self.jugador_nombre=None
        self.color=None
        self.siguiente_color=None
        self.coordenadas=coordenadas
        pass


class Camino:
    def __init__(self):

        self.primero=None
        self.ultimo=None
        self.ultimo_color=None
        self.bases={}
        self.cuadros=[]
        pass


    def anadir_cuadro_normal(self, cuadro):

        if self.primero==None:

            self.primero=cuadro
            self.ultimo=cuadro

        else:

            self.ultimo.siguiente=cuadro
            self.ultimo=cuadro

        

        self.cuadros.append(cuadro)

    def anadir_cuadro_color(self, cuadro):

        if self.ultimo_color==None:

            self.ultimo.siguiente_color=cuadro
            self.ultimo_color=cuadro
            

        else:

            self.ultimo_color.siguiente_color=cuadro
            self.ultimo_color=cuadro

        self.cuadros.append(cuadro)

    def avanzar_jugador(self, cuadro, numero, color_jugador):
        
        cuadro_actual=cuadro
        for x in range(numero):

            if cuadro_actual.siguiente_color!=None:

                if cuadro_actual.siguiente_color.color!=color_jugador:

                    cuadro_actual=cuadro_actual.siguiente
                    pass

                elif cuadro_actual.siguiente_color.color==color_jugador:

                    cuadro_actual=cuadro_actual.siguiente_color

            elif cuadro_actual.siguiente!=None and cuadro_actual.siguiente_color==None:

                cuadro_actual=cuadro_actual.siguiente

            else:

                return("final")

        if cuadro_actual.jugador!=None:

            jugador_comido=cuadro_actual.jugador
            jugador_come=cuadro.jugador
            cuadro_actual.jugador=jugador_come
            cuadro.jugador=None

            jugador_comido_nombre=cuadro_actual.jugador_nombre
            jugador_come_nombre=cuadro.jugador_nombre
            cuadro_actual.jugador_nombre=jugador_come_nombre
            cuadro.jugador_nombre=None

            self.bases[jugador_comido].jugador=jugador_comido
            self.bases[jugador_comido].jugador_nombre=jugador_comido_nombre


            return((jugador_comido_nombre, jugador_come_nombre, cuadro_actual))

        else:
            
            cuadro_actual.jugador_nombre=cuadro.jugador_nombre
            cuadro.jugador_nombre=None

            cuadro_actual.jugador=cuadro.jugador
            cuadro.jugador=None

            return(cuadro_actual)