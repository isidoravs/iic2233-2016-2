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
Módulo que se encarga de toda la matemática detrás del programa. Busca facilitar la vida de los usuarios que sufren día a día con cálculos demasiado difíciles para hacer a mano, de manera que puedan evitar esta frustración:

![alt text](https://media.giphy.com/media/PW24kUmUv3vlm/giphy.gif "Casi como mi frustracion haciendo esta tarea...")

Para su correcto funcionamiento importa **reduce** de la librería *functools*, **numpy** (sólo para gráficos) y **pyplot** de la librería *matplotlib*.

> **Atributos más relevantes:**

1. `operations`: lista con las operaciones básicas, según su prioridad en el cálculo. Permiten hacer las operaciones del tipo "2 + 3^2 - 6%2".
2. `other_operations`: diccionario con operaciones del tipo trigonométricas, logaritmo y exponencial, se calculan antes que las básicas. Permiten hacer el llamado a los métodos correspondientes para su cálculo en esta clase.
3. `func_commands`: diccionario con los comandos de Maplemathica, permiten llamar a los métodos correspondientes cuando se analizan ls partes del comando ingresado por el usuario.
4. `inverse_func`: diccionario del tipo *funcion: inversa*. Útil para el comando `Solve` al calcular operaciones del tipo "Cos[x] == 0".
5. `integrate` y `derivate`: diccionarios con las integrales / derivadas de operaciones trigonométricas, logaritmo y exponencial.

> **Otros atributos:**

1. `error`: permite controlar el output a imprimir cuando se produjo un error en el cálculo del comando.
2. `show_output`: permite controlar el display en consola cuando se está escribiendo en el archivo *respuestas.txt*
3. `assign_func`: permite asignar lo obtenido de integrar y derivar a funciones, de manera que no se siga calculando.

> **Métodos más relevantes:**:

En general, Maplemathica se basa en dos métodos:

### pre_calculate(self, old_command, mathematica)
Se encarga de:

* limpiar el comando para su lectura
* hacer los cambios de variables (y del valor Pi) mediante el método `eval_variables`
* dar prioridad a los cáculos entre paréntesis
* determinar errores de llamado a variables no existentes
* evaluar lo obtenido de las funciones en `func_commands`

De haber pasado el filtro de este método, se pasa a calcular lo pedido (en base a las operaciones en `operations` y `other_operations`) con el método `calculate`.

### calculate(self, old_operation)
Se encarga de:

* calcular factoriales
* calcular las operaciones en `other_operations` y luego las de `operations` con el método `all_operations`
* maneja error del tipo ZeroDivisionError
* retorna el resultado final (como float o int)

### Apartado matemático

Los siguientes métodos se basan en las series e identidades dadas en el item 5.1 y 5.2 del enunciado:

* log
* exp
* sin, cos, tan
* sec, csc
* arcsin, arccos, arctan

### `func_commands`

Algunos comentarios sobre las funciones de este tipo:

1. `abs`: permite el cálculo del valor absoluto de un número. Incluso del tipo "Abs[1 - Abs[-3]]"
2. `summatory`: permite hacer la suma de expresiones del tipo "a\*x^n + ... + n" con respecto a la variable y el intervalo dado. No permite las sumas con variables no definidas o intervalos no dados.
3. `derivate`: permite derivar expresiones trigonométricas, logaritmo y exponencial además de polinomios. Se almacena el resultado siempre en una función que luego es posible evaluar. Toma en cuanta la regla de la cadena para expresiones del tipo "Sin[2\*x^2 + 3\*x]", por ejemplo.
4. `integrate`: permite integrar expresiones trigonométricas, logaritmo y exponencial además de polinomios. Se almacena la primitiva siempre en una función. *Obs:* No evalúa según el intervalo dado ni calcula integrales multiples. Considera regla de la cadena para expresiones del tipo "Tan[2\*x]", por ejemplo.
5. `solve`: permite resolver ecuaciones. Utilizando el Teorema de la Raíz Racional otorga las posibles soluciones y luego las evalúa para desplegar en consola las raíces (racionales) correspondientes. *Obs:* no toma en cuenta el dominio dado y grados deben ser integers.
6. `plot`: permite graficar en 2D las funciones trigonométricas de la varible dada, en los intervalos y con el color/linewidth correspondiente.

* para derivar e integrar polinomios se ultizaron los métodos `set_grado` y `set_coef` que permiten representar los polinomios como un diccionario en base a los coeficientes asociados a las variables del polinomio.

*Obs:* simplify, plot3D, region_plot y piecewise no implementados.

#
![alt text](https://media.giphy.com/media/9JjnmOwXxOmLC/giphy.gif "Algo más?")

**Algunas observaciones:**

* En general, se redondean los resultados de las divisiones al quinto decimal.
* Si el archivo existe cuando se quiere guardar un estado, se reemplaza.
* Asumo que el usuario no va a ingresar errores de sintaxis distintos a los planteados en el item 7 del enunciado (están todos esos controlados)
* Si se vuelve a definir una variable con otro valor, se sobreescribe (al igual que ocurre cuando se carga un estado). Si se define una función con un nombre de una función ya definida, se sobreescribe (sin importar la cantidad de variabes).
* Al leer *consultas.txt* no se van eliminando las variables/funciones, sólo sobreescriben las correspondientes. (Si se eliminan el terminar *resultados.txt*)
* Si una la lectura de *consultas.txt* falla, comentar línea 11 de `consola.py` para continuar con el intérprete.
* Permite guardar variables del tipo "a = f[1,2]; 

> Y este es el intérprete Maplemáthica! Espero que sea de gran utilidad.

![alt text](https://media.giphy.com/media/k1bSa7EHfYHh6/giphy.gif "Like a Bob")

Se despide,

Isidora Vizcaya.
