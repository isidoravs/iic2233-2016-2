# Tarea 2
![alt text](http://multitap.cl/wp-content/uploads/2016/01/Gostones.jpg "PROGRAGO")
> Bienvenido a este modelo de las funcionalidades del juego **GO**!
> En éste participan dos jugadores poniendo y capturando piedras en un tablero de 19 x 19.
> Para lograrlo, las distintas clases y sus métodos, además de otras funciones, se dividen en **5** módulos:

```
main.py
```
Módulo principal (**el que se debe ejecutar**) que contiene la extensión de la clase `MainWindow` (del módulo `gui` dado). En este módulo principal, la clase `GOWindow` que hereda de `MainWindow` tiene como atributos:

1. `tablero`: objeto de la clase `Tablero` explicada más adelante, que corresponde a un grafo no dirigido que modela el espacio de juego y las intersecciones para colocar las piezas.
2. `juego`: instancia de la clase `InfoJuego` explicada más adelante, que contiene la información de las partidas (*GM[1]FF[4]CA[UTF-8]SZ[19]KM[6.5]* en caso de que estos datos no sean proporcionados por un archivo). Este atributo permite no perder información adicional que exista en los archivos **.sgf** en caso de volver a guardarlos.
3. `turn`: determina que jugador tiene el turno (*black* o *white*)
4. `jugada`: establece el número de la jugada actual. Se actualiza en caso de hacer una variación y siempre calza con la coordenada **i** del árbol de jugadas.
5. `arbol`: instancia de la clase `ArbolJugadas`, explicada más adelante, que modela el árbol de todas las jugadas (como dice el nombre :)) junto con las variaciones que existan en la partida. Queda representado en la parte derecha de la interfaz.
6. `max_depth`: número que indica la cantidad de variaciones en el árbol. Útil para actualizar las ramas en caso de hacer una variación que necesite desplazar otras ramas hacia abajo.
7. `id_prox_nodo`: número único que asigna un id a cada nodo del árbol, de manera que se pueda guardar la información y establecer las relaciones padre-hijo entre los nodos del árbol.
8. `depth`: indica el nivel donde se está haciendo la variación. Comienza en 0 cuando no hay variaciones y corresponde a la coordenada **j** del árbol de jugadas.
9. `actual_node`: nodo del tablero que está en juego cuando es un turno. Principalmente, ayuda a establecer las variacines cuando existe una divergencia en las jugadas (**Obs** : si se selecciona un nodo anterior, la variación comienza sólo desde el punto en que difieren las jugadas. Para esto también ayuda el booleano `new_variation`.). 
10. `tablero_pasado`: lista (de la clase `MyList`) con nodos que determina las jugadas anteriores al punto seleccionado por el usuario.
11. `dead_pieces`: lista (de la clase `MyList`) de nodos que se deen eliminar dado que fueron marcados como muertos.
12. `ko_chance`: guarda las coordenadas de la posición que queda prohibida para no violar la **regla de Ko**. En caso de pasar más de un turno desde que esta tentativa opción de Ko, el atributo vuelve a ser *None*.
13. `end_game`: (por último!) booleano que determina si ya fue el término de una partida.
