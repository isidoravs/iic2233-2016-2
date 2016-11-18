from PyQt4.QtGui import QWidget, QLabel, QPixmap, QApplication, QFont, QIcon
from PyQt4.QtGui import QRadioButton, QLineEdit, QPushButton, QAbstractItemView
from PyQt4.QtGui import QTableWidget, QListWidget, QListWidgetItem, QTableWidgetItem
from PyQt4.QtCore import QTimer, Qt, QEvent, QSize
import os


def get_absolute_path(relative_path):
    return os.path.join(os.path.dirname(__file__), relative_path)


class Game(QWidget):
    def __init__(self, player, participants):
        super().__init__()
        self.setFixedSize(1225, 680)
        self.setWindowTitle('Programillo - ¡A dibujar!')

        self.background = QLabel(self)
        self.background.setGeometry(0, 0, 1225, 680)
        self.background.setPixmap(QPixmap(get_absolute_path(
            "./images/background_game.png")).scaled(1225, 680))

        # participantes
        self.player = player
        self.participants = participants

        # chat
        self.game_chat = QListWidget(self)
        self.game_chat.setGeometry(880, 200, 330, 400)

        self.button_send = QPushButton("&>", self)
        self.button_send.move(1170, 619)
        self.button_send.resize(40, 35)
        self.button_send.clicked.connect(self.send_chat)

        self.label_message = QLineEdit("", self)
        self.label_message.setGeometry(880, 620, 280, 33)

        # participantes
        self.display_participants = ParticipantsTable(self, participants)
        self.display_participants.setGeometry(20, 80, 240, 180)

        self.button_invite = QPushButton("&Invitar", self)
        self.button_invite.move(150, 265)
        self.button_invite.resize(self.button_invite.sizeHint())
        self.button_invite.clicked.connect(self.invite_friend)

        # dibujos ganadores
        self.display_drawings = DrawingsList(self)
        self.display_drawings.setGeometry(100, 320, 160, 350)

        # mostrar cuando este temrinada la imagen
        self.button_save = QPushButton("&Guardar imagen", self)
        self.button_save.move(720, 620)
        self.button_save.resize(self.button_save.sizeHint())
        self.button_save.clicked.connect(self.save_image)

    def send_chat(self):
        # actualizar todos los amigos RR
        self.update_chat(self.player, self.label_message.text())
        self.label_message.setText("")
        return

    def invite_friend(self):
        # buscar y agregar (cuadro de dialogo)
        # self.display_participants.add_participant(participant)
        return

    def update_chat(self, friend, message):
        self.game_chat.addItem("{}: {}".format(friend, message))
        return

    def winner_drawing(self, path):
        self.display_drawings.add_drawing(path)
        return

    def save_image(self):  # hacer el proceso de pasar a png
        pass

class ParticipantsTable(QTableWidget):
    def __init__(self, parent, data):
        QTableWidget.__init__(self, parent)

        self.data = data  # lista con participantes
        self.setRowCount(len(self.data))
        self.setColumnCount(1)

        self.horizontalHeader().setStretchLastSection(True)  # usa espacio
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)  # no editar

        self.setHorizontalHeaderLabels([""])
        self.setmydata()

    def setmydata(self):
        for i in range(len(self.data)):
            friend = self.data[i]
            self.setItem(0, i, QTableWidgetItem(friend))

    def add_participant(self, participant):
        rowPosition = self.rowCount()
        self.insertRow(rowPosition)
        self.setItem(rowPosition, 0, QTableWidgetItem(participant))
        # servidor muestre a los demas el nuevo participante RR
        return

class DrawingsList(QListWidget):

    def add_drawing(self, path):
        size = QSize(100, 100)
        item = QListWidgetItem()
        item.setSizeHint(size)
        icon = QIcon()
        icon.addPixmap(QPixmap(path), QIcon.Normal, QIcon.Off)
        item.setIcon(icon)
        self.addItem(item)
        self.setIconSize(size)


if __name__ == "__main__":
    app = QApplication([])
    game = Game("isidora", ["tere", "antonia"])
    game.show()
    game.winner_drawing("./images/1.jpg")
    game.winner_drawing("./images/2.jpg")
    game.winner_drawing("./images/3.jpg")
    game.winner_drawing("./images/4.gif")
    app.exec_()

