# Tarea 4
> Bienvenido a esta simulación de la **Guerra de dioses**!
> En éste se enfrentan las razas de humanos, orcos y muertos vivientes, mientras los dioses se entretienen al ver el mundo arder.
> Para lograrlo, las distintas clases y sus métodos, además de otras funciones, se dividen en **7** módulos:

```
main.py
```
Módulo principal (**el que se debe ejecutar**) que contiene la clase `Simulacion` encargada del funcionamiento principal de la tarea. Se encarga de inicializar ambos ejércitos, los primeros aldeanos, mapa, objetivo, ganador, mostrar estadísticas y además coordinar la estrategia de los humanos (cuando son 3/4 del ejercito enemigo (mínimo) dividen su ejército para dejar defensores en la base).

`tick()`: método encargado de controlar la ocurrencia de eventos en cada tick de ejecución (*simulación síncrona*). Para controlar el paso del tiempo utiliza un contador; cada 7 ticks de simulación aumenta un segundo de simulación (para darle mayor realidad a los eventos que ocurren).

**Obs:**

* Primer ejército en lograr objetivo permite que su dios utilice el poder asignado y descargue su furia contra la humanidad. Luego se determina un nuevo objetivo y comienza desde cero el conteo (el atributo `objective_qty` del ejército lleva conteo de lo logrado del objetivo). Este objetivo no afecta en la personalidad de las razas, no buscan *directamente* cumplir el objetivo.

* Asumo que en mapa siempre se darán las 4 construcciones iniciales (issue \#402)

* Una raza se declara ganadora si destruye el templo enemigo. Si acaba el tiempo y ninguno lo ha logrado es un empate (sería injusto considerar las muertes o el oro, dado que cada raza tiene su estrategia para llegar al templo).

* Cuando se cumple la condición de los humanos para atacar, se manda a la mitad (o mitad menos uno en caso de impar) más **rápida** de las unidades de combate al templo (no deja a los mas debiles). Los defensores (no puede ser el héroe) se dividen entre templo, cuartel y torretas (si alguno de los anteriores esta en construccion, van al templo). Ellos buscan en campo de vision y persiguen si estan cerca de la edificacion que defienden (deambulan cerca de la edificación correspondiente gracias al método `random_move`).

* Las tasas de creación y muertes por raza consideran a todas las unidades del ejército (aldeanos, guerreros, arqueros, mascotas y heroe).

```
inicio.py
```
Módulo encargado de controlar la interacción por consola antes de inciar la simulación. Pide el *tiempo* máximo de simulación, *dios* de cada ejército, *poder* de cada dios (issue \#390) y *raza* de cada ejército. Estos últimos no se pueden repetir entre ambos ejércitos. Además pide el intervalo de creación *guerreros:arqueros:mascotas* y la tasa de creación del héroe (**segundos** para su aparición y reaparición en caso de muerte).

Este módulo maneja las **excepciones** pedidas en el enunciado.

```
ejercito.py
```
Modulo encargado de modelar las funcionalidades de ambos ejércitos, mediante la clase **Inicio**. Toma la información inicial dada por el usuario e inicializa las condiciones cada "army". Lleva la cuenta de las estadísticas por raza y tiene como atributos distintas listas con aldeanos, guerreros, arqueros, mascotas y torretas. Además guarda en distintos atributos al héroe (instancia de la clase **Hero**), templo (instancia de la clase **Templo**), cuartel (instancia de la clase **Cuartel**) y mina (instancia de la clase **Mina**). 

Tiene distintas properties como `gold`, `total_units`, `villager_qty`, `all_buildings` (retorna booleano que determina si el ejército cuenta con cuartel y torretas, no en estado de construcción), `complete_army` (retorna una lista con todas las unidades de esta raza) y `war_units` (retorna lista con todas las unidades de combate del ejército, todas menos los aldeanos).

### Métodos importantes
* `creation_cicle`: encargado de la creación de unidades. Cumple con las condiciones dadas en el enunciado (mínimo 6 aldeanos, verifica que haya oro suficiente, que cumpla con la cantidad máxima de unidades mediante *set_max_units*)

* `hero_arrival`: encargado de controlar la llegada del héroe y reaparición en caso de que muera.

* `count_troops`: determina la cantidad de muertos en cada paso de segundo y los elimina de las tropas del ejército.

* `activate_power` / `desactivate_power`:  se encarga de controlar los efectos del poder del dios y su activación/desactivación dependiendo del rango de tiempo que dure (generalmente un número aleatorio entre 8 y 15 segundos)

* `show_power_effectiveness`: calcula la efectividad del poder. Para cada uso se calcula la cantidad de muertos en caso de **plaga**, **berserker** y **glaciar**, en caso de **terremoto** el daño a edificios y para **revivir** la cantidad de muertos invocados. Si el poder se utiliza más de una vez, muestra el promedio de efectividades.

### Poderes
Algunos comentarios sobre los poderes de los dioses:

* **Plaga**: las unidades afectadas por la plaga disminuyen su *hp* en **8** por segundo, mientras que su *move* disminuye en **1** unidad en total. Luego de ésta recuperan la mitad del *hp* que tenían antes de la plaga.

* **Terremoto**: las edificaciones (no mina), sufren un daño de **10** por segundo.

* **Invocar a los muertos**: revive a los aldeanos, guerreros, arqueros o mascotas que correspondan. Éstas aparecen en el templo o cuartel según su tipo de unidad. 

```
unidades.py
```
Módulo que contiene las clases **Warrior**, **Archer** y **Pet**. Las tres determinan las carácterísticas de las unidades de combate y cuentan con métodos iguales o muy similares (se testean variadamente en el módulo de testeo explicado más adelante). Se diferencian principalmente en sus atributos:

1. `move`: cantidad de movimientos por segundo. Número aleatorio entre: (2, 7) *warriors*, (2, 7) *archers* y (3, 6) *pets*. Disminuye en uno cuando es de raza **Orc** o aumenta en uno cuando es de raza **Skull**.
2. `hp`: Vida de las unidades. Número aleatorio entre: (150, 250) *warriors*, (100, 200) *archers* y (100, 200) *pets*.
3. `harm`: Daño que hace una unidad a un enemigo por segundo de simulación. Número aleatorio entre: (3, 8) *warriors*, (2, 6) *archers* y (2, 7) *pets*. Aumenta en uno cuando es de raza **Orc**.
4. `creation_time`: tiempo de creación dado en el enunciado.
5. `cost`: costo de creación dado en el enunciado
6. `attack_range` / `shoot_range`: rango de ataque (o disparo en caso de arqueros), cuando enemigos se encuentran dentro de éste son atacados. Número aleatorio entre: (50, 80) *archers* y (20, 40) *pets*, en *warriors* es fijo 15 para que no sea necesario estár justo sobre otro al atacar. 
7. `vision_range`: rango de visión de la unidad, permite identificar enemigos o aliados cerca. Útil para que orcos persigan a el enemigo más cercano dentro de ese rango o mascota defienda al aliado más cercano que es vulnerable o está siendo atacado (*rabia*). Valor de 50 para *warriors* y *archers*, 70 para *pets*.
8. `unit`: almacena un objeto de la clase **Human**, **Orc** o **Skull** según la raza del ejército. Es el que luego es agregado a la interfaz gráfica y altera sus coordenadas y hp (que determina la property *health* de la clase **Warrior**, **Archer** o **Pet**). 

El método más importante de las clases en este módulo (que es similar en las 3) es:

`self.avanzar(race, enemy_temple, enemy_barrack, enemy_towers, enemy_army, allies)`

Controla la cantidad de movimientos y/o acciones que debe llevar a cabo la unidad en cada segundo. Se rige por lo pedido en el enunciado y según cada raza se determina la estrategia a utilizar.

### Human
![alt text](https://media.giphy.com/media/kzaSXi0M3FFXG/giphy.gif "Humano")

Los humanos cuando van a atacar avanzan al templo. Si hay un enemigo en su rango de ataque (que es menor al de vision) ataca y hace daño a éste pero continúa su rumbo al templo. Si hay torretas o cuarteles cerca los ataca también pero su objetivo es el templo.

### Orc
![alt text](https://media.giphy.com/media/3oEdvdm6gpQFguAK5i/giphy.gif "Orco")

A los orcos le interesa ir al templo (en un comienzo se dirigen a éste para ir a atacar), pero si ve a algún enemigo (éste se encuentra en su campo de visión) cambia su foco y va directamente a atacarlo (`move_near`). Sólo puede dañarlo si está en su rango de ataque, pero el orco siempre persigue al enemigo más cercano en su rango de visión. Si el templo, torreta o cuartel están más cerca en su campo de visión que el enemigo cambian su foco de ataque y van hacia estas edificaciones. Son los más fuertes y por lo tanto causan más daño. Como son los más lentos, las unidades enemigas pueden escapar de éstos (saliendo de su campo de visión). Buscan pelear hasta la muerte si el enemigo está a asu alcance.

### Skull
![alt text](https://media.giphy.com/media/qTD9EXZRgI1y0/giphy.gif "Muerto Viviente")

Los muertos vivientes sólo buscan destruir el templo. Siempre buscan evitar al enemigo más cercano de su campo de visión (se alejan de él: `move_far`). Sin embargo, si hay enemigos u otras edificaciones enemigas en su rango de ataque no dudarán en dañarlas (manteniendo su dirección al templo).

```
otras_unidades.py
```
Módulo que contiene las clases:

1. **Villager**:
Los aldeanos cuentan con velocidad, hp, creation_time, cost y unit al igual que las otras unidades. Pero además cuentan con los siguientes atributos:

* `collect`: tiempo entre 5 y 10 segundos que demoran en sacar oro de la mina
* `strenght`: capacidad de carga de oro que pueden transportar al templo.
* `construction`: cantidad de piezas que aporta a la construcción de las edificaciones.
* `working` / `building`: atributo que determina si el aldeano está sacando oro o construyendo edificios.

También cuenta con el método `avanzar` que es distinto al de las otras unidades, debido a que no atacan a los enemigos y sólo transitan entre su mina y el templo, sacando y dejando oro. Además se encargan de ir a reconstruir las torretas o el cuartel si han sido destruidos (su hp debe haber llegado a 0, no reconstruyen si el hp es menor al total). **Obs:** si estas edificaciones están en construcción no pueden ser atacadas por los enemigos, son el único gasto que permite deuda (quedan con saldo negativo de oro si no tienen suficiente para pagar la reconstrucción). 

Como `construction` determina la cantidad de piezas que aporta a la construcción de la edificación, si hay más aldeanos reconstruyendo ésta es terminada en menor tiempo. **Obs:** Los aldeanos no buscan construir más torretas que las con que parten la simulación. Son completamente sacrificados, si están construyendo y son atacados, continúan con su trabajo... *aunque sea hasta la muerte*. 

2. **Hero**:
Los objetos de esta clase cuentan con atributos y métodos muy similares a los de las otras unidades. Según su raza poseen distintas características (menor `harm` en el caso de Crsitián y menor `hp` en el caso de Hernán, dado que tiene tres vidas). Sin emabrgo su principal diferencia son los poderes con los que cuentan, éstos se determinan por `set_power_info` y `avanzar`. 

* *Cristián*: para su ritual debe permanecer quieto por **5** segundos con el enemigo en su rango de vision (mas reducido que otros, **25**). Para esto necesita total concentración, por lo tanto encuentra al enemigo más cercano en su rango y lo trata de convertir (unidad enemiga guardada en el atributo `objective`). Si otras unidades enemigas se cruzan en medio del ritual, este mago igual ataca. Su clon no tiene el poder pero tiene sus mismos atributos y apariencia (mitad del hp).

* *Manu*: puede tener máximo dos mascotas protectoras a su lado (no agregar si siguen vivas). Cuando mueren ambas empieza el tiempo para nueva invocación de éstas (**30** segundos). Si este héroe muere, las mascotas mueren con él. Ellas siguen siempre a Manu protegiéndolo de los enemigos que estén dentro de sus rangos de ataque (mayor al de las mascotas comunes).

* *Hernán*: tiempo en resucitar va a ser un tercio (aprox) de la tasa de invocacion del héroe. Éste revive en el mismo lugar en que murió (almacenado en el atributo `death_cord`).

```
edificaciones.py
```
Módulo que contiene las siguientes clases:

1. `Cuartel`: hereda de **Building**. Tiene *hp* = 500, *cost* = 100 y *construction_time* = 80 (piezas para terminar su construcción). Además el atributo `work_on` lleva el conteo de cuántas piezas se han construido en caso de que los aldeanos estén trabajando en esta edificación.

2. `Torreta`: hereda de **Building**. Tiene *hp* = 400, *cost* = 150, *construction_time* = 60 (piezas para terminar su construcción) y el mismo atributo `work_on`. Además cuenta con los atributos `attack_speed` que determina la cantidad de ataques por segundo, `harm` que es el daño que produce al enemigo (calculado en base a *speed*) y `shoot_range` que es su rango de ataque (radial, como todos los rangos en la tarea).

Cuenta con los métodos: `check_perimeter(self, enemy_army)` y `in_perimeter(self, enemy)` que permiten a la torreta atacar a los enemigos que se encuentren dentro de su rango de ataque.

3. `Mina`: hereda de **Building**. La mina no puede ser atacada y es indestructible (incluso en caso de terremoto).

4. `Templo`: hereda de **Temple**. Cuenta con un *hp* inicial de 1250.

### Testeo
En el módulo `test_module.py` llevo a cabo el testeo de mi simulación. Se testea más del 50% de las funciones implementadas. 

**No implementado**: Cómo afecta la personalidad de los dioses en los ejércitos (únicamente cambia razón de creación de unidades en caso de que GodessFlo sea la diosa de uno de los dos ejércitos).
