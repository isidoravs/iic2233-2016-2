# Tarea 2
![alt text](http://multitap.cl/wp-content/uploads/2016/01/Gostones.jpg "PROGRAGO")
> Bienvenido a este modelo de las funcionalidades del juego **GO**!
> En éste participan dos jugadores poniendo y capturando piedras en un tablero de 19 x 19.
> Para lograrlo, las distintas clases y sus métodos, además de otras funciones, se dividen en **5** módulos:

```
main.py
```
Módulo principal (**el que se debe ejecutar**) que contiene la extensión de la clase `MainWindow` (del módulo `gui` dado). En este módulo principal, la clase `GOWindow` que hereda de `MainWindow` tiene como atributos principales:

1. `tablero`: objeto de la clase `Tablero` explicada más adelante, que corresponde a un grafo no dirigido que modela el espacio de juego y las intersecciones para colocar las piezas.

2. `juego`: instancia de la clase `InfoJuego` explicada más adelante, que contiene la información de las partidas (*GM[1]FF[4]CA[UTF-8]SZ[19]KM[6.5]* en caso de que estos datos no sean proporcionados por un archivo). Este atributo permite no perder información adicional que exista en los archivos **.sgf** en caso de volver a guardarlos.

3. `jugada`: establece el número de la jugada actual. Se actualiza en caso de hacer una variación y siempre calza con la coordenada **i** del árbol de jugadas.

4. `arbol`: instancia de la clase `ArbolJugadas`, explicada más adelante, que modela el árbol de todas las jugadas (como dice el nombre :)) junto con las variaciones que existan en la partida. Queda representado en la parte derecha de la interfaz.

5. `depth`: indica el nivel donde se está haciendo la variación. Comienza en 0 cuando no hay variaciones y corresponde a la coordenada **j** del árbol de jugadas.

6. `ko_chance`: guarda las coordenadas de la posición que queda prohibida para no violar la **regla de Ko**. En caso de pasar más de un turno desde que esta tentativa opción de Ko, el atributo vuelve a ser *None*.

```
tablero.py
```
Modela el funcionamiento de las piedras en el tablero y su relación unas con otras en las interesecciones.

### NodeTablero
Clase que permite representar cada interesección del tablero. En caso de estar vacía sus atributos `color`, `value` (número de jugada en que se inserta la pieza en esa intersección), `x_pos` e `y_pos` (coordenadas como números) son *None*. Además el atributo `piece` es un booleano que determina si en ese nodo del grafo existe o no una piedra (analogamente para el atributo `square`).

Lo mejor de estos nodos es que se conectan mediante sus atributos `link_up`, `link_down`, `link_right` y `link_left` a los demás nodos del grafo, permitiendo la conexión entre las interesecciones del tablero.

### Tablero
Clase que describe el tablero de juego. Éste corresponde a un grafo no dirigido que dado un tamaño (filas / columnas) conecta los distintos nodos (inicialmente como intersecciones vacías) para crearlo y que exista la debida conexión entre ellos por medio del método `set_tablero(filas, columnas)`.

Esta clase se encarga, además de toda la interacción entre nodos, de llevar la cuenta de prisioneros y territorio del jugador blanco y negro (con sus atributos `prisioneros_black`, `prisioneros_white`, `territorio_black` y `territorio_white`).

Algunos métodos de `Tablero` importantes de explicar son:

1. 

```
arbol.py
```

---
```
myEDD.py
```
Explicar implementación

---
```
parserSGF.py
```
Explicar funcionamiento

---
```
bonus.py
```
> (intento de) bonus
