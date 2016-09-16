# Tarea 2
![alt text](http://multitap.cl/wp-content/uploads/2016/01/Gostones.jpg "PROGRAGO")
> Bienvenido a este modelo de las funcionalidades del juego **GO**!
> En éste participan dos jugadores poniendo y capturando piedras en un tablero de 19 x 19.
> Para lograrlo, las distintas clases y sus métodos, además de otras funciones, se dividen en **5** módulos:

```
main.py
```
Módulo principal (**el que se debe ejecutar**) que contiene la extensión de la clase `MainWindow` (del módulo `gui` dado). En este módulo principal, la clase `GOWindow`, que hereda de `MainWindow`, tiene como atributos principales:

1. `tablero`: objeto de la clase `Tablero` explicada más adelante. Éste corresponde a un grafo no dirigido que modela el espacio de juego y las intersecciones para colocar las piedras.

2. `juego`: instancia de la clase `InfoJuego` explicada más adelante. Éste contiene la información de las partidas (*GM[1]FF[4]CA[UTF-8]SZ[19]KM[6.5]* en caso de que estos datos no sean proporcionados por un archivo). Este atributo permite no perder información adicional que exista en los archivos **.sgf** en caso de volver a guardarlos.

3. `jugada`: establece el número de la jugada actual. Se actualiza en caso de hacer una variación y siempre calza con la coordenada **i** del árbol de jugadas.

4. `arbol`: instancia de la clase `ArbolJugadas`, explicada más adelante, que modela el árbol de todas las jugadas (como dice el nombre :)) junto con las variaciones que existan en la partida. Queda representado en la parte derecha de la interfaz.

5. `depth`: indica el nivel donde se está haciendo la variación. Comienza en 0 cuando no hay variaciones y corresponde a la coordenada **j** del árbol de jugadas. Además el atributo `max_depth` determina la cantidad de variaciones, lo que es útil por si se requiere hacer una variación entre dos lineas de juego (permite desplazar las ramas del árbol hacia abajo y tener una visión óptima de éste). **Obs:** Al hacer click en un nodo del árbol de jugadas, únicamente si el siguiente estado difiere al que habría ocurrido, se produce la variación. 

6. `pass_seguidos`: permite llevar la cuenta de las veces que los jugadores han pasado. Si no pasa de manera seguida y su valor es 1 se reinicia, si pasa de manera seguida termina el juego. Una vez pasadas dos veces seguidas los jugadores deben terminar el juego, no pueden realizar otra accion hasta determinar el ganador (pero luego pueden volver a analizar las jugadas).

7. `ko_chance`: guarda las coordenadas de la posición que queda prohibida para no violar la **regla de Ko**. En caso de pasar más de un turno desde que se establece la tentativa opción de Ko, el atributo vuelve a ser *None*.

```
tablero.py
```
Modela el funcionamiento de las piedras en el tablero y su relación unas con otras en las interesecciones.

### NodeTablero
Clase que permite representar cada interesección del tablero. En caso de estar vacía sus atributos `color`, `value` (número de jugada en que se inserta la pieza en esa intersección), `x_pos` e `y_pos` (coordenadas como números) son *None*. Además el atributo `piece` es un booleano que determina si en ese nodo del grafo existe o no una piedra (analogamente para el atributo `square`).

**Obs:** el número `value` se agrega en las piedras del tablero en la interfaz, dado que permiten al jugador llevar un mejor seguimiento de sus jugadas pasadas.

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

**Estados Iguales**: mediante el atributo `resumen` de cada nodo del árbol (que contiene un string de 361 caracteres con el estado del tablero resumido, *X* si es vacío, *B* si hay una piedra negra y *W* si hay una piedra blanca) y el método `obtener_resumen(resumen)` es posible comparar cada vez que se agrega una piedra al tablero si hay estados iguales en el arbol de jugadas. En caso de ocurrir esto, se conecta con una línea blanca.

---
```
myEDD.py
```
Además de la utilización de árboles y grafos, utilicé listas ligadas para reemplazar el uso de listas proporcinadas por Python.
### Node
Nodo que únicamente tiene los atributos `value` (valor, lo que se quiere almacenar) y `next` (nodo próximo con el cual se conecta).

### MyList
Clase que representa la lista ligada (caso particular de árbol), es una secuencia de nodos. Luego, tiene un atributo `root` (primer nodo) y `tail` (último nodo). Cuando se utiliza el método `append(value)` cambia el nodo siguiente (`next`) del actual nodo *cola* y luego se actualiza el último nodo (`Node(value)`) en `tail`. En caso de no existir una *cabeza*, el nodo con el valor que se quiere agregar pasa a ser el `root` (y por ende, adicionalmente, `tail`). 

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
Las siguientes funciones permiten al usuario abrir un archivo de la extensión pedida y retorna un objeto de la clase **ArbolJugadas** para poder ver las partidas guardadas. Este árbol mediante los métodos `set_arbol_jugadas(arbol_jugadas)` y previamente `clear_arbol(arbol)` (para borrar los nodos de las jugadas en la interfaz) de **GoWindow**, es el que se ve reflejado para los jugadores de manera que puedan hacer click en los nodos y ver las jugadas pasadas.

1. `sgfToTree(path)`
Esta función instancia un objeto de la clase **InfoJuego** (que se almacena en la variable *juego*), abre el archivo y lo lee hasta encontrar el primer nodo (determinado por `";B["`). Todo lo anterior se guarda en cada atributo de *juego* y luego llama a la función `set_arbol(data, juego)` entregándole como parámetros un string con todo el contenido de la partida (combinación de **;B[xy]** e **;W[xy]**, junto con sus variaciones) y la variable *juego*. Retorna una lista (de la clase `MyList`) con el árbol (objeto de la clase **ArbolJugadas**) y *juego*.

2. `set_arbol(data, juego, arbol_jugadas=None, id_split=0, number_split=0, depth=0)`
Función recursiva que contempla inicialmente dos casos: 

* arbol\_jugadas es *None* -> entonces crea un objeto de la clase **ArbolJugadas** y lo asigna a esa variable. Si comienza con una variación `(`, únicamente tiene el nodo raíz vacío; en cambio, si comienza con una piedra negra `;B` se agregan dos nodos (el raíz vacío y otro de id 1, color "black" y número 1). En ambos caso se llama recursivamente a la función para continuar el árbol.

* otro caso (**else**) -> distingue tres casos para ir formando el árbol:

**Caso 0** (base): cuando no hay paréntesis (y, por ende, variaciones) en `data` que es el string que almacena las jugadas. En este caso sólo es un string de la forma *;B[xy];W[xy];B[xy]...*.

**Caso 1**: data comienza con una variación - `(` - luego en este caso se busca la cantidad de variaciones y por cada una se llama recursivamente a la función cambiando el `depth` de cada uno (coordenada **j** en el árbol).

**Caso 2**: cuando data no es inmediatamente una variación pero dentro del string hay varaciones. En este caso funciona de manera similar al caso base hasta llegar a la variación donde se llama recursivamente la función para llegar al caso 1.

Finalmente retorna el árbol de jugadas.

![Emoción infinita](http://www.reactiongifs.com/r/cheering_minions.gif "Costó pero se pudo")

### Save
Las siguientes funciones permiten al usuario guardar las jugadas en un archivo de extensión **.sgf**, dado el árbol de jugadas al momento de hacer click en el botón *Save*.

1. `treeToSgf(arbol_jugadas, info, path)`
Función que comienza el string que será escrito en el archivo en `path`. En primer lugar se agrega la información básica obtenida de `info` que es el objeto de la clase **InfoJuego** mencionado anteriormente y luego se llama a `set_file(arbol_jugadas)` para agregar la información del árbol al string. Finalmente cierra con un `)\n` y lo escribe en el archivo pedido.

2. `set_file(arbol_jugadas, ret="")`
Función recursiva que distingue tres casos:

* **Caso 0** (base): el nodo del árbol no tiene hijos, y por lo tanto, es el nodo final del árbol. Retorna el string `ret`.
* **Caso 1**: el nodo de `arbol_jugadas` tiene únicamente un hijo, luego no hay variaciones. Se agrega `;B[xy]` o `;W[xy]` según corresponda. A `ret` se le agrega el resto del árbol, llamado recursivamente a la función, con el hijo como parámetro.
* **Caso 2**: el nodo tiene más de un hijo, entonces por cada hijo se agrega la porción de variación (de manera recursiva) que corresponda, encerrada entre paréntesis.

Finalmente retorna el string con el resumen de jugadas.

```
Funcionalidades que vale la pena explicar...
```

### On point click
Cuando se hace click en el nodo del árbol se llama al método `show_tablero_pasado(point)` que obtiene todas las jugadas anteriores a ese punto siguiendo el camino correcto en caso de haber una variación. Luego reinicia el tablero y los valores de los nodos de éste para llamar a `simular_jugadas_pasadas(letter, y, text, color)` por cada jugada anterior. Esto permite recrear el proceso de todas las jugadas hasta llegar al punto seleccionado de manera que se capturen las piedras correspondientes y no existan problemas si el usuario vuelve a seleccionar un nodo del árbol pero del "futuro".

### Add piece
El método `add_piece(letter, y, text, color)` de la clase **Tablero** (DuckTyping) retorna *True* (y actualiza los atributos del nodo correspondiente) si es un lugar válido para agregar una pieza. Si es una jugada suicida o ya hay una pieza en esta intersección, retorna *False*. Para determinar si una jugada es suicida se llama al método `actualizar_libertades(node)` de la clase **Tablero** que crea una lista con los nodos de color contrario junto al nodo recién agregado. Esta lista se entrega como parámetro a `revisar_captura` y si este método no retorna *None*, retorna una lista con las piedras a eliminar (cuando existe captura), que luego permite borrarlas del tablero.

### Set grupo
El método `set_grupo(nodo)` de la clase **Tablero** se encarga de armar los grupos de piedras contiguos de un mismo color. Esto ayuda a su captura (para contar las libertades del grupo) y también para contar territorio dado que se modifica de manera que se generen "grupos" de nodos vacíos. Debido a que es una función recursiva se facilitaba su implementación con el atributo de **Tablero** `one_group` que almacena, cada vez que se necesita, un grupo de manera temporal.

**Obs:** el código permite que con agregar una piedra se pueda capturar más de un grupo a la vez, si corresponde.

### On pass click
Al pasar se agrega en el árbol un nodo con el color del usuario y número de jugada, pero `x` e `y` son *None* (por lo que no existe en el tablero pieza con ese color y numero). 

**Casos especiales**: al abrir un archivo con pasos, en caso de apretar ese nodo del arbol se agrega 1 a `pass_seguidos`. En caso de que el jugador siguiente pase, termina el juego, de otra forma se agrega una variación. Si el archivo termina con dos pasos seguidos y se aprieta el último nodo, la partida termina y se deben seleccionar las piedras muertas para calcular el territorio.

### On count click
Cuando el usuario presiona el botón `COUNT`, además del cálculo de puntaje, se llama a la función `contar_territorio()`. Este método se encarga de crear "grupos" de nodos vacíos para luego determinar si pertenecen a algún territorio (verificando si está rodeado por piedras de un mismo color). Para verificar que el jugador no seleccione grupos con dos o más ojos se utilizan los métodos `set_posibles_ojos()` (que agrega a una lista los nodos de intersecciones vacías rodeados por piedras) y `validar_grupo(grupo)` que cuenta la cantidad de ojos dentro de un mismo grupo de piedras (si es mayor o igual a 2 retorna *False*). 

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
