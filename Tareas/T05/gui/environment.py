from .entity import Entity
from .utils import get_asset_path


class Wall(Entity):
    def __init__(self, kind, pos=(30, 30), size=(100, 60)):
        self.destructible = False
        self.__destroyed = False
        self.kind = kind
        super().__init__(["obstacles", self.kind + ".png"], size=size,
                         hp=0, pos=pos)

class Coin(Entity):
    def __init__(self, pos=(100, 100), size=(10, 10)):
        super().__init__(["obstacles", "coin.png"], size=size, hp=0, pos=pos)


    # @property
    # def destroyed(self):
    #     if not self.destructible:  # no se puede destruir
    #         return False
    #     return self.__destroyed
    #
    # @destroyed.setter
    # def destroyed(self, other):
    #     self.__destroyed = other
    #     self.updatePixmap()
