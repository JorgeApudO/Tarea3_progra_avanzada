# Tarea 3: DCCasillas :school_satchel:



## Consideraciones generales :octocat:

<Mi tarea permite jugar con hasta jugadores pero solo con una ficha cada uno. No hay archivo de parametros (cree los archivos pero no tienen nada) porque no alcance a hacerlo, todas las variables que deberian ser parametros estan anotadas como que deberian moverse y las fichas aparecen una vez que se lanza el primer dado
Mi servidor se encuentra separado en 3 secciones (hay 4 archivos pero no alcance a hacer el ultimo), uno para cada seccion del juego.>

### Cosas implementadas y no implementadas :white_check_mark: :x:

Explicación: mantén el emoji correspondiente, de manera honesta, para cada item. Si quieres, también puedes agregarlos a los títulos:
- ❌ si **NO** completaste lo pedido
- ✅ si completaste **correctamente** lo pedido
- 🟠 si el item está **incompleto** o tiene algunos errores

**⚠️⚠️NO BASTA CON SOLO PONER EL COLOR DE LO IMPLEMENTADO**,
SINO QUE SE DEBERÁ EXPLICAR QUÉ SE REALIZO DETALLADAMENTE EN CADA ITEM.
⚠️⚠️

#### Networking: 23 pts (18%)
##### ✅ Protocolo <Utilizo el protocolo pedido en el enunciado\>
##### ✅ Correcto uso de sockets <Instancio los sockets como corresponde (cliente o servidor) y las aplicaciones se pueden utilizar sin bloquearse por escuchar un socket\>
##### ✅ Conexión <La conexion se mantiene, y se pueden intercambiar todos los tipos necesarios de mensajes\>
##### ✅ Manejo de clientes <Se puede conectar una cantidad ilimitada de clientes por parte de los sockets, eso si, la parte grafica no soporta esto, entonces no lo recomiendo\>
#### Arquitectura Cliente - Servidor: 31 pts (25%)
##### ✅ Roles <Hay una separacion total de los roles de cliente y servidor, los clientes manejan solo cosas que se piden en el enunciado y el servidor solo cosas que se piden en el enunciado, nunca manejan algo que le corresponde al otro\>
##### 🟠 Consistencia <Se mantiene actualizada la informacion entre el cliente y el server, pero no se utilizan locks,\>
##### ✅ Logs <Se implementan todos los logs pedidos en el enunciado\>
#### Manejo de Bytes: 26 pts (21%)
##### ❌ Codificación <No lo implementé\>
##### ❌ Decodificación <No lo implementé\>
##### ❌ Encriptación <No lo implementé\>
##### ❌ Desencriptación <No lo implementé\>
##### 🟠 Integración <No entendí si esto se referia al protocolo de TCP o encriptar y codificar, SI utilizé el protocolo correcto pero NO encripté ni codifiqué\>
#### Interfaz: 23 pts (18%)
##### ✅ Ventana inicio <Se visualiza correctamente la ventana, se realizan todas las revisiones necesarias para el nombre de usuario y su entrada a la sala de espera\>
##### 🟠 Sala de Espera <Se visualiza correctamente la ventana, solo el admin puede abrir la sesion de juego o cuando entra el ultimo jugador, el admin puede iniciar el juego sin importar cuantos jugadores hay\>
##### 🟠 Sala de juego <Se visualiza casi todo lo pedido en la ventana, no se ve el numero del dado y el jugador actual es el que acaba de lanzar el dado no el que lo está por lanzar (me di cuenta de ese error muy tarde como para arreglarlo)\>
##### ❌ Ventana final <No tengo ventana final\>
#### Reglas de DCCasillas: 18 pts (14%)
##### ✅ Inicio del juego <Se asignan correctamente turnos y colores\>
##### 🟠 Ronda <Cada jugador puede lanzar el dado en su turno, avanzan primero por las casillas blancas y luego por las de color, cambian de turno correctamente, no hay segunda ficha, no pude revisar si servia comer fichas pero "deberia" funcionar, se calcula correctamente el avanze segun el resultado del dado pero si se pasa de la casilla final igual gana\>
##### 🟠 Termino del juego <El ganador es el primero en llevar una ficha a la meta\>
#### General: 4 pts (3%)
##### ❌ Parámetros (JSON) <No usé archivo de parametros\>
#### Bonus: 5 décimas máximo
##### ❌ Cheatcode <No realizé cheatcodes\>
##### ❌ Turnos con tiempo <No realizé cheatcodes\>
##### ❌ Rebote <No realizé cheatcodes\>

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. En tanto Server como Cliente, el archivo main.py de Server debe iniciarse primero
Además se debe crear los siguientes archivos y directorios adicionales:
1. ```Sprites/``` en ```Cliente```
Sprites debe contener los mismos archivos entregados en el enunciado, con sus mismas rutas.

## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```random```: ```choice() ```
2. ```threading```: ```thread ```
3. ...

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```clases``` en server: Contiene a ```Cuadro```, ```Camino```, (Lista ligada/grafo para formar el tablero)



eferencias de código externo :book:

Para realizar mi tarea saqué código de:
1. \<Ayudantia 8>: este hace recibe la informacion de los socket en todo y está implementado en todos los archivos de backend y servidor 
2. \<https://stackoverflow.com/questions/67948983/resizing-a-window-with-pyqt5-how-do-i-reduce-the-size-of-a-widget-to-allow-the/67952671#67952671>: este hace \<una imagen que se puede achicar más alla del tamaño minimo de su pixmap> y está implementado en el archivo <ventanajuego.py> en las líneas <8-61> 
