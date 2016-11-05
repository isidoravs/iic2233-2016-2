from random import randint
from .entity import Entity
from .utils import get_asset_path
from PyQt4.QtCore import QTimer, pyqtSignal, Qt, QObject
from PyQt4.QtGui import QLabel, QPixmap
from time import sleep
from math import tan, radians


class Bomb(Entity):
    def __init__(self, attack_range, pos=(0, 0)):
        self.time_to_explode = randint(3,6)
        self.harm = int(self.set_harm())
        self.attack_range = attack_range
        self.start_time = 0  # contador para explosion
        super().__init__(["obstacles", "bomb.png"], size=(40, 40),
                         hp=self.time_to_explode, pos=pos)

    def set_harm(self):
        with open("constantes.txt", "r") as file:
            for line in file:
                if "bombHarm" in line:
                    return line.strip().split(",")[1]

class Explotion:
    pass


class PowerUp(Entity):
    def __init__(self, kind, pos=(0, 0), size=(20, 35)):
        self.kind = kind
        super().__init__(["bullets", self.kind + ".png"], size=size,
                         hp=0, pos=pos)


class Bullet(Entity):
    def __init__(self, kind, pos=(10,10)):
        self.kind = kind
        self.distance = 900  # ponderador de daño
        self.rebounds = 2  # rebotes
        self.to_remove = False
        super().__init__(["bullets", "bullet" + self.kind + ".png"],
                         size=(12, 21), hp=0, pos=pos)

    def shoot_move(self, forbidden_cords, enemies, harm, tank):
        if self.cord_x < 88 or self.cord_x > 750 \
                or self.cord_y < 83 or self.cord_y > 597:  # bordes
            # rebote
            self.to_remove = True
            return

        for enemy in enemies:  # tambien incluye principal
            if self.cord_x > enemy.cord_x and self.cord_x < enemy.cord_x + enemy.width():
                if self.cord_y > enemy.cord_y and self.cord_y < enemy.cord_y + enemy.height():
                    # choca a enemigo
                    alpha = int(self.distance // 200)
                    if alpha < 1:
                        alpha = 1

                    new_harm = harm * alpha
                    enemy.health -= new_harm
                    self.to_remove = True
                    return

        if self.rebounds == 1:  # ya reboto permite autoimpacto
            if self.cord_x > tank.cord_x and self.cord_x < tank.cord_x + tank.width():
                if self.cord_y > tank.cord_y and self.cord_y < tank.cord_y + tank.height():
                    # autoimpacto
                    alpha = int(self.distance // 200)
                    if alpha < 1:
                        alpha = 1

                    new_harm = harm * alpha
                    tank.health -= new_harm
                    self.to_remove = True
                    return

        all_borders = list()
        all_borders.extend([(self.cord_x, y) for y in
                            range(int(self.cord_y),
                                  int(self.cord_y + self.height()))])
        all_borders.extend([(self.cord_x + self.width(), y) for y in
                            range(int(self.cord_y),
                                  int(self.cord_y + self.height()))])
        all_borders.extend([(x, self.cord_y) for x in
                            range(int(self.cord_x),
                                  int(self.cord_x + self.width()))])
        all_borders.extend([(x, self.cord_y + self.height()) for x in
                            range(int(self.cord_x),
                                  int(self.cord_x + self.width()))])

        for cord in all_borders:
            if cord in forbidden_cords:
                self.to_remove = True
                return

        if int(self.angle) in range(0, 10):
            self.cord_y -= 5

        elif int(self.angle) in range(170, 190):
            self.cord_y += 5

        elif int(self.angle) in range(80, 100):
            self.cord_x += 5

        elif self.angle < 0:  # II cuadrante
            self.cord_x -= 5
            self.cord_y += 5 / tan(radians(self.angle))

        elif int(self.angle) in range(190, 270):
            self.cord_x -= 5
            self.cord_y += 5 / tan(radians(self.angle))

        else:
            self.cord_x += 5
            self.cord_y -= 5 / tan(radians(self.angle))

        self.distance -= 5

        return
