from random import randint
from .entity import Entity
from .utils import get_asset_path
from PyQt4.QtCore import QTimer, pyqtSignal, Qt, QObject
from PyQt4.QtGui import QLabel, QPixmap
from time import sleep
from math import tan, radians
from random import randint


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

class Explotion(Entity):  # tipo bomba (18) y entre balas (6)
    def __init__(self, kind, pos=(0, 0), size=(50, 50), exp=18):
        self._counter = exp
        self.kind = kind
        super().__init__(["smoke", self.kind + str(exp // 6) + ".png"], size=size, hp=0, pos=pos)

    @property
    def counter(self):
        return self._counter

    @counter.setter
    def counter(self, other):
        self._counter = other
        if other > 0 and other % 6 == 0:
            self.updatePixmap()

    def updatePixmap(self):
        self._base_image = ["smoke", self.kind + str(self.counter // 6) + ".png"]
        self.cord_x += randint(-20, 20)
        self.cord_y += randint(-20, 20)
        super().updatePixmap()


class PowerUp(Entity):
    def __init__(self, kind, pos=(0, 0), size=(20, 35)):
        self.kind = kind
        super().__init__(["bullets", self.kind + ".png"], size=size,
                         hp=0, pos=pos)


class Bullet(Entity):
    def __init__(self, kind, harm, pos=(10,10), owner=None):
        self.kind = kind
        self.owner = owner
        self.base_harm = harm
        self.distance = 900  # ponderador de daño
        self.rebounds = 2  # rebotes
        self.to_remove = False
        super().__init__(["bullets", "bullet" + self.kind + ".png"],
                         size=(12, 21), hp=0, pos=pos)

    def shoot_move(self, forbidden_cords, enemies):
        if self.cord_x < 88 or self.cord_x > 750 \
                or self.cord_y < 83 or self.cord_y > 597:  # bordes
            # rebote
            self.to_remove = True
            return

        for enemy in enemies:  # tambien incluye principal
            if enemy != self.owner:
                if self.cord_x > enemy.cord_x and self.cord_x < enemy.cord_x + enemy.width():
                    if self.cord_y > enemy.cord_y and self.cord_y < enemy.cord_y + enemy.height():
                        if self.kind == "Explosive":  # detonacion no harm directo
                            pass
                        else:
                            if self.kind == "Ralentizante":
                                if enemy.speed < 1:
                                    pass
                                elif enemy.speed == 1:
                                    enemy.speed = 0.5
                                else:
                                    enemy.speed = int(enemy.speed // 2)

                            # choca a enemigo
                            alpha = int(self.distance // 200)
                            if alpha < 1:
                                alpha = 1

                            new_harm = self.base_harm * alpha
                            enemy.health -= new_harm

                        self.to_remove = True
                        return

        # if self.rebounds == 1:
        #     if self.cord_x > tank.cord_x and self.cord_x < tank.cord_x + tank.width():
        #         if self.cord_y > tank.cord_y and self.cord_y < tank.cord_y + tank.height():
        #             # autoimpacto
        #             alpha = int(self.distance // 200)
        #             if alpha < 1:
        #                 alpha = 1
        #
        #             new_harm = harm * alpha
        #             tank.health -= new_harm
        #             self.to_remove = True
        #             return

        if self.kind != "Penetrante":  # si pueden atravesar walls
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

        elif int(self.angle) in range(190, 271):
            self.cord_x -= 5
            self.cord_y += 5 / tan(radians(self.angle))

        else:
            self.cord_x += 5
            self.cord_y -= 5 / tan(radians(self.angle))

        self.distance -= 5
        return


class Portal(Entity):
    def __init__(self, pos=(10,10)):
        self._flying = True
        self.to_remove = False
        super().__init__(["bullets", "portal.png"], size=(40, 40), hp=0, pos=pos)

    @property
    def flying(self):
        return self._flying

    @flying.setter
    def flying(self, other):
        self._flying = other
        self.updatePixmap()

    def updatePixmap(self):
        if self.flying:
            self._base_image = ["bullets", "portal.png"]
        else:
            self._base_image = ["bullets", "portalWall.png"]
        super().updatePixmap()

    def shoot_move(self, forbidden_cords, enemies):
        if self.cord_x < 88 or self.cord_x > 750 \
                or self.cord_y < 83 or self.cord_y > 597:  # bordes
            self.flying = False
            return

        for enemy in enemies:  # tambien incluye principal
            if self.cord_x > enemy.cord_x and self.cord_x < enemy.cord_x + enemy.width():
                if self.cord_y > enemy.cord_y and self.cord_y < enemy.cord_y + enemy.height():
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
                self.flying = False
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

        elif int(self.angle) in range(190, 271):
            self.cord_x -= 5
            self.cord_y += 5 / tan(radians(self.angle))

        else:
            self.cord_x += 5
            self.cord_y -= 5 / tan(radians(self.angle))

        return

