from PyQt4.QtGui import QLabel, QPixmap, QTransform, QWidget, QProgressBar
from PyQt4.QtCore import Qt
from .utils import get_asset_path
from math import sqrt
'''
    bastante codigo sacado de la gui T04
'''


class Entity(QWidget):

    def __init__(self, base_image, size, hp=200, pos=(0, 0), parent=None):
        super().__init__(parent)
        self._base_label = QLabel(self)
        if len(base_image) > 1:
            if "tank" in base_image[1] or "barrel" in base_image[1] or "bullet" in base_image[1]:
                aux = max(size[0], size[1])
                self._base_label.setFixedSize(aux * sqrt(2), aux * sqrt(2))
        self._base_image = base_image
        self._size = size
        self._decor_label = None
        self._decor_pixmap = None
        self._hp_max = hp

        self.__pixmap = None
        """type: PyQt4.QtGui.QPixmap"""

        self.__cord_x = pos[0]
        self.__cord_y = pos[1]
        self.__angle = 0

        self.setAlignment(Qt.AlignCenter)
        self.updatePixmap()

        if self._hp_max != 0:
            self.set_hp_bar(size)

        # if _debugging:
        #     self.setStyleSheet("border: 1px solid black")

    @property
    def health(self):
        return self.__hp_bar.value()

    @health.setter
    def health(self, hp):
        if hp > self._hp_max:
            hp = self._hp_max
        elif hp < 0:
            hp = 0
        self.__hp_bar.setValue(hp)

    @property
    def angle(self):
        return self.__angle

    @angle.setter
    def angle(self, angle):
        self.__angle = angle
        self.updatePixmap()

    @property
    def cord_x(self):
        return self.__cord_x

    @cord_x.setter
    def cord_x(self, cord):
        self.__cord_x = cord
        self.move(self.cord_x, self.cord_y)

    @property
    def cord_y(self):
        return self.__cord_y

    @cord_y.setter
    def cord_y(self, cord):
        self.__cord_y = cord
        self.move(self.cord_x, self.cord_y)

    def set_hp_bar(self, size):
        self.__hp_bar = QProgressBar(self)
        self.__hp_bar.setMaximum(self._hp_max)
        self.__hp_bar.setValue(self._hp_max)
        self.__hp_bar.setTextVisible(False)
        self.__hp_bar.setMaximumSize(size[0] * sqrt(2), 5)

    def hide_hp_bar(self, bool=False):
        if bool:
            self.__hp_bar.hide()
        else:
            self.__hp_bar.show()

    def add_decoration(self, path):
        if path is None:
            self._decor_label.deleteLater()
            self._decor_label = None
        else:
            self._decor_label = QLabel(self)
            self._decor_pixmap = QPixmap(path)
            # self._decor_pixmap = self._decor_pixmap.scaled(self._size[0], self._size[1])
            self._decor_pixmap = self._decor_pixmap.transformed(QTransform().rotate(self.angle))
            self._decor_label.setPixmap(self._decor_pixmap)
            self._decor_label.setAlignment(Qt.AlignCenter)
            self._decor_label.show()

    def updatePixmap(self):
        path = get_asset_path(self._base_image)
        self.__pixmap = QPixmap(path)
        self.__pixmap = self.__pixmap.scaled(self._size[0], self._size[1])
        self.__pixmap = self.__pixmap.transformed(QTransform().rotate(self.angle))
        self._base_label.setPixmap(self.__pixmap)
        self._base_label.show()

    def setFixedSize(self, x, y):
        super().setFixedSize(x, y)
        self._base_label.setFixedSize(x, y)

    def setAlignment(self, alignment):
        self._base_label.setAlignment(alignment)
