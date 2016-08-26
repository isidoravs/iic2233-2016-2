# Tarea 1
*Isidora Vizcaya*

Para poder modelar un sistema de batallas entre programones que se nos pidió en la tarea, cree 6 **modulos** que explicaré a continuación con sus respectivos conjuntos de clases y funciones (separados por sus relaciones y tipos en común).

* main.py

Módulo principal (ejecutable) que contiene el menú en el cuál el usuario puede registarse / ingresar o salir del sistema. Para este módulo se utiliza la librería *sys* y se importan las clases **ProgramonRojo**, **PCBastian** y **Menu**, que se explican en el próximo módulo. Las clases anteriores se utilizan para cargar los datos y permitir el ingreso de los usuarios al juego; una vez ingresados se despliega el menú principal de Programon Rojo.

* programonRojo.py

Módulo que contiene las clases principales del juego, que manejan el funcionamiento de éste.
### ProgramonRojo
Clase que almacena los jugadores del juego y el jugador actual. Permite ingresar, registrarse y salir del sistema, a partir de la informacion que carga de la base de datos del juego. Al iniciar el juego, automáticamente se cargan los datos, de esta manera al hacer *log in* se verifica el nombre de usuario y contraseña y al hacer *sign up* se instancia un objeto de la clase **Jugador** con un nombre de usuario único que escoge entre los tres primeros programones y se agregan a su equipo.

### PCBastian
Clase que funciona como una base de datos que almacena todos los programones (por jugador) y la lista con la información base de todos los programones existentes. Recibe como parametro el objeto de la clase **ProgramonRojo** de manera que pueda acceder a todos los jugadores y el jugador actual. Lo esencial de esta clase es que su método *cambiar_equipo* permite al jugador actual, administrar los programones del equipo con los restantes guardados en el diccionario de programones de la clase. Para acceder a esta opcion se debe ingresar al PC con el nombre y contraseña.

### Menu
Clase que permite al usuario acceder a las distintas funcionalidades del juego. Siempre da la opción de volver hacia atrás y recibe como parámetros el objeto de la clase **ProgramonRojo** y **PCBastian** para acceder a los jugadores y sus programones. A través de un ciclo *while* este se mantiene corriendo (mediante el método *run*) hasta que el jugador opta por *salir* y se guarda su información en el **PC** (datos se guardan en archivo *infoJugadores.json*). El menú despliega 6 opciones: "Programones en la Progradex" (que llama al método *show_programones* de la clase **Progradex** explicada más adelante), "Caminar" (hacia adelante, atrás y mostrar mapa, que ocupa métodos de la clase **Mapa** explicada más adelante), "Datos del jugador" (imprime la información del jugador actual), "Consultas", "Salir".

Para la opción de consultas se da la opción de "Batalla por Programon" que muestra todos los resultados de los enfrentamientos contra un oponente al introducir el nombre del programon. Esta opción muestra el nombre del oponente y el resultado: "ganador", "perdedor" o "intercambio" (en caso de que haya sido cambiado antes de perder contra otro programón). Otra opción de consultas es "Ranking de programones" que imprime los mejores 10 porcentajes de batallas ganadas por especie de programón (como deben haber batallado en más de 10 batallas para entrar en el ranking, pueden ser menos de 10 porcentajes). La última opción de consulta es "Jugador" que amplía la opción 3. del menú principal, dado que muestra todos sus programones (con stats) y todas las batallas en que éstos se han visto involucrados.
