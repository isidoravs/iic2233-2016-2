from PyQt4 import QtGui, QtCore
from juego import Juego
import sys
import time


class Programadito(QtGui.QWidget):

    def __init__(self):
        super().__init__()
        self.inicializa_GUI()


    def inicializa_GUI(self):
        self.setFixedSize(1000, 800)
        self.setWindowTitle("Programadito")

        self.boton_inicio = QtGui.QPushButton('&Start', self)
        self.boton_inicio.setGeometry(125, 30, 750, 50)
        self.boton_inicio.clicked.connect(self.start)

        self.etiqueta1 = QtGui.QLabel('Mensaje:', self)
        self.etiqueta1.move(125, 100)

        self.boton_reinicio = QtGui.QPushButton('&Restart', self)
        self.boton_reinicio.setGeometry(125, 140, 750, 50)
        self.boton_reinicio.clicked.connect(self.restart)

        self.etiqueta2 = QtGui.QLabel('Carta:', self)
        self.etiqueta2.move(480, 220)

        self.imagen_j1 = QtGui.QLabel(self)
        self.imagen_j1.setGeometry(50, 300, 200, 100)
        self.imagen_j1.setPixmap(QtGui.QPixmap(
            "cartas/jugador_1.png").scaled(200, 100))

        self.imagen_j2 = QtGui.QLabel(self)
        self.imagen_j2.setGeometry(750, 300, 200, 100)
        self.imagen_j2.setPixmap(
            QtGui.QPixmap("cartas/jugador_2.png").scaled(200, 100))

        self.imagen_inicio = QtGui.QLabel(self)
        self.imagen_inicio.setGeometry(350, 250, 300, 450)
        self.imagen_inicio.setPixmap(
            QtGui.QPixmap("cartas/black_joker.png").scaled(300, 450))

        self.cartas_j1 = QtGui.QLabel('54', self)
        self.cartas_j1.move(50, 700)

        self.cartas_j2 = QtGui.QLabel('54', self)
        self.cartas_j2.move(670, 700)

        self.winner_label = QtGui.QLabel("", self)
        self.winner_label.move(400, 750)
        self.winner_label.show()

        self.etiqueta1.hide()
        self.etiqueta2.hide()
        self.imagen_j1.hide()
        self.imagen_j2.hide()
        self.cartas_j1.hide()
        self.cartas_j2.hide()
        self.boton_reinicio.hide()
        self.imagen_inicio.hide()

    def start(self):
        self.etiqueta1.show()
        self.etiqueta2.show()
        self.imagen_j1.show()
        self.imagen_j2.show()
        self.cartas_j1.show()
        self.cartas_j2.show()
        self.boton_reinicio.show()
        self.imagen_inicio.show()

        # inicializar juego
        self.game = Juego()
        return

    def finish(self):
        pass

    def restart(self):
        pass

    def keyPressEvent(self, event):
        if event.text() == "S":  # jugador 1 agrega
            self.winner_label.hide()
            path_carta = self.game.saca_jugador1()
            if path_carta is True:
                self.winner_label.setText("GANADOR FINAL JUGADOR 1")
                self.winner_label.show()
                time.sleep(2)
                sys.exit()

            self.cartas_j1.setText(str(len(self.game.jugador1)))
            self.etiqueta2.setText("Carta: {}".format(self.game.carta_actual))
            self.etiqueta2.resize(100, 25)
            self.imagen_inicio.setPixmap(
                QtGui.QPixmap("cartas/" + path_carta).scaled(300, 450))

        elif event.text() == "K":  # jugador 2 agrega
            self.winner_label.hide()
            path_carta = self.game.saca_jugador2()

            if path_carta is True:
                self.winner_label.setText("GANADOR FINAL JUGADOR 2")
                self.winner_label.show()
                time.sleep(2)
                sys.exit()

            self.cartas_j2.setText(str(len(self.game.jugador2)))
            self.etiqueta2.setText("Carta: {}".format(self.game.carta_actual))
            self.etiqueta2.resize(100, 25)
            self.imagen_inicio.setPixmap(
                QtGui.QPixmap("cartas/" + path_carta).scaled(300, 450))

        elif event.text() == "W":  # jugador 1 apreta
            resultado = self.game.compara_jugador1()
            if resultado:
                self.winner_label.setText("GANADOR JUGADOR 1")
                self.winner_label.show()

                self.imagen_inicio.setPixmap(
                    QtGui.QPixmap("cartas/black_joker.png").scaled(300, 450))
            else:
                self.winner_label.setText("Jugador 1 se ha equivocado")
                self.winner_label.show()

            self.cartas_j1.setText(str(len(self.game.jugador1)))
            self.cartas_j2.setText(str(len(self.game.jugador2)))

        elif event.text() == "I":  # jugador 2 apreta
            resultado = self.game.compara_jugador2()
            if resultado:
                self.winner_label.setText("GANADOR JUGADOR 2")
                self.winner_label.show()
                self.imagen_inicio.setPixmap(
                    QtGui.QPixmap("cartas/black_joker.png").scaled(300, 450))
            else:
                self.winner_label.setText("Jugador 2 se ha equivocado")
                self.winner_label.show()

            self.cartas_j1.setText(str(len(self.game.jugador1)))
            self.cartas_j2.setText(str(len(self.game.jugador2)))




if __name__ == '__main__':
    app = QtGui.QApplication([])
    ventana = Programadito()
    ventana.show()
    app.exec_()