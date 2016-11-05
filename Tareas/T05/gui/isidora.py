from PyQt4 import QtGui
from PyQt4 import QtCore
from bullet import Bullet


class Ventana(QtGui.QWidget):

    def __init__(self):
        super().__init__()
        self.__setUp()

    def __setUp(self):
        self.setGeometry(100, 100, 450, 250)
        self.setWindowTitle("Probando")

        self.start_boton = QtGui.QPushButton('&Start', self)
        self.start_boton.clicked.connect(self.start)
        self.start_boton.move(275, 210)


    def start(self):
        self.empezar()
        self.start_boton.hide()

    def empezar(self):
        bullet = Bullet(parent=self, kind="Normal", x=100, y=100)
        bullet.start()


    def update_image(self, myImageEvent):
        label = myImageEvent.image
        label.move(myImageEvent.x, myImageEvent.y)

if __name__ == '__main__':
    app = QtGui.QApplication([])
    ventana = Ventana()
    ventana.show()
    app.exec_()
