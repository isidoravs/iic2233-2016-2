from PyQt4.QtGui import QWidget, QLabel, QPixmap, QApplication, QFont, QCursor
from PyQt4.QtGui import QRadioButton, QLineEdit, QPushButton, QMouseEvent
from PyQt4.QtGui import QTableWidget, QListWidget, QIcon, QListWidgetItem
from PyQt4.QtCore import QTimer, Qt, QEvent
import os
import re


def get_absolute_path(relative_path):
    return os.path.join(os.path.dirname(__file__), relative_path)

class Chat(QWidget):
    def __init__(self, client, player, participants, messages):
        super().__init__()
        self.setFixedSize(500, 550)
        self.setWindowTitle('Programillo - Chat')

        self.messages = messages

        self.background = QLabel(self)
        self.background.setGeometry(0, 0, 500, 550)
        self.background.setPixmap(QPixmap(get_absolute_path(
            "./images/background_chat.png")).scaled(500, 550))

        self.player = player  # nombre jugador actual
        self.participants = participants  # lista con participantes sorted (friends + player)
        self.client = client

        self.label_message = QLineEdit("", self)
        self.label_message.setGeometry(20, 492, 340, 33)

        self.button_send = QPushButton("&Enviar", self)
        self.button_send.move(370, 490)
        self.button_send.resize(100, 35)
        self.button_send.clicked.connect(self.send_chat)

        self.button_start = QPushButton("&Ok!", self)
        self.button_start.move(420, 15)
        self.button_start.resize(70, 35)

        self.chat = QListWidget(self)
        self.chat.setGeometry(20, 70, 450, 390)

        self.start_messages()

    def start_messages(self):
        for msge in self.messages:
            self.chat.addItem(msge)

    def send_chat(self):
        message = "{}: {}".format(self.player, self.label_message.text())
        message.replace(";", "")  # evita problemas
        self.label_message.setText("")

        participants = ";".join(self.participants)

        self.client.send("chat;send;{};{};{}".format(self.player,
                                                     message,
                                                     participants))
        return

    def add_chat(self, message):
        if ":)" or ":(" or ":o" in message:

            icon_happy = QIcon(get_absolute_path("./images/emoji-).jpg"))
            item_happy = QListWidgetItem()
            item_happy.setIcon(icon_happy)

            icon_sad = QIcon(get_absolute_path("./images/emoji-(.png"))
            item_sad = QListWidgetItem()
            item_sad.setIcon(icon_sad)

            icon_wow = QIcon(get_absolute_path("./images/emoji-o.png"))
            item_wow = QListWidgetItem()
            item_wow.setIcon(icon_wow)

            aux = message + " "
            all_emojis =  [m.start() for m in re.finditer('(:\)|:\(|:o)', aux)]

            chat = ""
            for i in range(len(aux) - 1):
                if aux[i] != ":":
                    if i - 1 not in all_emojis:
                        chat += aux[i]
                else:
                    if aux[i+1] == ")":
                        self.chat.addItem(chat)
                        self.chat.addItem(item_happy)
                        chat = ""

                    elif aux[i+1] == "(":
                        self.chat.addItem(chat)
                        self.chat.addItem(item_sad)
                        chat = ""

                    elif aux[i+1] == "o":
                        self.chat.addItem(chat)
                        self.chat.addItem(item_wow)
                        chat = ""

                    else:
                        if i - 1 not in all_emojis:
                            chat += aux[i]

            if chat != "":
                self.chat.addItem(chat)

        else:
            self.chat.addItem(message)

        self.messages.append(message)

    def closeEvent(self, QCloseEvent):
        to_send = "chat;close;friends;{};messages;{}".format(";".join(self.participants),
                                                             ";".join(self.messages))
        self.client.send(to_send)
        QCloseEvent.accept()



if __name__ == "__main__":
    print("Module being run directly")