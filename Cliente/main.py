import sys
from PyQt5.QtWidgets import QApplication
from frontend.ventanainicio import VentanaInicio
from backend.logicainicio import LogicaInicio
from frontend.ventanaespera import VentanaEspera
from backend.logicaespera import LogicaEspera

from frontend.ventanajuego import VentanaJuego
from backend.logicajuego import LogicaJuego
"""
from frontend.ventanafinal import VentanaPostNivel
from backend.logicafinal import LogicaPostNivel
"""


app = QApplication([])
ventana_inicio=VentanaInicio()
logica_inicio=LogicaInicio()

ventana_espera=VentanaEspera()
logica_espera=LogicaEspera()

ventana_juego=VentanaJuego()
logica_juego=LogicaJuego()

"""

logica_principal= LogicaPrincipal()
ventana_principal= VentanaPrincipal()

logica_juego= LogicaJuego()
ventana_juego= VentanaJuego()

ventana_post_nivel= VentanaPostNivel()
logica_post_nivel= LogicaPostNivel()
"""

ventana_inicio.senal_nombre.connect(logica_inicio.recibir_nombre)
ventana_inicio.senal_espera.connect(logica_espera.iniciar_espera)

logica_inicio.senal_corregir_nombre.connect(ventana_inicio.corregir_nombre)
logica_inicio.senal_error.connect(ventana_inicio.sala_llena)
logica_inicio.senal_abrir_espera.connect(ventana_inicio.abrir_espera)

logica_espera.senal_admin.connect(ventana_espera.asignar_admin)
logica_espera.senal_abrir_ventana.connect(ventana_espera.mostrar)
logica_espera.senal_activar_partida.connect(ventana_espera.activar_partida)

ventana_espera.senal_iniciar_juego.connect(logica_espera.iniciar_partida)
ventana_espera.senal_abrir_juego.connect(logica_juego.abrir_juego)

logica_juego.senal_abrir_ventana.connect(ventana_juego.mostrar)
logica_juego.senal_mi_turno.connect(ventana_juego.mi_turno)
logica_juego.senal_terminar_juego.connect(ventana_juego.terminar)
logica_juego.senal_actualizar_pantalla.connect(ventana_juego.actualizar)

ventana_juego.senal_dado.connect(logica_juego.dado_a_server)
ventana_juego.senal_prox_turno.connect(logica_juego.prox_turno)


"""

ventana_principal.senal_enviar_datos.connect(logica_principal.revisar_datos)
logica_principal.senal_datos_corregidos.connect(ventana_principal.recibir_datos)
ventana_principal.senal_jugar.connect(logica_juego.iniciar_juego)

logica_juego.senal_abrir_ventana.connect(ventana_juego.mostrar_ventana)
logica_juego.senal_actualizar.connect(ventana_juego.actualizar_nivel)
logica_juego.senal_disparar_arma.connect(ventana_juego.disparar_arma)
logica_juego.senal_explosion.connect(ventana_juego.explosion)
logica_juego.senal_cerrar_nivel.connect(ventana_juego.animacion_final)

ventana_juego.senal_tecla.connect(logica_juego.accion_mira)
ventana_juego.senal_abrir_post_nivel.connect(ventana_post_nivel.mostrar_ventana)
ventana_juego.senal_volver.connect(ventana_principal.mostrar_ventana)
ventana_juego.senal_volver.connect(logica_juego.volver)

ventana_post_nivel.senal_salir.connect(logica_post_nivel.cerrar_juego)
ventana_post_nivel.senal_volver_a_jugar.connect(logica_juego.iniciar_nivel)
"""

ventana_inicio.show()
sys.exit(app.exec_())

