# Tarea 4
> Bienvenido a esta simulación de la **Guerra de dioses**!
> En éste se enfrentan las razas de humanos, orcos y muertos vivientes, mientras los dioses se entretienen al ver el mundo arder.
> Para lograrlo, las distintas clases y sus métodos, además de otras funciones, se dividen en **7** módulos:

```
main.py
```
Módulo principal (**el que se debe ejecutar**) que contiene la clase `Simulacion` encargada del funcionamiento principal de la tarea. Se encarga de inicializar ambos ejércitos, los primeros aldeanos, mapa, objetivo, ganador, mostrar estadísticas y además coordinar la estrategia de los humanos (cuando son 3/4 del ejercito enemigo (mínimo) dividen su ejército para dejar defensores en la base).

* `tick()`: método encargado de controlar la ocurrencia de eventos en cada tick de ejecución (*simulación síncrona*). Para controlar el paso del tiempo utiliza un contador; cada 7 ticks de simulación aumenta un segundo de simulación (para darle mayor realidad a los eventos que ocurren).

**Obs:**

* Primer ejército en lograr objetivo permite que su dios utilice el poder asignado y descargue su furia contra la humanidad. Luego se determina un nuevo objetivo y comienza desde cero el conteo (el atributo `objective_qty` del ejército lleva conteo de lo logrado del objetivo). Este objetivo no afecta en la personalidad de las razas, no buscan *directamente* cumplir el objetivo.

* Asumo que en mapa siempre se darán las 4 construcciones iniciales (issue \#402)

* Una raza se declara ganadora si destruye el templo enemigo. Si acaba el tiempo y ninguno lo ha logrado es un empate (sería injusto considerar las muertes o el oro, dado que cada raza tiene su estrategia para llegar al templo).

* Cuando se cumple la condición de los humanos para atacar, se manda a la mitad (o mitad menos uno en caso de impar) más **rápida** de las unidades de combate al templo (no deja a los mas debiles). Los defensores (no puede ser el héroe) se dividen entre templo, cuartel y torretas (si alguno de los anteriores esta en construccion, van al templo). Ellos buscan en campo de vision y persiguen si estan cerca de la edificacion que defienden (deambulan cerca de la edificación correspondiente gracias al método `random_move`).

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

```
ejercito.py
```





### Valores asignados
`HP`:
