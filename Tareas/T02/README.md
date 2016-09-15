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

```
arbol.py
```
### ArbolJugadas
Clase que representa un árbol, modelando cada nodo (que es en sí un árbol) y agregando más de forma incremental. Esta clase se utiliza para el árbol de jugadas y las variaciones que ocurren en las partidas del juego. En caso de no existir ninguna variación en un nodo sólo hay un elemento en la lista (de la clase `MyList`) `hijos`.

Para hacer más fácil el volver a jugadas pasadas cuando el usuario hace click en un nodo del árbol, cada objeto de esta clase tiene como atributos:

* `x`: coordenada x de la piedra correspondiente en el tablero
* `y`: coordenada y de la piedra correspondiente en el tablero
* `number`: corresponde al número de jugada en que se agrega la piedra relacionada con ese nodo del árbol. Coincide con la coordenada **i** del espacio destinado al árbol en la interfaz.
* `depth`: coordenada **j** del espacio destinado al árbol en la interfaz. Se relaciona con en nivel o variación de la partida.

**Estados Iguales**: mediante el atributo `resumen` de cada nodo del árbol (que contiene un string con el estado del tablero resumido, *X* si es vacío, *B* si hay una piedra negra y *W* si hay una piedra blanca) y el método `obtener_resumen(resumen)` es posible comparar cada vez que se agrega una piedra al tablero si hay estados iguales en el arbol de jugadas. En caso de ocurrir esto, se conecta con una línea blanca.

---
```
myEDD.py
```
Además de la utilización de árboles y grafos, utilicé listas ligadas para reemplazar el uso de listas proporcinadas por Python.
### Node
Nodo que únicamente tiene los atributos `value` (valor, lo que se quiere almacenar) y `next` (nodo próximo con el cual se conecta).

### MyList
Clase que representa la lista ligada (caso particular de árbol), es una secuencia de nodos. Luego, tiene un atributo `root` (primer nodo) y `tail` (último nodo). Cuando se utiliza el método `append(value)` cambia el nodo siguiente (`next`) del actual nodo *cola* y luego se actualiza el último nodo (`Node(value)`) en `tail`. En caso de no existir una *cabeza*, el nodo con el valor que se quiere agregar pasa a ser el `root` (y por ende, `tail`). 

Además para esta clase se sobreescriben los métodos:

* `__len__()`: de manera que retorne la cantidad de nodos en la lista ligada.
* `__getitem__()`: de manera que se pueda iterar sobre la lista y conseguir un elemento de ésta. Retorna el valor del nodo en la posición **i** de la lista ligada.
* `__repr__()`: retorna un string que muestra los valores de cada nodo de la lista, separados por comas y encerrados por corchetes (`[]`) como sería en una lista común.

---
```
parserSGF.py
```
Módulo encargado de trabajar con los archivos **.sgf**. 

### InfoJuego
Clase mencionada anteriormente que alamcena toda la información contenida o que debería contener un archivo **SGF**. Los valores predeterminados son *GM* = 1, *FF* = 4, *CA* = "UTF-8", *SZ* = 19, *KM* = 6.5; los que pueden cambiar en caso de abrir un archivo con valores distintos.

### Open
Las siguientes funciones permiten al usuario abrir un archivo de la extensión pedida y retorna un objeto de la clase **ArbolJugadas** para poder ver las partidas guardadas. Este árbol mediante los métodos... **COMPLETAR**.

1. `sgfToTree(path)`
Esta función instancia un objeto de la clase **InfoJuego** (que se almacena en la variable *juego*), abre el archivo y lo lee hasta encontrar el primer nodo (determinado por `";B["`). Todo lo anterior se guarda en cada atributo de *juego* y luego llama a la función `set_arbol` entregándole como parámtros un string con todo el contenido de la partida (combinación de **;B[xy]** e **;W[xy]**, junto con sus variaciones) y la variable *juego*.

Retorna una lista (de la clase `MyList`) con el árbol (objeto de la clase **ArbolJugadas**) y *juego*.

2. `set_arbol(data, juego, arbol_jugadas=None, id_split=0, number_split=0, depth=0)`
Función recursiva que contempla inicialmente dos casos: 
* arbol\_jugadas es *None* -> entonces crea un objeto de la clase **ArbolJugadas** y lo asigna a esa variable. Si comienza con una variación `(`, únicamente tiene el nodo raíz vacío; en cambio, si comienza con una piedra negra `;B` se agregan dos nodos (el raíz vacío y otro de id 1, color "black" y número 1). En ambos caso se llama recursivamente a la función para continuar el árbol.
* otro caso (**else**) -> distingue tres casos para ir formando el árbol:
..* **Caso 0** (base): cuando no hay paréntesis (y, por ende, variaciones) en `data` que es el string que almacena las jugadas. En este caso sólo es un string de la forma *;B[xy];W[xy];B[xy]...* 
..* **Caso 1**: 



### Save

1. `treeToSgf(arbol_jugadas, info, path)`

2. `set_file(arbol_jugadas, ret="")`

---
```
bonus.py
```
> (intento de) bonus

Después de muchos intentos... no lo logré.

![Mucha tristeza](http://www.reactiongifs.com/r/sbbn.gif "Mucha Tristeza")

... pero de todas formas creo que cubrí todo lo pedido por la tarea! Espero que disfrutes este juego!

GO!
---
*Isidora Vizcaya*
