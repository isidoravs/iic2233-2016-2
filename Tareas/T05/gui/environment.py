from .entity import Entity
from .utils import get_asset_path


class Wall(Entity):
    def __init__(self, kind, pos=(30, 30), size=(100, 60)):
        self.destructible = False
        self.__destroyed = False
        self.kind = kind
        self.size = size
        super().__init__(["obstacles", self.kind + ".png"], size=size,
                         hp=0, pos=pos)
