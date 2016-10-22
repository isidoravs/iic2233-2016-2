import gui
from gui.kinds.human import Human
from gui.kinds.skull import Skull
from gui.kinds.orc import Orc
from random import randint, choice
from math import sqrt
from edificaciones import Torreta, Cuartel
from unidades import Pet


class Villager:  # NO es parte del ejercito
    def __init__(self, army):
        self.army = army
        self.move = randint(2, 5)
        self.hp = randint(60, 120)
        self.collect = randint(5, 10)  # tiempo recolectando
        self.construction = 3 + randint(-2, 2)  # fraccion de tiempo menos o mas que se demora
        self.strength = 10 + randint(-5, 5)  # base 10
        self.creation_time = 5
        self.cost = 10
        self.unit = None

        self.load = 0  # oro que lleva
        self.working = -1  # tiempo dentro de la mina
        self.building = -1  # tiempo construyendo
        self.job = None
        self.under_attack = False
        self.new_building = None

    @property
    def health(self):
        return self.unit.health

    def add_villager(self, race, x_pos, y_pos):
        if race == "Human":
            villager = Human('villager', (x_pos, y_pos), hp=self.hp)

        elif race == "Orc":
            self.move -= 1
            villager = Orc('villager', (x_pos, y_pos), hp=self.hp)

        else:
            self.move += 1
            self.hp -= 10
            villager = Skull('villager', (x_pos, y_pos), hp=self.hp)

        self.unit = villager
        return villager

    def avanzar(self, mine_location, temple_location, army):  # aldeanos solo van a la mina y vuelven
        if self.working == -1 and self.building == -1:  # no estan dentro de la mina ni construyendo
            if army.all_buildings:  # determina si ejercito tiene todos los edificios
                for _ in range(self.move):  # toma en cuenta velocidad
                    if self.load == 0:  # no lleva oro, se debe dirigir a la mina
                        if mine_location[0] == self.unit.cord_x:
                            if mine_location[1] > self.unit.cord_y:
                                self.unit.cord_y += 1
                            elif mine_location[1] == self.unit.cord_y:
                                # llega a la mina
                                self.working = 0
                                self.unit.hide()
                                break
                            else:  # <
                                self.unit.cord_y -= 1

                        elif mine_location[0] > self.unit.cord_x:
                            if mine_location[1] > self.unit.cord_y:
                                self.unit.cord_x += 1
                                self.unit.cord_y += 1
                            elif mine_location[1] == self.unit.cord_y:
                                self.unit.cord_x += 1
                            else:  # <
                                self.unit.cord_x += 1
                                self.unit.cord_y -= 1

                        elif mine_location[0] < self.unit.cord_x:
                            if mine_location[1] > self.unit.cord_y:
                                self.unit.cord_x -= 1
                                self.unit.cord_y += 1
                            elif mine_location[1] == self.unit.cord_y:
                                self.unit.cord_x -= 1
                            else:  # <
                                self.unit.cord_x -= 1
                                self.unit.cord_y -= 1

                    else:
                        if temple_location[0] == self.unit.cord_x:
                            if temple_location[1] > self.unit.cord_y:
                                self.unit.cord_y += 1
                            elif temple_location[1] == self.unit.cord_y:
                                army.gold += self.load
                                army.objective_qty += self.load
                                self.load = 0  # reinicia

                            else:  # <
                                self.unit.cord_y -= 1

                        elif temple_location[0] > self.unit.cord_x:
                            if temple_location[1] > self.unit.cord_y:
                                self.unit.cord_x += 1
                                self.unit.cord_y += 1
                            elif temple_location[1] == self.unit.cord_y:
                                self.unit.cord_x += 1
                            else:  # <
                                self.unit.cord_x += 1
                                self.unit.cord_y -= 1

                        elif temple_location[0] < self.unit.cord_x:
                            if temple_location[1] > self.unit.cord_y:
                                self.unit.cord_x -= 1
                                self.unit.cord_y += 1
                            elif temple_location[1] == self.unit.cord_y:
                                self.unit.cord_x -= 1
                            else:  # <
                                self.unit.cord_x -= 1
                                self.unit.cord_y -= 1
            else:  # debe ir a construir
                if army.cuartel is None:
                    coord = army.cuartel_location
                    for _ in range(self.move):
                        if coord[0] == self.unit.cord_x:
                            if coord[1] > self.unit.cord_y:
                                self.unit.cord_y += 1
                            elif coord[1] == self.unit.cord_y:
                                # llega a cuartel para reconstruir (primero)
                                new_cuartel = Cuartel(coord[0], coord[1])  # crea nuevo
                                new_cuartel.in_construction = True
                                army.cuartel = new_cuartel
                                self.building = 0
                                self.job = new_cuartel
                                self.new_building = new_cuartel
                                break
                            else:  # <
                                self.unit.cord_y -= 1

                        elif coord[0] > self.unit.cord_x:
                            if coord[1] > self.unit.cord_y:
                                self.unit.cord_x += 1
                                self.unit.cord_y += 1
                            elif coord[1] == self.unit.cord_y:
                                self.unit.cord_x += 1
                            else:  # <
                                self.unit.cord_x += 1
                                self.unit.cord_y -= 1

                        elif coord[0] < self.unit.cord_x:
                            if coord[1] > self.unit.cord_y:
                                self.unit.cord_x -= 1
                                self.unit.cord_y += 1
                            elif coord[1] == self.unit.cord_y:
                                self.unit.cord_x -= 1
                            else:  # <
                                self.unit.cord_x -= 1
                                self.unit.cord_y -= 1

                elif None in army.torretas:
                    i = army.torretas.index(None)
                    coord = army.torretas_location[i]
                    for _ in range(self.move):
                        if coord[0] == self.unit.cord_x:
                            if coord[1] > self.unit.cord_y:
                                self.unit.cord_y += 1
                            elif coord[1] == self.unit.cord_y:
                                # llega a torreta para reconstruir (primero)
                                new_torreta = Torreta(coord[0], coord[1])  # crea nueva
                                new_torreta.in_construction = True
                                army.torretas[i] = new_torreta
                                self.building = 0
                                self.job = new_torreta
                                self.new_building = new_torreta
                                break
                            else:  # <
                                self.unit.cord_y -= 1

                        elif coord[0] > self.unit.cord_x:
                            if coord[1] > self.unit.cord_y:
                                self.unit.cord_x += 1
                                self.unit.cord_y += 1
                            elif coord[1] == self.unit.cord_y:
                                self.unit.cord_x += 1
                            else:  # <
                                self.unit.cord_x += 1
                                self.unit.cord_y -= 1

                        elif coord[0] < self.unit.cord_x:
                            if coord[1] > self.unit.cord_y:
                                self.unit.cord_x -= 1
                                self.unit.cord_y += 1
                            elif coord[1] == self.unit.cord_y:
                                self.unit.cord_x -= 1
                            else:  # <
                                self.unit.cord_x -= 1
                                self.unit.cord_y -= 1

                elif True in [t.in_construction for t in army.torretas]:
                    # encuentra la torreta en construccion y deben ir hacia ella
                    job = [t for t in army.torretas if t.in_construction]
                    coord = army.torretas_location[army.torretas.index(job[0])]
                    for _ in range(self.move):
                        if coord[0] == self.unit.cord_x:
                            if coord[1] > self.unit.cord_y:
                                self.unit.cord_y += 1
                            elif coord[1] == self.unit.cord_y:
                                # llega a torreta en construccion
                                self.building = 0
                                self.job = job[0]
                                break
                            else:  # <
                                self.unit.cord_y -= 1

                        elif coord[0] > self.unit.cord_x:
                            if coord[1] > self.unit.cord_y:
                                self.unit.cord_x += 1
                                self.unit.cord_y += 1
                            elif coord[1] == self.unit.cord_y:
                                self.unit.cord_x += 1
                            else:  # <
                                self.unit.cord_x += 1
                                self.unit.cord_y -= 1

                        elif coord[0] < self.unit.cord_x:
                            if coord[1] > self.unit.cord_y:
                                self.unit.cord_x -= 1
                                self.unit.cord_y += 1
                            elif coord[1] == self.unit.cord_y:
                                self.unit.cord_x -= 1
                            else:  # <
                                self.unit.cord_x -= 1
                                self.unit.cord_y -= 1

                elif army.cuartel.in_construction:
                    # encuentra la cuartel en construccion y deben ir hacia ella
                    coord = army.cuartel_location
                    for _ in range(self.move):
                        if coord[0] == self.unit.cord_x:
                            if coord[1] > self.unit.cord_y:
                                self.unit.cord_y += 1
                            elif coord[1] == self.unit.cord_y:
                                # llega a cuartel en construccion
                                self.building = 0
                                self.job = army.cuartel
                                break
                            else:  # <
                                self.unit.cord_y -= 1

                        elif coord[0] > self.unit.cord_x:
                            if coord[1] > self.unit.cord_y:
                                self.unit.cord_x += 1
                                self.unit.cord_y += 1
                            elif coord[1] == self.unit.cord_y:
                                self.unit.cord_x += 1
                            else:  # <
                                self.unit.cord_x += 1
                                self.unit.cord_y -= 1

                        elif coord[0] < self.unit.cord_x:
                            if coord[1] > self.unit.cord_y:
                                self.unit.cord_x -= 1
                                self.unit.cord_y += 1
                            elif coord[1] == self.unit.cord_y:
                                self.unit.cord_x -= 1
                            else:  # <
                                self.unit.cord_x -= 1
                                self.unit.cord_y -= 1

        elif self.working != -1:  # esta trabajando
            self.working += 1
            if self.working == self.collect:  # termino de recolectar
                self.working = -1
                self.unit.show()
                # lleva cierta cantidad de oro
                self.load = self.strength  # depende de su fuerza
                army.gold_extraction[-1] += self.load  # a ultimo minuto

        elif self.building != -1:  # esta construyendo
            if self.job is not None and self.job.in_construction:
                self.job.work_on += self.construction  # agrega trabajo de este aldeano
                if self.job.work_on == self.job.construction_time:  # termino de construir
                    self.job.in_construction = False

                    self.job.work_on = 0
                    self.job = None
                    self.building = -1
            else:  # otro aldeano la termino
                self.job = None
                self.building = -1

        return


class Hero:  # unico por especie
    def __init__(self, army, race):
        self.race = race
        self.army = army
        self.name = ""
        self.move = randint(3, 8)
        self.hp = randint(175, 250)  # cambia en caso de Hernan
        self.harm = randint(3, 10)  # cambia en caso de Cristian
        self.attack_range = 15
        self.vision_range = 50
        self.power_info = None  # diccionario con caracteristicas a cada uno
        self.define_hero()
        self.under_attack = False
        self.unit = None
        self.attack_temple = False
        self.death_cord = None
        self.clone = False

        self.aux_clock = 0
        self.new_entity = []
        self.pets = []
        self.objective = None
        self.enemy_to_clone = None

    @property
    def health(self):
        return self.unit.health

    def define_hero(self):
        if self.race == "Human":
            self.name = "Cristian"
            self.harm = 2  # daño reducido
            self.set_power_info("cloning")

        elif self.race == "Orc":
            self.move -= 1
            self.harm += 1
            self.name = "Manu"
            self.set_power_info("pets")

        else:  # Skull
            self.move += 1
            self.name = "Hernan"
            self.hp = randint(150, 200)  # porque tiene tres vidas
            self.set_power_info("revive")
        return

    def set_power_info(self, power):
        if power == "cloning":
            self.power_info = {'time': 5}

        elif power == "pets":
            self.power_info = {'time': 30}

        elif power == "revive":
            self.power_info = {'time': 40}
            self.lives = 3

        self.power_info['name'] = power
        return

    def add_hero(self, race, x_pos, y_pos):
        if race == "Human":
            self.vision_range = 30
            hero = Human('hero', (x_pos, y_pos), hp=self.hp)

        elif race == "Orc":
            self.move -= 1
            hero = Orc('hero', (x_pos, y_pos), hp=self.hp)

        else:
            self.move += 1
            self.hp -= 10
            hero = Skull('hero', (x_pos, y_pos), hp=self.hp)

        self.unit = hero
        return hero

    def avanzar(self, race, enemy_temple, enemy_barrack, enemy_towers,
                enemy_army, allies):
        # poderes
        if self.name == "Manu":
            # creacion mascotas
            self.aux_clock += 1
            if self.aux_clock == self.power_info['time']:  # crear mascota
                pet1 = Pet()
                pet1.attack_range = 40
                pet1.add_pet("Orc", self.unit.cord_x, self.unit.cord_y + 35)
                pet1.hero_pet = True

                pet2 = Pet()
                pet2.attack_range = 40
                pet2.add_pet("Orc", self.unit.cord_x, self.unit.cord_y - 35)
                pet2.hero_pet = True
                self.new_entity.append(pet1)
                self.new_entity.append(pet2)
                self.pets = list(self.new_entity)

            # mantener a su lado
            if len(self.pets) == 2:
                self.pets[0].unit.cord_x = self.unit.cord_x
                self.pets[0].unit.cord_y = self.unit.cord_y + 35

                self.pets[1].unit.cord_x = self.unit.cord_x
                self.pets[1].unit.cord_y = self.unit.cord_y - 35

            elif len(self.pets) == 1:
                self.pets[0].unit.cord_x = self.unit.cord_x
                self.pets[0].unit.cord_y = self.unit.cord_y + 35

        if self.name == "Cristian" and not self.clone:
            if self.objective is None:  # no esta en ritual
                one_enemy = self.closest_in_range(enemy_army)
                if one_enemy is not None:
                    self.objective = one_enemy
                    self.aux_clock = 1
            else:
                if self.in_perimeter(self.objective.unit):  # sigue en rango del ritual
                    self.aux_clock += 1
                    if self.aux_clock == self.power_info['time']:
                        # fin del ritual
                        self.enemy_to_clone = self.objective
                        if self.objective is not None:
                            self.objective.unit.health = 0  # para que se elimine
                            self.objective = None
                else:
                    self.objective = None

                one_enemy = self.closest_in_range(enemy_army)
                if one_enemy is not None:  # enemigo en el rango
                    if self.in_perimeter(one_enemy.unit, False):  # ataque
                        one_enemy.unit.health -= self.harm
                        one_enemy.under_attack = True

                    if self.in_perimeter(enemy_barrack, False):
                        if not enemy_barrack.in_construction:
                            enemy_barrack.health -= self.harm

                    for tower in enemy_towers:
                        if tower is not None:
                            if not tower.in_construction:
                                if self.in_perimeter(tower, False):
                                    tower.health -= self.harm

                    if self.temple_in_range(enemy_temple):
                        enemy_temple.health -= self.harm
                return

        if self.attack_temple:
            self.random_move()  # da movimiento a la jugada

        one_enemy = self.closest_in_range(enemy_army)
        if one_enemy is None:  # no hay enemigos cerca, ataco templo
            self.under_attack = False  # no es posible RR
            for _ in range(self.move):
                self.move_near(enemy_temple)  # objetivo es el templo

        else:  # hay enemigo en el rango
            if race == "Human":
                if self.in_perimeter(one_enemy.unit, False):  # en rango de ataque
                    one_enemy.unit.health -= self.harm
                    one_enemy.under_attack = True

                for _ in range(self.move):
                    self.move_near(enemy_temple)

            elif race == "Orc":
                # si hay alguien en su campo de vision lo persigue
                if self.distance(enemy_temple) < self.distance(one_enemy.unit):
                    for _ in range(self.move):
                        self.move_near(enemy_temple, False)  # persecucion

                elif self.distance(enemy_barrack) < self.distance(one_enemy.unit):
                    for _ in range(self.move):
                        self.move_near(enemy_barrack, False)  # persecucion

                elif self.closest_in_range(enemy_towers, True) is not None:
                    near_tower = self.closest_in_range(enemy_towers, True)
                    if self.distance(near_tower) < self.distance(one_enemy.unit):
                        for _ in range(self.move):
                            self.move_near(near_tower, False)  # persecucion

                else:
                    for _ in range(self.move):
                        self.move_near(one_enemy.unit, False)  # persecucion

                    if self.in_perimeter(one_enemy.unit, False):  # ataque
                        one_enemy.unit.health -= self.harm
                        one_enemy.under_attack = True

            else:  # Skull
                # si hay alguien en el campo de vision lo evita (y dirige al templo)
                for _ in range(self.move):
                    self.move_far(one_enemy.unit)
                    self.move_near(enemy_temple)

                if self.in_perimeter(one_enemy.unit, False):
                    one_enemy.unit.health -= self.harm
                    one_enemy.under_attack = True

        # torreta o cuartel en rango de ataque
        if self.in_perimeter(enemy_barrack, False):
            if not enemy_barrack.in_construction:
                enemy_barrack.health -= self.harm

        for tower in enemy_towers:
            if tower is not None:
                if not tower.in_construction:
                    if self.in_perimeter(tower, False):
                        tower.health -= self.harm

        if self.temple_in_range(enemy_temple):  # mantiene actualizado
            enemy_temple.health -= self.harm  # disminuye hp del templo
            self.attack_temple = True
        else:
            self.attack_temple = False

    def defend(self, temple, enemy_army):
        return  # no defiende

    def move_near(self, objective, temple=True):
        if objective.cord_x == self.unit.cord_x:
            if objective.cord_y > self.unit.cord_y:
                self.unit.cord_y += 1
            elif objective.cord_y == self.unit.cord_y:
                if temple:
                    # llega al templo
                    self.attack_temple = True
                else:
                    self.random_move()  # aporta movimiento
            else:
                self.unit.cord_y -= 1

        elif objective.cord_x > self.unit.cord_x:
            if objective.cord_y > self.unit.cord_y:
                self.unit.cord_x += 1
                self.unit.cord_y += 1
            elif objective.cord_y == self.unit.cord_y:
                self.unit.cord_x += 1
            else:  # <
                self.unit.cord_x += 1
                self.unit.cord_y -= 1

        elif objective.cord_x < self.unit.cord_x:
            if objective.cord_y > self.unit.cord_y:
                self.unit.cord_x -= 1
                self.unit.cord_y += 1
            elif objective.cord_y == self.unit.cord_y:
                self.unit.cord_x -= 1
            else:  # <
                self.unit.cord_x -= 1
                self.unit.cord_y -= 1
        return

    def move_far(self, objective):
        if objective.cord_x == self.unit.cord_x:
            if objective.cord_y > self.unit.cord_y:
                self.unit.cord_y -= 1
            elif objective.cord_y == self.unit.cord_y:
                pass
            else:
                self.unit.cord_y += 1

        elif objective.cord_x > self.unit.cord_x:
            if objective.cord_y > self.unit.cord_y:
                self.unit.cord_x -= 1
                self.unit.cord_y -= 1
            elif objective.cord_y == self.unit.cord_y:
                self.unit.cord_x -= 1
            else:  # <
                self.unit.cord_x -= 1
                self.unit.cord_y += 1

        elif objective.cord_x < self.unit.cord_x:
            if objective.cord_y > self.unit.cord_y:
                self.unit.cord_x += 1
                self.unit.cord_y -= 1
            elif objective.cord_y == self.unit.cord_y:
                self.unit.cord_x += 1
            else:  # <
                self.unit.cord_x += 1
                self.unit.cord_y += 1
        return

    def temple_in_range(self, enemy_temple):
        return (enemy_temple.cord_x - self.unit.cord_x) ** 2 + \
               (enemy_temple.cord_y - self.unit.cord_y) ** 2 <= self.attack_range ** 2

    def closest_in_range(self, enemy_army, buidings=False):  # army.complete_army
        near = list()
        for enemy in enemy_army:
            if buidings:  # mas cercana de las torretas
                if enemy is not None:
                    if self.in_perimeter(enemy):
                        near.append((enemy, self.distance(enemy)))
            else:
                if self.in_perimeter(enemy.unit):
                    near.append((enemy, self.distance(enemy.unit)))

        if len(near) == 0:
            return

        aux = sorted(near, key=lambda x: x[1])
        return aux[0][0]  # enemigo en rango mas cercano

    def random_move(self):
        n = randint(-1, 1)
        direction = choice(['x', 'y'])

        if direction == 'x':
            self.unit.cord_x += n
        else:
            self.unit.cord_y += n
        return

    def in_perimeter(self, enemy, vision=True, archer=False):
        if enemy is None:
            return False

        if vision:  # rango de vision
            return (enemy.cord_x - self.unit.cord_x) ** 2 + \
                   (enemy.cord_y - self.unit.cord_y) ** 2 <= self.vision_range ** 2
        else:  # rango de ataque
            if archer:
                return (enemy.cord_x - self.unit.cord_x) ** 2 + \
                       (enemy.cord_y - self.unit.cord_y) ** 2 <= self.shoot_range ** 2
            else:
                return (enemy.cord_x - self.unit.cord_x) ** 2 + \
                       (enemy.cord_y - self.unit.cord_y) ** 2 <= self.attack_range ** 2

    def distance(self, objective):
        return sqrt((objective.cord_x - self.unit.cord_x) ** 2 +
                    (objective.cord_y - self.unit.cord_y) ** 2)


if __name__ == "__main__":
    print("Module being run directly")
