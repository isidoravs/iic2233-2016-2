import gui
from gui.building import Building, Temple
from random import randint, uniform


class Cuartel(Building):  # unico
    def __init__(self, x_pos, y_pos):  # property in_construction
        self.hp = 500  # usar property health de entity
        self.cost = 100
        self.construction_time = 80  # no son segundos (relacion de trabajo)
        self.work_on = 0
        super().__init__('barracks', pos=(x_pos, y_pos), hp=self.hp)  # self.k es el tipo 'barracks', 'tower', 'mine'


class Torreta(Building):  # property in_construction
    def __init__(self, x_pos, y_pos):
        self.hp = 400  # usar property health de entity
        self.cost = 150
        self.construction_time = 60
        self.work_on = 0

        # ataque
        self.attack_speed = uniform(0.5, 1.5)  # ataques por segundo
        self.harm = round(self.attack_speed * randint(1, 5))  # toma en cuenta la velocidad de ataque
        self.shoot_range = randint(100, 150)
        super().__init__('tower', pos=(x_pos, y_pos), hp=self.hp)

    def check_perimeter(self, enemy_army):  # lista con enemigos
        if self.in_construction:
            return

        for enemy in enemy_army:
            # verifico si esta en el perimetro
            if self.in_perimeter(enemy):
                enemy.unit.health -= self.harm

    def in_perimeter(self, enemy):
        return (enemy.unit.cord_x - self.cord_x) ** 2 + \
               (enemy.unit.cord_y - self.cord_y) ** 2 <= self.shoot_range**2


class Mina(Building):  # property in_construction
    def __init__(self, x_pos, y_pos):  # no se puede destruir
        super().__init__('mine', pos=(x_pos, y_pos))


class Templo(Temple):  # unico, no se puede reconstuir
    def __init__(self, god, x_pos, y_pos):
        self.hp = 1250  # mayor hp, usar property health de entity
        super().__init__(god, pos=(x_pos, y_pos), hp=self.hp)  # self.god es el dios del templo


if __name__ == "__main__":
    print("Module being run directly")
