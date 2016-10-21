import gui
from gui.kinds.human import Human
from gui.kinds.skull import Skull
from gui.kinds.orc import Orc
from edificaciones import Torreta, Cuartel
from math import sqrt
from random import choice, randint


class Warrior:
    def __init__(self):
        self.move = randint(2, 7)  # movimiento por tick
        self.hp = randint(150, 250)  # cuando llega a 0 muere
        self.harm = randint(3, 8)
        self.creation_time = 5
        self.cost = 20
        self.attack_range = 15  # para que no debe estar sobre el otro
        self.unit = None
        self.vision_range = 50  # determina ataque

        self.attack_temple = False
        self.under_attack = False

    @property
    def health(self):
        return self.unit.health

    def add_warrior(self, race, x_pos, y_pos):  # en simulacion se debe instanciar
        if race == "Human":
            warrior = Human('warrior', (x_pos, y_pos), hp=self.hp)

        elif race == "Orc":
            self.move -= 1
            self.harm += 1
            warrior = Orc('warrior', (x_pos, y_pos), hp=self.hp)

        else:
            self.move += 1
            self.hp -= 10
            warrior = Skull('warrior', (x_pos, y_pos), hp=self.hp)

        self.unit = warrior
        return warrior  # en simulacion agregar con gui.add_entity(warrior)

    def avanzar(self, race, enemy_temple, enemy_barrack, enemy_towers,
                enemy_army, allies):
        if self.attack_temple:
            self.random_move()  # da movimiento a la jugada

        one_enemy = self.closest_in_range(enemy_army)
        if one_enemy is None:  # no hay enemigos cerca, ataco templo
            self.under_attack = False  # no es posible RR
            for _ in range(self.move):
                self.move_near(enemy_temple)  # objetivo es el templo

        else:  # hay enemigo en el rango
            if race == "Human":
                if in_perimeter(self, one_enemy.unit, False):  # en rango de ataque
                    one_enemy.unit.health -= self.harm
                    one_enemy.under_attack = True

                for _ in range(self.move):
                    self.move_near(enemy_temple)

            elif race == "Orc":
                # si hay alguien en su campo de vision lo persigue
                if distance(self, enemy_temple) < distance(self, one_enemy.unit):
                    for _ in range(self.move):
                        self.move_near(enemy_temple, False)  # persecucion

                elif distance(self, enemy_barrack) < distance(self, one_enemy.unit):
                    for _ in range(self.move):
                        self.move_near(enemy_barrack, False)  # persecucion

                elif self.closest_in_range(enemy_towers, True) is not None:
                    near_tower = self.closest_in_range(enemy_towers, True)
                    if distance(self, near_tower) < distance(self, one_enemy.unit):
                        for _ in range(self.move):
                            self.move_near(near_tower, False)  # persecucion

                else:
                    for _ in range(self.move):
                        self.move_near(one_enemy.unit, False)  # persecucion

                    if in_perimeter(self, one_enemy.unit, False):  # ataque
                        one_enemy.unit.health -= self.harm
                        one_enemy.under_attack = True

            else:  # Skull
                # si hay alguien en el campo de vision lo evita (y dirige al templo)
                for _ in range(self.move):
                    self.move_far(one_enemy.unit)
                    self.move_near(enemy_temple)

                if in_perimeter(self, one_enemy.unit, False):
                    one_enemy.unit.health -= self.harm
                    one_enemy.under_attack = True

        # torreta o cuartel en rango de ataque
        if in_perimeter(self, enemy_barrack, False):
            if not enemy_barrack.in_construction:
                enemy_barrack.health -= self.harm

        for tower in enemy_towers:
            if tower is not None:
                if not tower.in_construction:
                    if in_perimeter(self, tower, False):
                        tower.health -= self.harm

        if self.temple_in_range(enemy_temple):  # mantiene actualizado
            enemy_temple.health -= self.harm  # disminuye hp del templo
            self.attack_temple = True
        else:
            self.attack_temple = False

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

    def defend(self, building, enemy_army):  # solo en caso de humanos
        if distance(self, building) <= 100:  # perimetro de la base
            x_move = randint(-1, 1)
            y_move = randint(-1, 1)
            for _ in range(self.move):  # agrega movimiento
                self.unit.cord_x += x_move
                self.unit.cord_y += y_move
        else:
            for _ in range(self.move):  # acercarse a proteger el templo
                self.move_near(building, False)

        # atacar si esta en rango de ataque
        one_enemy = self.closest_in_range(enemy_army)
        if one_enemy is not None:  # perseguir y atacar
            for _ in range(self.move):
                self.move_near(one_enemy.unit, False)  # persecucion

            if in_perimeter(self, one_enemy.unit, False):  # ataque
                one_enemy.unit.health -= self.harm

    def temple_in_range(self, enemy_temple):
        return (enemy_temple.cord_x - self.unit.cord_x) ** 2 + \
               (enemy_temple.cord_y - self.unit.cord_y) ** 2 <= self.attack_range ** 2

    def closest_in_range(self, enemy_army, buidings=False):  # army.complete_army
        near = list()
        for enemy in enemy_army:
            if buidings:  # mas cercana de las torretas
                if enemy is not None:
                    if in_perimeter(self, enemy):
                        near.append((enemy, distance(self, enemy)))
            else:
                if in_perimeter(self, enemy.unit):
                    near.append((enemy, distance(self, enemy.unit)))

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


class Archer:
    def __init__(self):
        self.move = randint(2, 7)
        self.hp = randint(100, 200)
        self.harm = randint(2, 6)
        self.shoot_range = randint(50, 80)  # rango de disparo
        self.creation_time = 7
        self.cost = 30
        self.unit = None
        self.vision_range = 50  # determina ataque

        self.attack_temple = False
        self.under_attack = False

    @property
    def health(self):
        return self.unit.health

    def add_archer(self, race, x_pos, y_pos):  # para luego agregar a interfaz
        if race == "Human":
            archer = Human('distance', (x_pos, y_pos), hp=self.hp)

        elif race == "Orc":
            self.move -= 1
            self.harm += 1
            archer = Orc('distance', (x_pos, y_pos), hp=self.hp)

        else:
            self.move += 1
            self.hp -= 10
            archer = Skull('distance', (x_pos, y_pos), hp=self.hp)
        self.unit = archer
        return archer

    def avanzar(self, race, enemy_temple, enemy_barrack, enemy_towers,
                enemy_army, allies):
        if self.attack_temple:
            self.random_move()  # da movimiento a la jugada

        one_enemy = self.closest_in_range(enemy_army)
        if one_enemy is None:  # no hay enemigos cerca, ataco templo
            self.under_attack = False
            for _ in range(self.move):
                self.move_near(enemy_temple)  # objetivo es el templo

        else:  # hay enemigo en el rango
            if race == "Human":
                # ataca cuando esta en rango de ataque
                if in_perimeter(self, one_enemy.unit, False, True):  # en rango de ataque
                    one_enemy.unit.health -= self.harm
                    one_enemy.under_attack = True

                for _ in range(self.move):
                    self.move_near(enemy_temple)

            elif race == "Orc":
                # si hay alguien en su campo de vision lo persigue
                if distance(self, enemy_temple) < distance(self, one_enemy.unit):
                    for _ in range(self.move):
                        self.move_near(enemy_temple, False)  # persecucion

                elif distance(self, enemy_barrack) < distance(self, one_enemy.unit):
                    for _ in range(self.move):
                        self.move_near(enemy_barrack, False)  # persecucion

                elif self.closest_in_range(enemy_towers, True) is not None:
                    near_tower = self.closest_in_range(enemy_towers, True)
                    if distance(self, near_tower) < distance(self, one_enemy.unit):
                        for _ in range(self.move):
                            self.move_near(near_tower, False)  # persecucion
                else:
                    for _ in range(self.move):
                        self.move_near(one_enemy.unit, False)  # persecucion

                    if in_perimeter(self, one_enemy.unit, False, True):  # ataque
                        one_enemy.unit.health -= self.harm
                        one_enemy.under_attack = True

            else:  # Skull
                # si hay alguien en el campo de vision lo evita (y dirige al templo)
                for _ in range(self.move):
                    self.move_far(one_enemy.unit)
                    self.move_near(enemy_temple)

                if in_perimeter(self, one_enemy.unit, False, True):
                    one_enemy.unit.health -= self.harm
                    one_enemy.under_attack = True

        if in_perimeter(self, enemy_barrack, False, True):
            if not enemy_barrack.in_construction:
                enemy_barrack.health -= self.harm

        for tower in enemy_towers:
            if tower is not None:
                if not tower.in_construction:
                    if in_perimeter(self, tower, False, True):
                        tower.health -= self.harm

        if self.temple_in_range(enemy_temple):  # mantiene actualizado
            enemy_temple.health -= self.harm  # disminuye hp del templo
            self.attack_temple = True
        else:
            self.attack_temple = False

    def move_near(self, objective, temple=True):
        if objective.cord_x == self.unit.cord_x:
            if objective.cord_y > self.unit.cord_y:
                self.unit.cord_y += 1
            elif objective.cord_y == self.unit.cord_y:
                if temple:
                    # llega al templo
                    self.attack_temple = True
                else:
                    self.random_move()
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

    def defend(self, building, enemy_army):  # solo en caso de humanos
        if distance(self, building) <= 100:  # perimetro de la base
            x_move = randint(-1, 1)
            y_move = randint(-1, 1)
            for _ in range(self.move):  # agrega movimiento
                self.unit.cord_x += x_move
                self.unit.cord_y += y_move
        else:
            for _ in range(self.move):  # acercarse a proteger el templo
                self.move_near(building, False)

        # atacar si esta en rango de ataque
        one_enemy = self.closest_in_range(enemy_army)
        if one_enemy is not None:  # perseguir y atacar
            for _ in range(self.move):
                self.move_near(one_enemy.unit, False)  # persecucion

            if in_perimeter(self, one_enemy.unit, False, True):  # ataque
                one_enemy.unit.health -= self.harm

    def temple_in_range(self, enemy_temple):
        return (enemy_temple.cord_x - self.unit.cord_x) ** 2 + \
               (enemy_temple.cord_y - self.unit.cord_y) ** 2 <= self.shoot_range ** 2

    def closest_in_range(self, enemy_army, buidings=False):  # army.complete_army
        near = list()
        for enemy in enemy_army:
            if buidings:
                if enemy is not None:  # mas cercana de las torretas
                    if in_perimeter(self, enemy):
                        near.append((enemy, distance(self, enemy)))
            else:
                if in_perimeter(self, enemy.unit):
                    near.append((enemy, distance(self, enemy.unit)))

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


class Pet:
    def __init__(self):
        self.move = randint(3, 6)
        self.hp = randint(100, 200)
        self.harm = randint(2, 7)
        self.attack_range = randint(20, 40)  # rango de ataque (revisar coherencia)
        self.creation_time = 6
        self.cost = 50
        self.unit = None
        self.vision_range = 70
        self.hero_pet = False

        self.attack_temple = False
        self.under_attack = False

    @property
    def health(self):
        return self.unit.health

    def add_pet(self, race, x_pos, y_pos):
        if race == "Human":
            pet = Human('pet', (x_pos, y_pos), hp=self.hp)

        elif race == "Orc":
            self.move -= 1
            self.harm += 1
            pet = Orc('pet', (x_pos, y_pos), hp=self.hp)

        else:
            self.move += 1
            self.hp -= 10
            pet = Skull('pet', (x_pos, y_pos), hp=self.hp)

        self.unit = pet
        return pet

    def avanzar(self, race, enemy_temple, enemy_barrack, enemy_towers,
                enemy_army, allies):
        if self.hero_pet:  # distinta funcionalidad
            for _ in range(self.move):
                self.random_move()  # darle movilidad
            one_enemy = self.closest_in_range(enemy_army)
            if one_enemy is not None:  # enemigo en el rango
                if in_perimeter(self, one_enemy.unit, False):  # ataque
                    one_enemy.unit.health -= self.harm
                    one_enemy.under_attack = True

                if in_perimeter(self, enemy_barrack, False):
                    if not enemy_barrack.in_construction:
                        enemy_barrack.health -= self.harm

                for tower in enemy_towers:
                    if tower is not None:
                        if not tower.in_construction:
                            if in_perimeter(self, tower, False):
                                tower.health -= self.harm

                if self.temple_in_range(enemy_temple):
                    enemy_temple.health -= self.harm

            return  # funcionalidad distinta

        if self.attack_temple:
            self.random_move()  # da movimiento a la jugada

        '''
            RAGE: proteger unidad aliada vulnerable dentro del rango de vision
        '''
        ally = self.closest_in_range(allies, False, True)
        one_enemy = self.closest_in_range(enemy_army)

        if ally is not None:  # debe ir a protegerlo
            for _ in range(self.move):
                self.move_near(ally.unit, False)  # va al rescate

                one_enemy = self.closest_in_range(enemy_army)
                if one_enemy is not None:
                    if in_perimeter(self, one_enemy.unit, False):  # enemigo en perimetro de ataque
                        one_enemy.unit.health -= self.harm
                        one_enemy.under_attack = True

        elif one_enemy is None:  # no hay enemigos cerca, ataco templo
            self.under_attack = False
            for _ in range(self.move):
                self.move_near(enemy_temple)  # objetivo es el templo

        else:  # hay enemigo en el rango
            if race == "Human":
                if in_perimeter(self, one_enemy.unit, False):  # en rango de ataque
                    one_enemy.unit.health -= self.harm
                    one_enemy.under_attack = True

                for _ in range(self.move):
                    self.move_near(enemy_temple)

            elif race == "Orc":
                # si hay alguien en su campo de vision lo persigue
                if distance(self, enemy_temple) < distance(self, one_enemy.unit):
                    for _ in range(self.move):
                        self.move_near(enemy_temple, False)  # persecucion

                elif distance(self, enemy_barrack) < distance(self, one_enemy.unit):
                    for _ in range(self.move):
                        self.move_near(enemy_barrack, False)  # persecucion

                elif self.closest_in_range(enemy_towers, True) is not None:
                    near_tower = self.closest_in_range(enemy_towers, True)
                    if distance(self, near_tower) < distance(self, one_enemy.unit):
                        for _ in range(self.move):
                            self.move_near(near_tower, False)  # persecucion

                else:
                    for _ in range(self.move):
                        self.move_near(one_enemy.unit, False)  # persecucion

                    if in_perimeter(self, one_enemy.unit, False):  # ataque
                        one_enemy.unit.health -= self.harm
                        one_enemy.under_attack = True

            else:  # Skull
                # si hay alguien en el campo de vision lo evita (y dirige al templo)
                for _ in range(self.move):
                    self.move_far(one_enemy.unit)
                    self.move_near(enemy_temple)

                if in_perimeter(self, one_enemy.unit, False):
                    one_enemy.unit.health -= self.harm
                    one_enemy.under_attack = True

        if in_perimeter(self, enemy_barrack, False):
            if not enemy_barrack.in_construction:
                enemy_barrack.health -= self.harm

        for tower in enemy_towers:
            if tower is not None:
                if not tower.in_construction:
                    if in_perimeter(self, tower, False):
                        tower.health -= self.harm

        if self.temple_in_range(enemy_temple):  # mantiene actualizado
            enemy_temple.health -= self.harm  # disminuye hp del templo
            self.attack_temple = True
        else:
            self.attack_temple = False

    def move_near(self, objective, temple=True):
        if objective.cord_x == self.unit.cord_x:
            if objective.cord_y > self.unit.cord_y:
                self.unit.cord_y += 1
            elif objective.cord_y == self.unit.cord_y:
                if temple:
                    # llega al templo
                    self.attack_temple = True
                else:
                    self.random_move()
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

    def defend(self, building, enemy_army):  # solo en caso de humanos
        if distance(self, building) <= 100:  # perimetro de la base
            x_move = randint(-1, 1)
            y_move = randint(-1, 1)
            for _ in range(self.move):  # agrega movimiento
                self.unit.cord_x += x_move
                self.unit.cord_y += y_move
        else:
            for _ in range(self.move):  # acercarse a proteger el templo
                self.move_near(building, False)

        # atacar si esta en rango de ataque
        one_enemy = self.closest_in_range(enemy_army)
        if one_enemy is not None:  # perseguir y atacar
            for _ in range(self.move):
                self.move_near(one_enemy.unit, False)  # persecucion

            if in_perimeter(self, one_enemy.unit, False):  # ataque
                one_enemy.unit.health -= self.harm

    def temple_in_range(self, enemy_temple):
        return (enemy_temple.cord_x - self.unit.cord_x) ** 2 + \
               (enemy_temple.cord_y - self.unit.cord_y) ** 2 <= self.attack_range ** 2

    def closest_in_range(self, enemy_army, buidings=False, protect=False):
        near = list()
        for enemy in enemy_army:
            if buidings:
                if enemy is not None:  # mas cercana de las torretas
                    if in_perimeter(self, enemy):
                        near.append((enemy, distance(self, enemy)))

            elif protect:  # busca de aliados a proteger
                if enemy != self:
                    if in_perimeter(self, enemy.unit) and enemy.under_attack:
                        # enemy es ally en este caso
                        near.append((enemy, distance(self, enemy.unit)))
            else:
                if in_perimeter(self, enemy.unit):
                    near.append((enemy, distance(self, enemy.unit)))

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


''' funciones
'''


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
