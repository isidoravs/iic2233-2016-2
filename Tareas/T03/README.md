# Tarea 3
![alt text](http://67.media.tumblr.com/30835bf9e8d809a6f944a921a80a650c/tumblr_inline_o0eoxv67QK1tbe472_500.gif "MAPLEMATHICA")
> Bienvenido a este nuevo (y completamente original) intérprete interactivo: Maplemathica!
> Para lograrlo, las distintas clases y sus métodos, además de otras funciones, se dividen en **3** módulos:

```
consola.py
```
Módulo principal (**el que se debe ejecutar**) que contiene las clase **Menu** que controla la interacción con el usuario con el método `run`.
Antes de pedir los comandos al usuario, Maplemathica carga las concultas de *consultas.txt* y escribe las respuestas en *resultados.txt* 
(con los métodos `consulta` y `decide_action`).
Luego borra las variables y funciones definidas en los estados del archivo de consultas para que el usuario comience con sus comandos desde cero.

El primer lugar, se distinguen 5 opciones cuando se ingresa un comando:

1. `"?" in comando`: entrega una descripción del comando dado, en base a lo guardado en el archivo *help.txt*.
2. `"load" in comando`: permite cargar un estado guardado en los archivos (de la carpeta *archivos*).
3. `"save" in comando`: permite guardar el estado actual en un .txt en la carpeta archivos.
4. `"exit" in comando`: permite salir del programa.
5. `else`: el usuario ha ingresado un comando para calculo o definición de variables/funciones. El método `opcion_consulta` determina si hace
falta *;* a la instrucción y luego de calcular, despliega los resultados en la consola o los escribe en *resultados.txt* de estar leyendo el 
archivo de consultas.

```
interprete.py
```
![alt text](https://media.giphy.com/media/AXorq76Tg3Vte/giphy.gif "MAPLEMATHICA")

Este módulo permite la determinar que busca el usuario con el comando ingresado. Almacena las **variables** y **funciones** en diccionaros como atributos de la clase.

El método principal `get_command` distingue entre estas opciones principales:

1. `"_]" in command`: define una función. En caso de ser una integral o derivada, la calcula en función de la variable y alamcena en el diccionario de funciones correspondiente.
2. `"[[" in command`: define una matriz. La parsea y almacena en el diccionario de variables (reemplaza las variables en caso de no ser todas sus entradas numéricas).
3. `True in [key in command for key in self.consultas_matriz]`: determina si se pide calcular alguna caracterísitica de las matrices y la asigna a su función correspondiente (*Obs:* Det, Range e Inv no implementados).
4. `"Who" in command`: despliega las variables con el método `show_variables`.
5. `"Clear" in command`: determina si se borra una variable/función específica o todas.
6. `"=" in command`: principalmente distingue entre operadores booleanos (que retornan *True* o *False* a la comparación del usuario) y definición de variables (para calcular su valor y almacenar en el diccionario correspondiente).
7. `len([x for x in self.consultas if x in command]) > 0`: determina si hay una consulta booleana y llama a los métodos **MCM**, **MCD** o **isdivisible** según corresponda.
8. `else`: funciona como **calculadora**, retorna el resultado al cálculo pedido por el usuario.


```
calculo.py
```
Módulo que se encarga de toda la matemática detrás del programa. Busca facilitar la vida de los usuarios para que eviten pasar por esta frustración:
![alt text](https://media.giphy.com/media/a8749TBnyEIY8/giphy.gif "MAPLEMATHICA")


