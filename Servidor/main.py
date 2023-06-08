import socket

from inicio import ServerInicio
from espera import ServerEspera
from juego import ServerJuego

server_inicio=ServerInicio()
server_espera=ServerEspera()
server_juego=ServerJuego()

#Pasar a parametros
SAFE_WORD="SI"
while server_inicio.recibiendo==True:

    parar=input()
    if parar=="SAFE_WORD":
        server_inicio.recibiendo=False
        server_espera.recibiendo=False
        server_juego.recibiendo=False






