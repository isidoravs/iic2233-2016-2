from PyQt4.QtGui import QWidget, QLabel, QPixmap, QApplication, QFont, QCursor, QMainWindow
from PyQt4.QtGui import QRadioButton, QLineEdit, QPushButton, QInputDialog
from PyQt4.QtGui import QTableWidget, QTableWidgetItem, QAbstractItemView
from PyQt4.QtCore import QTimer, Qt, SIGNAL
from .chat import Chat
from .juego import Game
import os
import time


def get_absolute_path(relative_path):
    return os.path.join(os.path.dirname(__file__), relative_path)


class GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.client = None
        self.username = None
        self.friends = list()
        self.games = list()

        self.game_online = None  # solo permite uno simultaneo

        self.all_chats = list()  # guarda instancias de chat (abiertos)

        self.programillo = Programillo()
        self.login = LogIn()

        self.__connections()
        self.login.show()
        self.login.raise_()

    def __connections(self):
        self.login.button_signup_done.clicked.connect(self.signup_done)
        self.login.button_login_done.clicked.connect(self.login_done)
        self.login.button_aux.clicked.connect(self.start_interface)

        self.programillo.button_search_friend.clicked.connect(self.search_friend)
        self.programillo.button_chat.clicked.connect(self.chat)
        self.programillo.button_create.clicked.connect(self.create_game)
        self.programillo.button_join.clicked.connect(self.join_game)

    def client_signals(self):
        self.connect(self.client, SIGNAL("start_chat"), self.start_chat)
        self.connect(self.client, SIGNAL("close_chat"), self.delete_chat)
        self.connect(self.client, SIGNAL("send_chat"), self.send_chat)
        self.connect(self.client, SIGNAL("add_game"), self.add_game)
        self.connect(self.client, SIGNAL("start_game"), self.open_game)
        self.connect(self.client, SIGNAL("add_friend"), self.add_friend)
        self.connect(self.client, SIGNAL("no_game"), self.reset_game)
        self.connect(self.client, SIGNAL("user_offline"), self.user_offline)
        self.connect(self.client, SIGNAL("send_game_chat"), self.add_game_chat)
        self.connect(self.client, SIGNAL("start_round"), self.start_round)
        self.connect(self.client, SIGNAL("game_guess"), self.guess_player)


    def start_interface(self):
        if self.username is None:
            print("No hay usuario")

        else:
            # cliente conectado
            self.client_signals()

            self.login.close()
            self.programillo.set_start_info(self.username, self.friends, self.games)
            self.programillo.client = self.client
            self.programillo.show()
            self.programillo.raise_()

    def login_done(self):
        if self.login.password_label1.text() == "":
            self.login.set_message("Enter a password")

        elif self.login.username_label.text() == "":
            self.login.set_message("Enter a username")

        else:
            try:
                valid = self.login.password_label1.text().encode('ascii')
                username = self.login.username_label.text()
                password = self.login.password_label1.text()
                self.connect_login(username, password)

            except UnicodeEncodeError:
                self.login.set_message("Invalid character in password")

    def signup_done(self):
        if self.login.password_label1.text() == "":
            self.login.set_message("Enter a password")

        elif self.login.username_label.text() == "":
            self.login.set_message("Enter a username")

        elif ";" in self.login.username_label.text():  # separacion base de datos
            self.login.set_message("Invalid character in username")

        elif ";" in self.login.password_label1.text():
            self.login.set_message("Invalid character in password")

        elif self.login.password_label1.text() != self.login.password_label2.text():
            self.login.set_message("Passwords doesn't match")

        else:
            try:
                valid = self.login.password_label1.text().encode('ascii')
                username = self.login.username_label.text()
                password = self.login.password_label1.text()
                self.connect_signup(username, password)

            except UnicodeEncodeError:
                self.login.set_message("Invalid character in password")

    def connect_login(self, username, password):
        return

    def connect_signup(self, username, password):
        return

    def search_friend(self):
        # chequea en base de datos
        friend = self.programillo.label_find.text().strip()

        items = []
        for i in range(self.programillo.display_friends.rowCount()):
            items.append(self.programillo.display_friends.item(i, 0).text())

        if friend in items:
            self.programillo.set_message("{} ya es tu amigo".format(friend))

        elif friend == self.username:
            self.programillo.set_message("No te agregues como amigo".format(friend))

        else:
            self.client.send("indata;friend;{};{}".format(friend, self.username))

    def add_friend(self):
        self.programillo.add_friend()
        self.programillo.label_find.setText("")

    def chat(self):
        selected = self.programillo.display_friends.selectedItems()
        usernames = [friend.text() for friend in selected]  # ya todos existen
        if len(usernames) == 0:
            return

        aux = sorted(usernames + [self.username])
        participants = ";".join(aux)  # incluye creador
        self.client.send("chat;start;{}".format(participants))
        return

    def start_chat(self, messages, participants):  # participants es lista
        new = True
        for chat in self.all_chats:
            if chat.participants == participants:
                new = False

        if new:
            # crear chat y abrir
            new_chat = Chat(self.client, self.username, participants, messages)
            new_chat.setWindowTitle("Chat - {}".format(", ".join(participants)))
            new_chat.button_start.clicked.connect(lambda: self.create_game_from_chat(participants, new_chat))

            self.all_chats.append(new_chat)
            new_chat.show()

    def send_chat(self, participants, message):
        for chat in self.all_chats:
            if chat.participants == participants:
                chat.add_chat(message)

    def delete_chat(self, participants):
        participants_list = participants.split(";")
        to_delete = None
        for chat in self.all_chats:
            if chat.participants == participants_list:
                to_delete = chat
                break

        if to_delete is not None:
            self.all_chats.remove(to_delete)
        else:
            print("wierd...")

    def create_game(self):
        self.programillo.set_games_message("")
        selected = self.programillo.display_friends.selectedItems()
        usernames = [friend.text() for friend in selected]

        if len(usernames) == 0:
            self.programillo.set_games_message("Selecciona amigos de tu lista")
        else:
            participants = ";".join(sorted(usernames + [self.username]))
            repeated = False
            for game in self.programillo.display_games.all_games:
                if participants == game:
                    self.programillo.set_games_message("Ya existe una sala con los participantes")
                    repeated = True

            if not repeated:
                # self.programillo.display_games.add_game(participants)
                self.client.send("game;add;{};{}".format(self.username,
                                                         participants))

    def create_game_from_chat(self, participants_list, chat):
        participants = ";".join(participants_list)

        repeated = False
        for game in self.programillo.display_games.all_games:
            if participants == game:
                # ya existe
                self.client.send("game;start;{}".format(participants))
                repeated = True
                break

        if not repeated:
            self.programillo.display_games.add_game(participants)
            self.client.send("game;add;{};{}".format(self.username,
                                                     participants))
            self.client.send("game;start;{}".format(participants))

    def add_game(self, participants):
        repeated = False
        for game in self.programillo.display_games.all_games:
            if participants == game:
                repeated = True

        if not repeated:
            self.programillo.display_games.add_game(participants)

    def join_game(self):
        if self.game_online is not None:
            self.programillo.set_games_message(
                "Ya tienes un juego online! Ciérralo para comenzar otro.")

        else:
            self.programillo.set_games_message("")
            selected = self.programillo.display_games.selectedItems()
            games = [sala.text() for sala in selected]

            if len(selected) == 0:
                self.programillo.set_games_message(
                    "Selecciona una sala para jugar")

            elif len(selected) > 1:
                self.programillo.set_games_message("No puedes unirte a más de una sala")

            elif "¡Sala comun!" in games[0]:
                pass

            else:
                aux = "".join(games[0].split(":")[1:]).strip()
                participants = aux.split(", ")
                self.client.send("game;start;{}".format(";".join(participants)))

    def open_game(self, success, participants=None):  # ya paso las condiciones y debe abrir ventana
        if not success:
            self.programillo.set_games_message("Tus amigos no estan online para jugar")
        else:
            self.game_online = Game(self.client, self.username, participants, participants, participants)
            self.game_online.show()
            self.game_online.button_invite.clicked.connect(self.invite_friend)
            # self.add_game_chat(" ~ Inicio de la partida ~ ")
            # self.add_game_chat(" > Participantes:")
            # self.add_game_chat("{}".format(", ".join(participants)))

            for chat in self.all_chats:
                if chat.participants == participants:
                    chat.add_chat(" ~ PARTIDA COMENZADA ~")

    def invite_friend(self):
        pass

    def reset_game(self):
        self.game_online = None

    def user_offline(self, user):
        if self.game_online is not None:
            if user in self.game_online.online:
                self.game_online.online.remove(user)
                self.game_online.offline.append(user)
            self.game_online.game_chat.addItem(" > {} ha cerrado el juego".format(user))

            if user in self.game_online.not_painted:
                self.game_online.not_painted.append(user)

            if len(self.game_online.online) == 1:
                self.game_online.game_chat.addItem(" > Solo estás tu online!")
                self.game_online.game_chat.addItem("Cierra la venta o espera que un amigo se una para jugar.")
                self.game_online.button_start.hide()

    def add_game_chat(self, message):
        if self.game_online is not None:
            self.game_online.game_chat.addItem(message)
            self.game_online.messages.append(message)

    def start_round(self, word, painter):
        print(word)
        if self.game_online is not None:
            self.game_online.start_round_signal(word)
            self.game_online.painter = painter
            if painter == self.username:
                self.game_online.button_send.hide()
                self.game_online.paint.painter = True

    def guess_player(self, player):
        if self.game_online is not None:
            if player not in self.game_online.guessed:
                self.game_online.guessed.append(player)
            if self.username == player:
                self.have_guessed = True


class Programillo(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1024, 680)
        self.setWindowTitle('Programillo')

        self.client = None

        self.background = QLabel(self)
        self.background.setGeometry(0, 0, 1024, 680)
        self.background.setPixmap(QPixmap(get_absolute_path(
            "./images/background_gui.png")).scaled(1024, 680))

        self.button_chat = QPushButton("&Chat", self)
        self.button_chat.move(895, 470)
        self.button_chat.resize(self.button_chat.sizeHint())

        self.label_find = QLineEdit("", self)
        self.label_find.setGeometry(280, 80, 350, 30)

        self.button_search_friend = QPushButton("&Agregar", self)
        self.button_search_friend.move(520, 120)
        self.button_search_friend.resize(self.button_search_friend.sizeHint())

        self.message_friends = QLabel("", self)
        self.message_friends.move(285, 120)

        self.button_create = QPushButton("&Crear sala", self)
        self.button_create.move(80, 610)
        self.button_create.resize(self.button_create.sizeHint())

        self.message_games = QLabel("", self)
        self.message_games.move(20, 650)

        self.button_join = QPushButton("&Unirse!", self)
        self.button_join.move(210, 610)
        self.button_join.resize(self.button_join.sizeHint())

    def set_start_info(self, username, friends, games):
        self.player = username

        self.display_friends = FriendsTable(self, username, friends)
        self.display_friends.setGeometry(780, 160, 225, 300)

        self.display_games = GamesTable(self, games)  # lista con participantes (;)
        self.display_games.setGeometry(20, 150, 300, 450)

        self.label_username = QLabel(username, self)
        self.score_font = QFont("", 10)
        self.score_font.setBold(True)
        self.label_username.setFont(self.score_font)
        self.label_username.move(780, 30)

        self.display_friends.show()
        self.label_username.show()

    def add_friend(self):  # agregar a base de datos
        friend = self.label_find.text().strip()
        self.display_friends.add_friend(friend)
        self.label_find.setText("")
        return

    def set_message(self, text):
        self.message_friends.setText(text)
        self.message_friends.setFixedWidth(self.message_friends.sizeHint().width())

    def set_games_message(self, text):
        self.message_games.setText(text)
        self.message_games.setFixedWidth(self.message_games.sizeHint().width())

    def closeEvent(self, QCloseEvent):
        self.client.send("exit")
        QCloseEvent.accept()


class LogIn(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(410, 325)
        self.setWindowTitle('Programillo')

        self.username = None
        self.friends = None

        self.logo = QLabel(self)
        self.logo.move(80,10)
        self.logo.setPixmap(QPixmap(get_absolute_path("images/login.png"))
                            .scaled(240, 140))

        self.button_signup = QPushButton("&Registrarse", self)
        self.button_signup.move(60, 200)
        self.button_signup.resize(self.button_signup.sizeHint())
        self.button_signup.clicked.connect(self.signup)

        self.button_login = QPushButton("&Ingresar", self)
        self.button_login.move(230, 200)
        self.button_login.resize(self.button_login.sizeHint())
        self.button_login.clicked.connect(self.login)

        self.button_back = QPushButton("&Volver", self)
        self.button_back.move(290, 20)
        self.button_back.resize(self.button_back.sizeHint())
        self.button_back.clicked.connect(self.get_back)
        self.button_back.hide()

        self.button_login_done = QPushButton("&Listo!", self)
        self.button_login_done.move(290, 280)
        self.button_login_done.resize(self.button_login_done.sizeHint())
        self.button_login_done.hide()

        self.button_signup_done = QPushButton("&Listo!", self)
        self.button_signup_done.move(290, 280)
        self.button_signup_done.resize(self.button_signup_done.sizeHint())
        self.button_signup_done.hide()

        self.button_aux = QPushButton("&Iniciar", self)
        self.button_aux.move(290, 280)
        self.button_aux.resize(self.button_aux.sizeHint())
        self.button_aux.hide()

        self.message = QLabel("", self)
        self.message.move(10, 290)

        self.username_label = QLineEdit("", self)
        self.username_label.setGeometry(160, 160, 240, 30)
        self.username_label.hide()

        self.password_label1 = QLineEdit("", self)
        self.password_label1.setGeometry(160, 200, 240, 30)
        self.password_label1.hide()

        self.password_label2 = QLineEdit("", self)
        self.password_label2.setGeometry(160, 240, 240, 30)
        self.password_label2.hide()

        self.label1 = QLabel("Username:", self)
        self.label2 = QLabel("Password:", self)
        self.label3 = QLabel("Confirm password:", self)
        self.label1.move(10, 165)
        self.label2.move(10, 205)
        self.label3.move(10, 245)

        self.label1.hide()
        self.label2.hide()
        self.label3.hide()

    def signup(self):
        self.username_label.show()
        self.password_label1.show()
        self.password_label2.show()

        self.label1.show()
        self.label2.show()
        self.label3.show()

        self.button_login.hide()
        self.button_signup.hide()
        self.button_back.show()
        self.button_signup_done.show()
        return

    def login(self):
        self.username_label.show()
        self.password_label1.show()

        self.label1.show()
        self.label2.show()


        self.button_login.hide()
        self.button_signup.hide()
        self.button_back.show()
        self.button_login_done.show()
        return

    def get_back(self):
        self.label1.hide()
        self.label2.hide()
        self.label3.hide()
        self.username_label.hide()
        self.password_label1.hide()
        self.password_label2.hide()

        self.button_back.hide()
        self.button_login.show()
        self.button_signup.show()
        self.button_login_done.hide()
        self.button_signup_done.hide()
        self.button_aux.hide()

        self.set_message("")
        return

    def set_message(self, text):
        self.message.setText(text)
        self.message.setFixedWidth(self.message.sizeHint().width())


class FriendsTable(QTableWidget):
    def __init__(self, parent, username, data):  # lista con nombres de amigos
        QTableWidget.__init__(self, parent)

        self.data = data  # lista con nombres de amigos
        self.setRowCount(len(self.data))
        self.setColumnCount(1)

        self.horizontalHeader().setStretchLastSection(True)  # usa espacio
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)  # no editar

        self.setHorizontalHeaderLabels(["Amigos"])
        self.setmydata()

    def setmydata(self):
        for i in range(len(self.data)):
            newitem = QTableWidgetItem(self.data[i])
            self.setItem(0, i, newitem)

    def add_friend(self, friend):
        rowPosition = self.rowCount()
        self.insertRow(rowPosition)
        self.setItem(rowPosition, 0, QTableWidgetItem(friend))
        return


class GamesTable(QTableWidget):
    def __init__(self, parent, data):
        QTableWidget.__init__(self, parent)

        self.data = data  # lista con string de participante (;)
        # self.setRowCount(len(self.data))
        self.setColumnCount(1)

        self.all_games = list()  # con listas de participantes

        self.horizontalHeader().setStretchLastSection(True)  # usa espacio
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)  # no editar

        self.setHorizontalHeaderLabels(["Selecciona una sala:"])
        self.setmydata()

    def setmydata(self):
        sala_comun = "¡Sala comun! Únete para jugar"
        newitem = QTableWidgetItem(sala_comun)
        self.insertRow(0)
        self.setItem(0, 0, newitem)

        for i in range(len(self.data)):
            participants = self.data[i]
            self.all_games.append(participants)

            rowPosition = self.rowCount()
            self.insertRow(rowPosition)

            aux = participants.split(";")
            string = "Sala {}: ".format(str(i + 1)) + ", ".join(aux)
            newitem = QTableWidgetItem(string)
            self.setItem(0, rowPosition, newitem)

    def add_game(self, participants):
        rowPosition = self.rowCount()
        self.insertRow(rowPosition)

        self.all_games.append(participants)
        aux = participants.split(";")
        string = "Sala {}: ".format(str(rowPosition)) + ", ".join(aux)
        self.setItem(0, rowPosition, QTableWidgetItem(string))
        return

if __name__ == "__main__":
    app = QApplication([])
    gui = GUI()
    gui.username = "isidora-prueba"
    app.exec_()