# Tarea 1
*Isidora Vizcaya*

Para poder modelar un sistema de batallas entre programones que se nos pidió en la tarea, cree 6 **modulos** que explicaré a continuación con sus respectivos conjuntos de clases y funciones (separados por sus relaciones y tipos en común).

1. main.py

Módulo principal (ejecutable) que contiene el menú en el cuál el usuario puede registarse / ingresar o salir del sistema. Para este módulo se utiliza la librería *sys* y se importan las clases **ProgramonRojo**, **PCBastian** y **Menu**, que se explican en el próximo módulo. Las clases anteriores se utilizan para cargar los datos y permitir el ingreso de los usuarios al juego; una vez ingresados se despliega el menú principal de Programon Rojo.

2. programonRojo.py

Módulo que contiene las clases principales del juego, que manejan el funcionamiento de éste.
### ProgramonRojo
Clase que almacena los jugadores del juego y el jugador actual. Permite ingresar, registrarse y salir del sistema, a partir de la informacion que carga de la base de datos del juego. Al iniciar el juego, automáticamente se cargan los datos, de esta manera al hacer *log in* se verifica el nombre de usuario y contraseña y al hacer *sign up* se instancia un objeto de la clase **Jugador** con un nombre de usuario único que escoge entre los tres primeros programones y se agregan a su equipo.

### PCBastian
Clase que funciona como una base de datos que almacena todos los programones (por jugador) y la lista con la información base de todos los programones existentes. Recibe como parametro el objeto de la clase **ProgramonRojo** de manera que pueda acceder a todos los jugadores y el jugador actual. Lo esencial de esta clase es que su método *cambiar_equipo* permite al jugador actual, administrar los programones del equipo con los restantes guardados en el diccionario de programones de la clase. Para acceder a esta opcion se debe ingresar al PC con el nombre y contraseña.


