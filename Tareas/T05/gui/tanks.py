from .entity import Entity
from .utils import get_asset_path
from math import cos, sin, atan, degrees, radians



class Tank(Entity):
    def __init__(self, color, move, stats, hp=75, pos=(88, 83), size=(45, 45),
                 center=(0, 0), radio=30, direction=None):  # "x>", "x<" o "y>", "y<"
        self.color = color
        self.harm = stats[0]
        self.size = size

        # tanque_circulo
        self.center = center
        self.radio = radio
        self.direction = direction

        self.bombs = self.start_bombs()  # solo para ppal
        self.bullets = self.start_bullets()  # solo para ppal, PILA

        if color == "Black":
            self.barrel = self.barrel = Barrel(self.color,
                                               pos=(pos[0] - 13, pos[1] - 13),
                                               size=(105, 105))
        else:
            self.barrel = self.barrel = Barrel(self.color, pos=(pos[0] - 13,
                                                                pos[1] - 13))

        self.resistance = stats[1]
        self.speed = stats[2]  # movimientos por tecla
        self.shoot = stats[3]
        self.bomb_range = stats[4]
        self.__move = move  # move es estado de movimiento
        super().__init__(["tanks", "tank" + self.color + str(move) + ".png"],
                         size=size, hp=hp, pos=pos)

    @property
    def movement(self):
        return self.__move

    @movement.setter
    def movement(self, other):
        if other == 4:
            self.__move = 1
        else:
            self.__move = other
        self.updatePixmap()

    def updatePixmap(self):  # define estados de movimiento
        if self.movement == 1:
            self._base_image = ["tanks", "tank" + self.color + "1.png"]
        elif self.movement == 2:
            self._base_image = ["tanks", "tank" + self.color + "2.png"]
        elif self.movement == 3:
            self._base_image = ["tanks", "tank" + self.color + "3.png"]
        super().updatePixmap()

    def start_bombs(self):
        if self.color == "Blue":
            with open("constantes.txt", "r") as file:
                for line in file:
                    if "startBombs" in line:
                        return int(line.strip().split(",")[1])
        else:
            return 0

    def start_bullets(self):
        if self.color == "Blue":
            with open("constantes.txt", "r") as file:
                for line in file:
                    if "startBullets" in line:
                        bullets_qty = int(line.strip().split(",")[1])
                        return ["n"] * bullets_qty
        else:
            return float("Inf")

    def make_movement(self, objective):  # avanzar
        if self.color == "Red":  # guiador
            opuesto = objective.cord_x - self.cord_x
            adyacente = self.cord_y - objective.cord_y
            if adyacente == 0:
                if opuesto > 0:
                    new_angle = 90
                else:
                    new_angle = 270

            elif opuesto == 0:
                if adyacente > 0:
                    new_angle = 0
                else:
                    new_angle = 180

            elif adyacente < 0:
                new_angle = degrees(atan(opuesto / adyacente)) + 180
            else:
                new_angle = degrees(atan(opuesto / adyacente))
            self.angle = new_angle
            self.barrel.angle = new_angle

            for _ in range(self.speed):  # revisar no chocar RR
                self.move_near(objective)

        elif self.color == "Green":  # circulo
            self.angle -= self.speed
            self.cord_x = self.center[0] + self.radio * cos(radians(self.angle))
            self.cord_y = self.center[1] + self.radio * sin(radians(self.angle))

            self.barrel.angle -= self.speed
            self.barrel.cord_x = self.cord_x - 13
            self.barrel.cord_y = self.cord_y - 13

        elif self.color == "Black":  # grande
            opuesto = objective.cord_x - self.cord_x
            adyacente = self.cord_y - objective.cord_y
            if adyacente == 0:
                if opuesto > 0:
                    new_angle = 90
                else:
                    new_angle = 270

            elif opuesto == 0:
                if adyacente > 0:
                    new_angle = 0
                else:
                    new_angle = 180

            elif adyacente < 0:
                new_angle = degrees(atan(opuesto / adyacente)) + 180
            else:
                new_angle = degrees(atan(opuesto / adyacente))
            self.angle = new_angle
            self.barrel.angle = new_angle

            for _ in range(self.speed):  # revisar no chocar RR
                self.move_near(objective)

    def move_near(self, objective):
        if objective.cord_x == self.cord_x:
            if objective.cord_y > self.cord_y:
                self.cord_y += 1
                self.barrel.cord_y += 1
            elif objective.cord_y == self.cord_y:
                # llega a objetivo
                pass
            else:
                self.cord_y -= 1
                self.barrel.cord_y -= 1

        elif objective.cord_x > self.cord_x:
            if objective.cord_y > self.cord_y:
                self.cord_x += 1
                self.cord_y += 1
                self.barrel.cord_x += 1
                self.barrel.cord_y += 1
            elif objective.cord_y == self.cord_y:
                self.cord_x += 1
                self.barrel.cord_x += 1
            else:  # <
                self.cord_x += 1
                self.cord_y -= 1
                self.barrel.cord_x += 1
                self.barrel.cord_y -= 1

        elif objective.cord_x < self.cord_x:
            if objective.cord_y > self.cord_y:
                self.cord_x -= 1
                self.cord_y += 1
                self.barrel.cord_x -= 1
                self.barrel.cord_y += 1
            elif objective.cord_y == self.cord_y:
                self.cord_x -= 1
                self.barrel.cord_x -= 1
            else:  # <
                self.cord_x -= 1
                self.cord_y -= 1
                self.barrel.cord_x -= 1
                self.barrel.cord_y -= 1
        return


class Barrel(Entity):
    def __init__(self, color, size=(90, 90), pos=(0, 0), hp=0):
        self.color = color
        self.size = size
        super().__init__(["tanks", "b" + self.color + ".png"], size=size,
                         hp=hp, pos=pos)
