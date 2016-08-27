# Tarea 1
*Isidora Vizcaya*
```python
"Ha aparecido un {} salvaje!".format(ayudante.name)
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
* Acceder al Centro Programon
Que ofrece ingresar al PC de Bastián y cambiar los programones de su equipo por lo que ha capturado y se encuentran en el PC (si tiene menos de 6 en su equipo, se le indica que no hay programones disponibles para cambiar).
* Ingresar al Gimnasio
Llama al método `entrar()` de la clase **Gimnasio** que informa al usuario si es la primera vez que pasa por éste o, en caso contrario, muestra la cantidad de entrenadores que ha derrotado y ofrece la opción de escoger un entrenador para pelear. En caso de haberlos derrotado a todos, inmediatamente comienza una batalla con el lider del gimnasio.
* Ir a la Tienda de Prograbolas
En esta opción se revisa que el jugador pueda acceder al menos a una prograbola y con el método de la clase, `tienda(jugador)`, se pide la cantidad de prograbolas a comprar y descuenta el dinero del usuario (si es que lo puede pagar).

### Gimnasio
Los objetos de esta clase poseen *nombre*, *id*, una lista de entrenadores (objetos de la clase **Trainer**) y un líder (objeto de la clase **Trainer** diferenciado). Su único método es *entrar()* que se explicó en la clase anterior.

### Mapa
Clase que modela el desplazamiento del usuario entre las ciudades. Posee como atributos el *jugador* actual, un *id* (que funciona de la misma manera que el *location\_id* del jugador (de hecho, se utiliza para actualizar este último), el *PC* y el contenido del archivo *routes.json*.

Su método más importante es `new_location(movimiento)` que recibe el valor **1** (si el jugador quiere avanzar hacia adelante) o **-1** (si el jugador quiere avanzar hacia atrás). En este método se determina la nueva ubicación del jugador de ser posible (no puede retroceder desde Pallet Town ni avanzar desde Cinnabar Island) y actualiza el atributo *location* del jugador dependiendo si entra o sale de una ciudad. Este método revisa si el jugador ha batallado en el gimnasio para que pueda seguir *avanzando* en el mapa. Si el jugador se encuentra en la hierba con un 35% de probabilidad llama al método `generar_programon_salvaje()` que retorna un objeto de la clase **Programon** para comenzar una batalla con éste y poder capturarlo.

```
batallas.py
```

Es el módulo más complejo que lleva a cabo todo el proceso de pelea entre programones, tanto en gimnasios como en la hierba (contra programones salvajes). Utiliza las librerías *math* (para cálculo de stats) y *random* (para definir ataques de oponentes o probabilidad de captura de programon salvaje). También utiliza la función *jsonToDict* para obtener los datos base de programones y movimientos.

### Trainer






## myJsonToDict
Junto con los módulos anteriores, se incluye el archivo *myJsonReader.py* que contiene la función `myJsonToDict(path)` pedida para esta tarea (sin utilizar librería *json*). En este archivo se extrae la información de los 6 archivos .json entregados en la tarea y se compara lo obtenido con lo retornado por la función `jsonToDict(path)` original. En este archivo se ve que lo obtenido es igual! Sin embargo, en los archivos entregados mantuve el uso de la función original debido a su mayor eficiencia.
