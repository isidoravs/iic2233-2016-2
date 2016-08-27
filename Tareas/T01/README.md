# Tarea 1
*Isidora Vizcaya*
```python
print("Ha aparecido un {} salvaje!".format(ayudante_salvaje.name))
```

Para poder modelar un sistema de batallas entre programones que se nos pidió en la tarea, cree 6 **modulos** que explicaré a continuación con sus respectivos conjuntos de clases y funciones (separados por sus relaciones y tipos en común).

```
main.py
```

Módulo principal (**el que se debe ejecutar**) que contiene el menú en el cuál el usuario puede registarse / ingresar o salir del sistema. Para este módulo se utiliza la librería *sys* y se importan las clases **ProgramonRojo**, **PCBastian** y **Menu**, que se explican en el próximo módulo. Las clases anteriores se utilizan para cargar los datos y permitir el ingreso de los usuarios al juego; una vez ingresados se despliega el menú principal de Programon Rojo.

```
programonRojo.py
```

Módulo que contiene las clases principales del juego, que manejan el funcionamiento de éste. Este módulo utiliza las librerías *sys* y *math*, además de importar las clases **Programon**, **Ciudad**, **Mapa**, **Jugador** y **Progradex** para las distintas interacciones entre el sistema principal y estas. Por último, desde el módulo **jsonReader** se importan las funciones *jsonToDict* y *dictToJson* para la carga/almacenamiento de datos.

### ProgramonRojo
Clase que almacena los jugadores del juego y el jugador actual. Permite ingresar, registrarse y salir del sistema, a partir de la informacion que carga de la base de datos del juego. Al iniciar el juego, automáticamente se cargan los datos, de esta manera al hacer *log in* se verifica el nombre de usuario y contraseña y al hacer *sign up* se instancia un objeto de la clase **Jugador** con un nombre de usuario único y un primer programon que escoge entre tres opciones para agregar a su equipo.

### PCBastian
Clase que funciona como una base de datos que almacena todos los programones (por jugador) y la lista con la información base de todos los programones existentes. Recibe como parametro el objeto de la clase **ProgramonRojo** de manera que pueda acceder a todos los jugadores y el jugador actual. Lo esencial de esta clase es que su método *cambiar_equipo* permite al jugador actual, administrar los programones del equipo con los restantes guardados en el diccionario de programones de la clase. Para acceder a esta opcion se debe ingresar al PC con el nombre y contraseña.

### Menu
Clase que permite al usuario acceder a las distintas funcionalidades del juego. Siempre da la opción de volver hacia atrás y recibe como parámetros el objeto de la clase **ProgramonRojo** y **PCBastian** para acceder a los jugadores y sus programones. A través de un ciclo *while* este se mantiene corriendo (mediante el método *run*) hasta que el jugador opta por *salir* y se guarda su información en el **PC** (datos se guardan en archivo *infoJugadores.json*). El menú despliega 6 opciones: "Programones en la Progradex" (que llama al método *show_programones* de la clase **Progradex** explicada más adelante), "Caminar" (hacia adelante, atrás y mostrar mapa, que ocupa métodos de la clase **Mapa** explicada más adelante), "Datos del jugador" (imprime la información del jugador actual), "Consultas" y "Salir".

Para la opción de consultas se da la opción de "Batalla por Programon" que muestra todos los resultados de los enfrentamientos contra un oponente al introducir el nombre del programon. Esta opción muestra el nombre del oponente y el resultado: "ganador", "perdedor" o "intercambio" (en caso de que haya sido cambiado antes de perder contra otro programón). Otra opción de consultas es "Ranking de programones" que imprime los mejores 10 porcentajes de batallas ganadas por especie de programón (como deben haber batallado en más de 10 batallas para entrar en el ranking, pueden ser menos de 10 porcentajes). La última opción de consulta es "Jugador" que amplía la opción 3. del menú principal, dado que muestra todos sus programones (con stats) y todas las batallas en que éstos se han visto involucrados.

```
jugador.py
```

Módulo que contiene la clase **Jugador** y **Progradex**, siendo este último un implemento que tiene cada jugador. Importa la función *jsonToDict* y la clase **Ciudad** del módulo *ciudades.py*.

### Jugador
Clase que asigna todos los atributos de los jugadores: unique\_id, unique\_name, password, yenes, prograbolas, equipo (lista con objetos de la clase **Programon**), medallas, batallas (diccionario en que sus keys son los nombres de las ciudades y sus respectivos values una lista de listas de la forma: `[nombre_entrenador, victorias]`). Además un atributo que posee es el *location\_id* que es un integer que determina la ubicación del jugador en el mapa. Ésta puede ir desde 0 (Ciudad, Pallet Town) hasta 32 (Ciudad, Cinnabar Island). Por lo tanto, una cualidad importante es que si `location_id % 4` es igual a 0, el jugador se encuentra en una ciudad y por lo tanto su atributo *location* es un objeto de la clase **Ciudad**, de otra forma se encuentra en la hierba y *location* es None. Por último, el atributo *progradex* es un objeto de la clase **Progradex**.

En esta clase se sobrecarga el método `__str__` para mostrar la información del jugador cuando éste lo necesite.

### Progradex
Clase que contiene a los programones (objetos de la clase **Programon**) vistos y capturados del jugador en dos listas distintas. Su método *show\_programones* mencionado antes, muestra toda la información (al hacer print() al objeto) de los programones capturados y únicamente el nombre, id y tipo de los programones vistos (además de la última vez que fueron vistos, número de ruta o ciudad).

```
ciudades.py
```

Módulo que contiene la clase **Ciudad** y sus las **Gimnasio** y **Mapa** que se relacionan directamente con ella. Para este módulo se utiliza la librería *random* para determinar la aparición de un programon salvaje en la hierba (modelada por la clase **Mapa**) y además se importan las funciones *jsonToDict* y las clases **Programon**, **Batalla** y **Trainer** (que permiten la interacción entre el jugador y los programones en los lugares modelados por este módulo).

### Ciudad
Los objetos de esta clase poseen un *nombre*, *id* y reciben además al objeto de la clase *PCBastian* como atributo. En caso de que su id sea distinto de 0 (no es Pallet Town), la ciudad posee un *gimnasio*. Para instanciar el gimnasio (objeto de la clase **Gimnasio** utilizo el método *set\_trainers()* que los obtiene de la base de datos y agrega sus respectivos programones al equipo. 

Como en la ciudad el jugador puede acceder a distintas opciones, los métodos `menu_ciudad()` y `opciones_ciudad()` permiten al jugador optar por:
* Acceder al Centro Programon<br />
Que ofrece ingresar al PC de Bastián y cambiar los programones de su equipo por lo que ha capturado y se encuentran en el PC (si tiene menos de 6 en su equipo, se le indica que no hay programones disponibles para cambiar).
* Ingresar al Gimnasio<br />
Llama al método `entrar()` de la clase **Gimnasio** que informa al usuario si es la primera vez que pasa por éste o, en caso contrario, muestra la cantidad de entrenadores que ha derrotado y ofrece la opción de escoger un entrenador para pelear. En caso de haberlos derrotado a todos, inmediatamente comienza una batalla con el lider del gimnasio.
* Ir a la Tienda de Prograbolas<br />
En esta opción se revisa que el jugador pueda acceder al menos a una prograbola y con el método de la clase, `tienda(jugador)`, se pide la cantidad de prograbolas a comprar y descuenta el dinero del usuario (si es que lo puede pagar).

### Gimnasio
Los objetos de esta clase poseen *nombre*, *id*, una lista de entrenadores (objetos de la clase **Trainer**) y un líder (objeto de la clase **Trainer** diferenciado). Su único método es *entrar()* que se explicó en la clase anterior.

### Mapa
Clase que modela el desplazamiento del usuario entre las ciudades. Posee como atributos el *jugador* actual, un *id* (que funciona de la misma manera que el *location\_id* del jugador (de hecho, se utiliza para actualizar este último), el *PC* y el contenido del archivo *routes.json*.

Su método más importante es `new_location(movimiento)` que recibe el valor **1** (si el jugador quiere avanzar hacia adelante) o **-1** (si el jugador quiere avanzar hacia atrás). En este método se determina la nueva ubicación del jugador de ser posible (no puede retroceder desde Pallet Town ni avanzar desde Cinnabar Island) y actualiza el atributo *location* del jugador dependiendo si entra o sale de una ciudad. Este método revisa si el jugador ha batallado en el gimnasio para que pueda seguir *avanzando* en el mapa. Si el jugador se encuentra en la hierba con un 35% de probabilidad llama al método `generar_programon_salvaje()` que retorna un objeto de la clase **Programon** para comenzar una batalla con éste y poder capturarlo (esta función revisa la restricción de los niveles de programones con evolución/subevolución por ruta).

```
batallas.py
```

Es el módulo más complejo que lleva a cabo todo el proceso de pelea entre programones, tanto en gimnasios como en la hierba (contra programones salvajes). Utiliza las librerías *math* (para cálculo de stats) y *random* (para definir ataques de oponentes o probabilidad de captura de programon salvaje). También utiliza la función *jsonToDict* para obtener los datos base de programones y movimientos.

### Trainer
Los objetos de esta clase poseen *nombre*, *programon\_squad* (lista con los programones de su equipo) y *trainer\_type*. Éste último determina si el entrenador es uno común o el lider del gimnasio. Para determinar los trainers por gimnasio, modifiqué el archivo *gyms.json* de manera que el jugador pudiera distinguir al entrenador por su nombre.

### Batalla
Cada batalla tiene como atributos el *nombre de la ciudad*, *jugador*, *oponente* (objeto de la clase **Trainer** o **Programon** (en caso de ser uno salvaje), *equipo del oponente* (lista con programones), *PC* y un boolean *capturable* que determina si la batalla se realiza contra un programon salvaje o no. Además se tienen las listas *elegidos\_jugador* / *disponibles\_jugador* y *elegidos\_oponente* / *disponibles\_oponente* que ayudan a determinar cuando el jugador o su oponente pierde la batalla si no hay más programones en condiciones de pelear y, además, determinan qué programones del equipo participaron de la batalla (para actualizar sus stats si logran ganar). Esta clase maneja el atributo *visto\_capturado* de los objetos de la clase **Programon** que se explica más adelante.

Sus métodos son (en general todos se llaman entre sí hasta que la batalla haya finalizado):
* `primer_programon()`: permite al usuario escoger el programon que comenzará de su equipo
* `menu_batalla(programon_jugador, programon_oponente)`: da la opción al jugador de pelear, cambiar su programon de la batalla o abandonar la batalla (lo que retorna "cobarde"). En caso de que se enfrente a un programon salvaje, se agrega la opción de lanzar una prograbola para capturarlo
* `turno_pelea(programon_jugador, programon_oponente)`: define los turnos de la batalla, en cada uno comienza el programon más rápido (**Obs.** se tener el mismo *speed* comienza el jugador) y permite a ambos programones atacar (en caso de que el primero en atacar no derrote al otro)
* `proximo_a_pelear(programon_actual, entrenador, solo_cambio)`: retorna el programon que reemplazará a *programon\_actual* debido a que éste no se encuentra en condiciones para pelear. Entrenador determina si el jugador o trainer deben cambiar a su programon (**Obs.** el jugador elige de sus programones disponibles y el trainer escoge automáticamente el siguiente en su lista de disponibles). Si no hay más programones disponibles determina que la batalla ha finalizado.
* `terminar_batalla(ganador, programon_jugador)`: devuelve a los programones a sus condiciones originales. Dependiendo del ganador, actualiza stats y sube el nivel de los programones que batallaron (de ganar el jugador). Actualiza la cantidad de yenes del jugador dependiendo del resultado (**Obs.** si se enfrenta contra programon salvaje, no recibe ni pierde dinero (¿Quién le pagaría o quitaría su dinero, si no está en el gimnasio?). En caso de enfrentarse contra el líder y ganar, el jugador recibe una medalla.
* `atrapar_programon_salvaje(programon_salvaje)`: se llama al lanzar la prograbola y permite capturar al programón según la probabilidad de acertarle.
* `pelear(programon_jugador, programon_oponente, final_batalla, ganador`: función recursiva principal de la clase **Batalla**. Para llegar al caso base y llamar al método *terminar\_batalla* en caso de existir un ganador el booleano *final\_batalla* es True. En caso contrario, se llama continuamente al método *turno\_pelea* que determina si un programon a perdido en el turno. Si pierde se llama al método *proximo\_a\_pelear*, que de retornar None implica que la batalla ha terminado y se llega al caso base. De no ocurrir lo anterior, se llama el método *pelear* a sí mismo para continuar con la batalla.

En este módulo además se agregan las funciones:
* `calculo_stats(base, iv, ev, nivel`: en base a las fórmulas dadas se calculan los nuevos stats del programon ganador
* `calculo_harm(programon_ataca, programon_defiende, base_move, type_move, PC)`: dependiendo de la combianción del ataque del programon y el tipo de programon atacado, calcula el daño (*harm*) que el atacante hace al programon que se defiende
* `resultado_ataque(result, programon_ataca, programon_defiende, PC)`: a partir del daño hecho, retorna un **Bool** determinando si el atacante ganó o no (al dejar sin *hp* a su oponente)

```
programones.py
```
Último módulo que contiene únicamente la clase **Programon**. Utiliza las librerías *math* y *random* para fines muy similares al modulo anterior. Además importa las funciones *jsonToDict* (de JsonReader.py) y *calculo\_stats* (de batallas.py).

### Programon
Clase que permite instanciar programones con *id*, *unique_id* (generado al instanciar, único para cada programon inclusive los salvajes no capturados), *name*, *moves* (lista con diccionarios que contienen los datos de cada movimiento), *tipo*, *nivel*, *hp*, *stats*, *evolve level* y *evolve to*, además de los *iv* y *ev* aleatorios (**Obs.** generados al instanciar y estáticos al evolucionar). Se incluye también, un atributo *batallas* (lista de lista tipo `[oponente, resultado]`, *original_hp* para devolver los hp al finalizar una batalla y *visto\_capturado* que contiene el id de la ubicación en el mapa en que fue por última vez visto o capturado.

Sus métodos son:
* `atacar`: dependiendo si es un programon del jugador o entrenador, determina el próximo movimiento en la pelea y su probabilidad de acertar
* `actualizar_stats`: con la función `calculo_stats` actualiza los nuevos valores de los atributos del programon si el programon aumenta de nivel (gana batalla -eso incluye capturar programón salvaje- en la que participó y tiene hp mayor a 0) **Obs.** Programones de entrenadores nunca aumentan su nivel o stats.
* `evolucionar`: Actualiza los atributos del programón, manteniendo su *unique\_id* y *nivel* (que es igual a *evolve\_level*) para que la instancia del programon en la **Progradex** y **PC** sea la misma sólo que con las características de un programón evolucionado. Este métdo retorna una instancia de **Programon** con los mismos atributos que el programon a evolucionar (pero cambia *unique\_id* a -1) para luego agregar esa "subevolución" a la Progradex (**Obs.** esta subevolución no está disponible para agregar al equipo de batalla).

Además se sobrecarga el método `__str__()` para mostrar los datos de cada programón.

## myJsonToDict
Junto con los módulos anteriores, se incluye el archivo *myJsonReader.py* que contiene la función `myJsonToDict(path)` pedida para esta tarea (sin utilizar librería *json*). En este archivo se extrae la información de los 6 archivos .json entregados en la tarea y se compara lo obtenido con lo retornado por la función `jsonToDict(path)` original. En este archivo se ve que lo obtenido es igual! Sin embargo, en los archivos entregados mantuve el uso de la función original debido a su mayor eficiencia.

```python
print("¡Ya esta!\n{} atrapado".format(ayudante_salvaje.name))
print("Se ha actualizando tu informacion en la Progradex")
```
