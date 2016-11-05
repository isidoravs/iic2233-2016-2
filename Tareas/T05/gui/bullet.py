from random import randint
from PyQt4.QtCore import QTimer, pyqtSignal, Qt, QThread
from PyQt4.QtGui import QLabel, QPixmap
from time import sleep


class MoveMyImageEvent:
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y


class Bullet(QThread):  # QTimer
    '''
        bastante codigo sacado de la ayudantia PyQt4
    '''
    trigger = pyqtSignal(MoveMyImageEvent)

    def __init__(self, parent, kind, x, y, wait=0):

        super().__init__()
        self.image = QLabel(parent)
        self.kind = kind
        self.image.setPixmap(QPixmap("assets/bullets/bullet{}.png".format(self.kind)).scaled(12, 25, Qt.KeepAspectRatio))
        self.image.show()

        self.trigger.connect(parent.update_image)
        self.__position = (0, 0)
        self.lag = wait

        # envia signal
        self.position = (x, y)

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        self.__position = value

        # trigger emite signal a mainwindow
        self.trigger.emit(MoveMyImageEvent(
            self.image, self.position[0], self.position[1]))

    def run(self):
        self.active = True
        sleep(self.lag)  # cuanto espera en partir
        while self.active:
            x, y = self.position
            self.position = (x + 5, y)
            if self.position[0] >= 1000:
                self.active = False
            sleep(0.01)