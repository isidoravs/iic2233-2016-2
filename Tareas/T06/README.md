# Tarea 6
> Bienvenido a Programillo! Para programar este juego, las distintas clases y sus métodos, además de otras funciones, se dividen en 6 módulos:

# Cliente-Servidor
En la entrega hay dos carpetas que incluyen los programas del cliente y el servidor separadamente. Estos funcionan de forma independiente y puede ser ejecutados desde distintos computadores. Las variables de HOST y PORT se dejaron visibles para su manipulación.

# /server
```
server.py
```
Módulo encargado de crear las conexiones con los sockets del cliente y manejar las respuestas que debe enviar a sus mensajes. El método `handle_command` es el encargado de decidir la respuesta que se entregará. Funciona principalmente mediante encoding y decoding de strings.

EL servidor es el único con acceso a la base de datos:
## /server/db
* *users.txt*: contiene a todos los usuarios registrados, sus contraseñas y sal respectivas
* *words.txt*: contiene todas las palabras del juego
* */chats*: carpeta con archivos del estilo "amigo1;amigo2;....txt" que guarda el historial de chats
* */friends*: carpeta que contiene archivos con el nombre de usuario y dentro de éste todos sus amigos.
* */games*: carpeta que contiene archivos con el nombre de usuario y dentro de éste todas las salas o juegos que tiene con otros amigos (para que muestre las salas creadas al abrir su cuenta).
* */games_record*: carpeta con archivos del estilo "amigo1;amigo2;....txt" que guarda el historial de juego (conversaciones, ganadores, turno de dibujar, etc.)

# /client


### Dibujando...
* Grosor es entero entre 1 y 3.
* `{` determina dibujo libre, `\` recta y `(` curva.
* Para **recta** se seleccionan dos puntos (inicio y fin) y **curva** requiere tres puntos para definirla (estilo Paint).
* **Templates:** tienen tamaño predeterminado, se insertan en dibujo al seleccionar su botón y al siguiente click determina su posición final (del centro de la figura).

### Asignación de puntajes
1. *Dibujante*
Si todos los jugadores adivinan su dibujo se le otorgan 100 puntos.
![alt text](https://media.giphy.com/media/AVcFVGSYI4Ijm/giphy.gif "Bonus dotes artísticos")

2. *Adivinador*
Si adivina la palabra su puntaje es `100 // (<puesto_en_adivinar> + 1)`

### Observaciones
![alt text](https://media.giphy.com/media/sBvF7qaDyze8M/giphy.gif "<3")
- Largo de sal random entre 32 y 64
- Si un usuario inicia chat con otro se abre una ventana para chat, si lo cierra no siguen llegando mensajes (no le interesa), pero si la vuelve a abrir puede seguir participando de la conversacion.
- Si se selecciona a mas de un amigo en el chat se crea uno grupal al seleccionar el botón de "Chat".
- Usuario solo ve salas en las que el participa y la sala comun por si no tiene amigos :( (No pude implementar la sala común)
- Un jugador sólo puede abrir un juego online al mismo tiempo.
- Para comenzar partida en un chat deben estar todos los participantes online (si ya existe sala se unen, si no existe, se crea y comienza).
- Juego avisa cuando un jugador cierra la ventana y sale del juego. Si sólo queda uno tambien.
- Si todos los participantes dibujan una vez termina la partida.
- Tiempo de 60 seg. por ronda.
- Algoritmo de similitud es la Distancia de Levenshtein con precisión menor o igual a 2 (avisa a usuario).
- No es CaseSensitive. 
- Chat del juego (sala) funciona como menú de historial. Contiene todas las partidas jugadas en esa sala junto con los chats, ganadores y dibujos ganadores.
- Al seleccionar al dibujante se le envía sólo a él cuál es la palabra que debe dibujar.

- PD. La selección de colores es mi mayor orgullo *.*. Templates, grosor y estilo de dibujo también funcionan perfectamente para todos los jugadores.

### No implementado
![alt text](https://media.giphy.com/media/zZupZVoFnuLyE/giphy.gif ":(")
* Invitar amigos
* Guardar imagen (con procesamiento de bytes)

~ Isidora Vizcaya
