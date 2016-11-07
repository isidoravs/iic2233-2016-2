# Tarea 5
<img src="https://scontent.fgru3-1.fna.fbcdn.net/t31.0-8/15016356_1217287821650869_4907137500733162404_o.jpg" width="800" height="600" />

> Bienvenido a **HackerTanks**!
> Para lograrlo, las distintas clases y sus métodos, además de otras funciones, se dividen en **9** módulos:


### T05
```
main.py
```
Módulo principal (**el que se debe ejecutar**). Contiene la clase `HackerTanks` que se encarga de la lógica del juego. Determina las acciones que llevan a cabo tanques, balas y bombas, además de setear las caracterísitcas de cada etapa o modo survival.

### T05/gui
```
__init__.py
```
Módulo que permite la interacción entre el *main.py* y los métodos y clases del módulo `main_window.py`. 

```
main_window.py
```
Contiene la clase `MainWindow` que hereda de *QWidget*. Controla la ventana principal del juego y sus cambios cuando el usuario selecciona modo/etapa. Son de special importancia los métodos `keyPressEvent` y `mousePressEvent` que permiten al usuario controlar al tanque principal (azul). Esta clase cuenta con los métodos `start`, `pause`, `restart`, `submit` y `quit` que están conectadas a los distintos botones para un buen desarrollo del juego.

```
store.py
```
En este módulo está la clase `Store` que hereda de *QWidget* y controla la ventana de la tienda. Permite comprar balas especiales y bombas, además de aumentar los stats del tanque principal. Avisa cuando no se tienen puntos suficientes y actualiza el puntaje luego de una compra exitosa. Al cerrar, el juego se encuentra en pausa.
<img src="https://scontent.fgru3-1.fna.fbcdn.net/t31.0-8/14918915_1217287888317529_5701768199751596402_o.jpg" width="900" height="500" />

*Lo más lindo que he hecho en esta tarea!*

```
tanks.py
```
Este módulo contiene la clase `Tank` que cuenta con tre métodos principales: **make_movement** que controla el movimiento del tanque segun su tipo, **in_vision** que para los tanques enemigos termina si el principal está en su rango de ataque (retorna un booleano) y **start_shooting** que retorna una instancia de la clase `Bala` cuando debe comenzar a disparar (las balas enemigas tienen una línea blanca para distinguirlas y las del tanque principal cambian de color según su tipo - se ve en la tienda).

```
power_ups.py
```
Modela la mayoría de los elementos extra que forman parte del juego. Contiene las clases:

* `Bomb`: cuenta con atributos como daño, rango de ataque y tiempo para explotar

* `Explotion`: permite la aparición de explosiones en caso de bomba, bala explosiva y colisión de balas (Causa daño de 5 puntos, es preciosa!).

* `Bullet`: su método principal *shoot_move* permite el movimiento de la bala en el juego y su detención cuando corresponde (choca con paredes -excepto bala penetrante-, ataca a enemigo o colisiona una bomba). Su daño es proporcional a la distancia desde la que fue lanzado.

* `Portal`: funciona similar a una bala pero no causa daño. Cambia su pixmap al encontrar una pared. Como pide el enunciado, sólo se pueden lanzar dos portales por etapa (pero si choca a enemigo desaparece y otorga otra oportunidad de lanzamiento al tanque).

* `PowerUp`: las instancias de esta clase son los elementos que aparecen aleatoriamente en el juego y pueden ser recogidos por el tanque principal. Estos son: balas especiales y monedas (**250** puntos). *Obs:* escudo no implementado.

```
environment.py
```
Contiene la clase `Wall` que define bordes y paredes de cada etapa. Segun sea destructible o no determina su imagen en la interfaz y el poder ser removida al momento de explotar una bomba o que un **Black Tank** (tanque_grande) la atraviese.

```
entity.py y utils.py
```
Módulos muy similares a los entregados en la T04. Permiten obtener path de archivos (*utils*) y las características que comparten todas las entidades como tanques, balas, bombas y paredes (cuyas clases heredan de ésta). 

### T05/gui/assets
La licencia de uso de los assets se encuentra en la carpeta *Kenney_topdownTanks*.

* Tanque principal

<img src="https://goo.gl/eS1oo2" width="150" height="150" />

* Tanque quieto

<img src="https://goo.gl/IvRCnU" width="150" height="150" />

* Tanque círculo

<img src="https://goo.gl/NcEr0Y" width="150" height="150" />

* Tanque guiador

<img src="https://goo.gl/usKv6h" width="150" height="150" />

* Tanque grande

<img src="https://goo.gl/XKPFQQ" width="200" height="200" />

* Bomba

<img src="https://goo.gl/C4Bm73" width="150" height="150" />

* Entrada a la tienda:

<img src="https://goo.gl/82YoSd" width="150" height="150" />

### Observaciones:

1. Controles (cambiados para mayor comodidad):

| Tecla         | Efecto        |
| ------------- |:-------------:|
| A             | izquierda     |
| D             | derecha       |
| W             | adelante      |
| S             | atras         |
| Left click    | disparo       |
| Right click   | bomba         |
| Enter         | portal        |

2. Tanque principal siempre comienza en esquina superior izquieda y 200 hp. Los tanques enemigos comienzan con 75 hp (excepto el tanque grande que parte con 100).

3. El archivo *constantes.txt* contiene tiempo máximo por etapa, stats con que comienza cada tanque (segun id: 0 azul, 1 quieto, 2 circulo, 3 guiador y 4 grande), daño standard de bomba, bombas con que comienza el tanque principal (tanques enemigos no tienen bombas y cuentan con infinitas balas) y puntaje por muerte de cada tanque enemigo (en el orden mencionado). Además tiene la contante de comienzo de balas (ésta se multiplica según el número de etapa).

4. Bomba muestra en barra tiempo para explotar (excepto que una bala lo colisione). En cas de que un tanque pase sobre una bomba no explota (sería fome la estartegia de juego).

5. Algunas contantes no modificables son: inicio con 200 puntos, cooldown de tienda dura 10 segundos (**tiempo se mide en segundos durante todo el juego**) y bonificación por completar todos los niveles es de 1000 puntos (da lo mismo el orden, se lleva registro de los niveles pasados, si pasa último nivel y no los ha completado todos, empieza uno que no haya ganado).
