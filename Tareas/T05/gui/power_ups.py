from random import randint
from .entity import Entity
from .utils import get_asset_path
from PyQt4.QtCore import QThread, pyqtSignal, Qt
from PyQt4.QtGui import QLabel, QPixmap


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

class Explotion:  # QTimer
    pass


class Bullet(Entity):  # QTimer
    def __init__(self, kind):
        self.kind = kind
        super().__init__()
