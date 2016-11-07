# Tarea 5
![alt text](https://scontent.fgru3-1.fna.fbcdn.net/t31.0-8/15016356_1217287821650869_4907137500733162404_o.jpg =250x "HackerTanks!")
{:height="36px" width="36px"}

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

```
tanks.py
```
Este módulo contiene la clase `Tank` que cuenta con tre métodos principales: **make_movement** que controla el movimiento del tanque segun su tipo, **in_vision** que para los tanques enemigos termina si el principal está en su rango de ataque (retorna un booleano) y **start_shooting** que retorna una instancia de la clase `Bala` cuando debe comenzar a disparar (las balas enemigas tienen una línea blanca para distinguirlas y las del tanque principal cambian de color según su tipo - se ve en la tienda).
```
power_ups.py
```
Modela la mayoría de los elementos extra que forman parte del juego. Contiene las clases:

* `Bomb`: cuenta con atributos como daño, rango de ataque y tiempo para explotar
* `Explotion`: permite la aparición de explosiones en caso de bomba, bala explosiva y colisión de balas
* `Bullet`: su método principal *shoot_move* permite el movimiento de la bala en el juego y su detención cuando corresponde (choca con paredes -excepto bala penetrante-, ataca a enemigo o colisiona una bomba).
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
