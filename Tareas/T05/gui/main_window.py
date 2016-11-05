from PyQt4.QtGui import QWidget, QLabel, QPixmap, QApplication, QFont, QCursor
from PyQt4.QtGui import QRadioButton, QLineEdit, QPushButton, QMouseEvent
from PyQt4.QtCore import QTimer, Qt, QEvent, SIGNAL
from .utils import get_asset_path
from .power_ups import Bomb, Bullet
from .store import Store
from math import atan, degrees
import time
'''
    bastante codigo sacado de la gui T04
'''


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setFixedSize(1024, 680)
        self.setWindowTitle('Hacker Tanks!')

        self.__timer = QTimer(self)
        self.background = QLabel(self)
        self.background.setGeometry(20, 20, 800, 640)
        self.background.setPixmap(QPixmap(get_asset_path(["background.png"])))
        self.__entities = []
        self._bombs = []  # ppal bombs
        self.all_bullets = list()

        self.store = QLabel(self)
        self.store.setGeometry(670, 120, 45, 45)
        self.store.setPixmap(QPixmap(get_asset_path(["environment", "cross.png"])).scaled(45, 45))

        self.mode = None
        self.stage = None
        self.final_score = 0
        self._score = 200

        self.is_paused = False
        self.start_pause = 0
        self.end_pause = 0
        self.paused_time = 0

        self.end_game = False

        self.tank = None
        self.forbidden_cords = list()  # poco eficiente

        self.start_menu()

        self.back_to_store = 0  # permitido para volver a entrar
        self.cooldown = False

        # teclas simultaneas
        self.last_key = ""
        self.last_key_time = 0

        self.cursor = QCursor()


    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, other):
        self._score = other

    def start_menu(self):
        self.label_start = QLabel(" -- Hacker Tanks! -- \n\n\n Mode:", self)
        self.label_start.move(840, 50)

        self.option1 = QRadioButton("Stages", self)
        self.option1.move(840, 150)
        self.label_stage = QLineEdit("", self)
        self.label_stage.move(840, 180)

        self.option2 = QRadioButton("Survival", self)
        self.option2.move(840, 220)

        self.button_start = QPushButton('&Start', self)
        self.button_start.resize(self.button_start.sizeHint())
        self.button_start.move(860, 530)
        self.button_start.clicked.connect(self.start)

        self.error_label = QLabel("", self)
        self.error_label.move(840, 250)

    def init_gui(self, mode, level=0):
        # ocultar anteriores
        self.label_start.hide()
        self.button_start.hide()
        self.option1.hide()
        self.option2.hide()
        self.label_stage.deleteLater()

        # labels
        self.label_score_fix = QLabel("Score: ", self)
        self.label_score_fix.move(830, 100)
        self.label_score_fix.show()

        self.label_score = QLabel(str(self.score), self)  # actualiza
        self.label_score.move(850, 120)
        self.label_score.show()

        if mode == "Stages":
            self.label_time_fix = QLabel("Time left: ", self)
        else:
            self.label_time_fix = QLabel("Clock: ", self)
        self.label_time_fix.move(830, 170)
        self.label_time_fix.show()

        self.label_time = QLabel("60 seg.", self)
        self.label_time.move(850, 190)
        self.label_time.show()

        self.label_level = QLabel("MODE:".format(mode), self)
        self.label_level.move(850, 30)
        self.set_level(mode, level)
        self.label_level.show()

        self.message_label = QLabel("", self)
        self.message_label.move(830, 270)
        self.message_label.show()

        self.bombs_label = QLabel("Bombs left: 0", self)
        self.bombs_label.move(830, 300)
        self.bombs_label.show()

        # mostrar 3 balas siguientes
        self.bullets_label = QLabel("Next bullets:", self)
        self.bullets_label.move(830, 320)
        self.bullets_label.show()

        self.bullet1 = QLabel(self)
        self.bullet1.move(860, 350)

        self.bullet2 = QLabel(self)
        self.bullet2.move(900, 350)

        self.bullet3 = QLabel(self)
        self.bullet3.move(940, 350)

        self.button_pause = QPushButton('&Pause', self)
        self.button_pause.resize(self.button_pause.sizeHint())
        self.button_pause.move(875, 480)
        self.button_pause.clicked.connect(self.pause)
        self.button_pause.show()

        self.button_quit = QPushButton('&Quit', self)
        self.button_quit.resize(self.button_quit.sizeHint())
        self.button_quit.move(875, 530)
        self.button_quit.clicked.connect(self.quit)
        self.button_quit.show()

    def startMain(self, main, delay=25):
        self.__timer.timeout.connect(main)
        self.__timer.start(delay)

    def add_entity(self, entity):  # agregar entidades
        entity.setParent(self)
        entity.show()
        self.__entities.append(entity)

    def set_score(self, score):  # RR ver si se corta
        self.label_score.setText(score)
        self.label_score.setFixedWidth(self.label_score.sizeHint().width())

    def set_next_bullets(self, tank):
        if tank is not None:
            if len(self.tank.bullets) >= 3:  # de otra manera no muestra ninguno
                bullet_1 = tank.bullets[-1]
                bullet_2 = tank.bullets[-2]
                bullet_3 = tank.bullets[-3]
                self._bullet1 = QPixmap(self.bullet_path(bullet_1))
                self._bullet2 = QPixmap(self.bullet_path(bullet_2))
                self._bullet3 = QPixmap(self.bullet_path(bullet_3))

                self.bullet1.setPixmap(self._bullet1)
                self.bullet2.setPixmap(self._bullet2)
                self.bullet3.setPixmap(self._bullet3)

                self.bullet1.show()
                self.bullet2.show()
                self.bullet3.show()
            else:
                self.bullet1.hide()
                self.bullet2.hide()
                self.bullet3.hide()

    def bullet_path(self, bullet_id):
        if bullet_id == "n":
            return get_asset_path(["bullets", "bulletNormal.png"])
        if bullet_id == "e":
            return get_asset_path(["bullets", "bulletExplosive.png"])
        if bullet_id == "p":
            return get_asset_path(["bullets", "bulletPenetrante.png"])
        if bullet_id == "r":
            return get_asset_path(["bullets", "bulletRalentizante.png"])

    def set_bombs_left(self, tank):
        if tank is not None:
            self.bombs_label.setText("Bombs left: {}".format(tank.bombs))
            self.bombs_label.setFixedWidth(self.bombs_label.sizeHint().width())

    def set_time(self, time_left):
        self.label_time.setText("{} seg.".format(time_left))
        self.label_time.setFixedWidth(self.label_time.sizeHint().width())

    def set_level(self, mode, level=0):
        if mode == "Stages":
            self.label_level.setText("MODE: Stages ({})".format(str(level)))
            self.label_level.setFixedWidth(self.label_level.sizeHint().width())
        else:
            self.label_level.setText("MODE: Survival")
            self.label_level.setFixedWidth(self.label_level.sizeHint().width())

    def set_message(self, message):
        self.message_label.setText(message)
        self.message_label.setFixedWidth(self.message_label.sizeHint().width())

    def show_error(self, error):
        self.error_label.setText("ERROR {}".format(error))
        self.error_label.setFixedWidth(self.error_label.sizeHint().width())
        self.error_label.move(823, 260)

    def keyPressEvent(self, event):
        if self.tank is None:  # evita errores antes de empezar
            return

        if self.is_paused:
            return

        if self.tank.cord_x in range(650, 690) and self.tank.cord_y in range(100, 140):
            if self.cooldown:
                if int(time.clock()) > self.back_to_store:  # paso el tiempo
                    self.cooldown = False

            if not self.cooldown:
                # sector tienda
                self.pause()  # pausa juego

                # nueva ventana
                self.start_store()
                self.cooldown = True
                return

        self.tank.movement += 1

        old_cord = (self.tank.cord_x, self.tank.cord_y)
        old_barrel_cord = (self.tank.barrel.cord_x, self.tank.barrel.cord_y)

        key = event.text()

        if key == "A" or key == "a":

            if (time.clock() - self.last_key_time) < 0.1 and self.last_key in [
                "S", "s", "W", "w"]:
                if self.last_key == "S" or self.last_key == "s":
                    self.tank.angle = 225
                    for _ in range(self.tank.speed):
                        self.tank.cord_x -= 1
                        self.tank.cord_y += 1

                        self.tank.barrel.cord_x -= 1
                        self.tank.barrel.cord_y += 1

                elif self.last_key == "W" or self.last_key == "w":
                    self.tank.angle = 315
                    for _ in range(self.tank.speed):
                        self.tank.cord_x -= 1
                        self.tank.cord_y -= 1

                        self.tank.barrel.cord_x -= 1
                        self.tank.barrel.cord_y -= 1

            else:  # izq
                self.tank.angle = 270
                self.tank.cord_x -= self.tank.speed
                self.tank.barrel.cord_x -= self.tank.speed

        elif key == "D" or key == "d":

            if (time.clock() - self.last_key_time) < 0.1 and self.last_key in [
                "S", "s", "W", "w"]:
                if self.last_key == "S" or self.last_key == "s":
                    self.tank.angle = 135
                    for _ in range(self.tank.speed):
                        self.tank.cord_x += 1
                        self.tank.cord_y += 1

                        self.tank.barrel.cord_x += 1
                        self.tank.barrel.cord_y += 1

                elif self.last_key == "W" or self.last_key == "w":
                    self.tank.angle = 45
                    for _ in range(self.tank.speed):
                        self.tank.cord_x += 1
                        self.tank.cord_y -= 1

                        self.tank.barrel.cord_x += 1
                        self.tank.barrel.cord_y -= 1

            else:  # der
                self.tank.angle = 90
                self.tank.cord_x += self.tank.speed
                self.tank.barrel.cord_x += self.tank.speed

        elif key == "S" or key == "s":

            if (time.clock() - self.last_key_time) < 0.1 and self.last_key in [
                "A", "a", "D", "d"]:
                if self.last_key == "A" or self.last_key == "a":
                    self.tank.angle = 225
                    for _ in range(self.tank.speed):
                        self.tank.cord_x -= 1
                        self.tank.cord_y += 1

                        self.tank.barrel.cord_x -= 1
                        self.tank.barrel.cord_y += 1

                elif self.last_key == "D" or self.last_key == "d":
                    self.tank.angle = 135
                    for _ in range(self.tank.speed):
                        self.tank.cord_x += 1
                        self.tank.cord_y += 1

                        self.tank.barrel.cord_x += 1
                        self.tank.barrel.cord_y += 1

            else:  # down
                self.tank.angle = 180
                self.tank.cord_y += self.tank.speed
                self.tank.barrel.cord_y += self.tank.speed

        elif key == "W" or key == "w":

            if (time.clock() - self.last_key_time) < 0.1 and self.last_key in [
                "A", "a", "D", "d"]:
                if self.last_key == "A" or self.last_key == "a":
                    self.tank.angle = 315
                    for _ in range(self.tank.speed):
                        self.tank.cord_x -= 1
                        self.tank.cord_y -= 1

                        self.tank.barrel.cord_x -= 1
                        self.tank.barrel.cord_y -= 1

                elif self.last_key == "D" or self.last_key == "d":
                    self.tank.angle = 45
                    for _ in range(self.tank.speed):
                        self.tank.cord_x += 1
                        self.tank.cord_y -= 1

                        self.tank.barrel.cord_x += 1
                        self.tank.barrel.cord_y -= 1

            else:  # up
                self.tank.angle = 0
                self.tank.cord_y -= self.tank.speed
                self.tank.barrel.cord_y -= self.tank.speed

        elif key == "G" or key == "g":
            self.quit()
            return

        elif key == "P" or key == "p":
            self.pause()
            return

        elif event.key() == 16777220:  # Enter
            # portales
            pass

        if not self.valid_movement(self.tank):
            self.tank.cord_x = old_cord[0]
            self.tank.cord_y = old_cord[1]

            self.tank.barrel.cord_x = old_barrel_cord[0]
            self.tank.barrel.cord_y = old_barrel_cord[1]

        self.last_key = key
        self.last_key_time = time.clock()
        return

    def start_store(self):
        actual_stats = {"harm": self.tank.harm, "hp": self.tank.max_hp,
                        "resistance": self.tank.resistance,
                        "speed": self.tank.speed,
                        "shoot": self.tank.shoot,
                        "bomb_range": self.tank.bomb_range}

        self.store = Store(self.score, actual_stats)
        self.store.show()

    def show_explotion(self, position):
        self.explotion = QLabel(self)
        self.explotion.setPixmap(QPixmap(get_asset_path(
            ["smoke", "explode3.png"])).scaled(64, 64, Qt.KeepAspectRatio))
        self.explotion.move(position[0], position[1])
        self.explotion.show()

    def mousePressEvent(self, event):
        if self.is_paused:
            return

        if self.mode is None:
            return

        if event.button() == Qt.LeftButton:
            # disparo
            if len(self.tank.bullets) == 0:
                return

            else:
                next_bullet = self.tank.bullets.pop()
                self.set_next_bullets(self.tank)
                if next_bullet == "n":
                    kind = "Normal"
                elif next_bullet == "e":
                    kind = "Explosive"
                elif next_bullet == "p":
                    kind = "Penetrante"
                else:  # r
                    kind = "Ralentizante"

                aux_angle = int(self.tank.barrel.angle)

                if aux_angle in range(-20, 20):
                    x_pos = self.tank.cord_x + 45//2
                    y_pos = self.tank.cord_y

                elif aux_angle in range(20, 65):
                    x_pos = self.tank.cord_x + 45
                    y_pos = self.tank.cord_y

                elif aux_angle in range(65, 115):
                    x_pos = self.tank.cord_x + 45
                    y_pos = self.tank.cord_y + 45//2

                elif aux_angle in range(115, 155):
                    x_pos = self.tank.cord_x + 45
                    y_pos = self.tank.cord_y + 45

                elif aux_angle in range(155, 200):
                    x_pos = self.tank.cord_x + 45 // 2
                    y_pos = self.tank.cord_y + 45

                elif aux_angle in range(200, 245):
                    x_pos = self.tank.cord_x
                    y_pos = self.tank.cord_y + 45

                elif aux_angle in range(245, 270):
                    x_pos = self.tank.cord_x
                    y_pos = self.tank.cord_y + 45//2

                elif aux_angle < 0:
                    x_pos = self.tank.cord_x
                    y_pos = self.tank.cord_y

                else:
                    x_pos = self.tank.barrel.cord_x + self.tank.barrel.width()//2
                    y_pos = self.tank.barrel.cord_y + self.tank.barrel.height()//2

                bullet = Bullet(kind, self.tank.harm,
                                pos=(int(x_pos), int(y_pos)), owner=self.tank)
                self.all_bullets.append(bullet)
                bullet.move(int(x_pos), int(y_pos))
                bullet.angle = self.tank.barrel.angle

                self.add_entity(bullet)


        elif event.button() == Qt.RightButton:
            # bomba
            if self.tank is not None:
                if self.tank.bombs > 0:
                    new_bomb = Bomb(self.tank.bomb_range, pos=(self.tank.cord_x, self.tank.cord_y))
                    self._bombs.append(new_bomb)
                    self.tank.bombs -= 1
                    self.add_entity(new_bomb)
                    new_bomb.move(new_bomb.cord_x, new_bomb.cord_y)
                    self.set_bombs_left(self.tank)

    def valid_movement(self, tank):
        all_borders = list()
        all_borders.extend([(tank.cord_x, y) for y in
                       range(tank.cord_y, tank.cord_y + tank.size[0])])
        all_borders.extend([(tank.cord_x + tank.size[0], y) for y in
                       range(tank.cord_y, tank.cord_y + tank.size[0])])
        all_borders.extend([(x, tank.cord_y) for x in
                       range(tank.cord_x, tank.cord_x + tank.size[0])])
        all_borders.extend([(x, tank.cord_y + tank.size[0]) for x in
                       range(tank.cord_x, tank.cord_x + tank.size[0])])

        x_pos = tank.cord_x
        y_pos = tank.cord_y

        if x_pos < 88 or x_pos + tank.width() > 750 \
                or y_pos < 83 or y_pos + tank.width() > 597:  # bordes
            return False

        for cord in all_borders:
            if cord in self.forbidden_cords:
                return False

        return True

    def move_barrel(self):
        point = self.mapFromGlobal(self.cursor.pos())  # posicion relativa a widget

        x_pos = point.x()
        y_pos = point.y()

        opuesto = x_pos - self.tank.cord_x
        adyacente = self.tank.cord_y - y_pos
        if adyacente == 0:
            if opuesto > 0:
                new_angle = 90
            else:
                new_angle = 270

        elif opuesto == 0:
            if adyacente > 0:
                new_angle = 0
            else:
                new_angle = 180

        elif adyacente < 0:
            new_angle = degrees(atan(opuesto / adyacente)) + 180
        else:
            new_angle = degrees(atan(opuesto / adyacente))

        self.tank.barrel.angle = new_angle
        return

    def start(self):
        self.error_label.show()
        if self.option1.isChecked():  # stages
            try:
                if int(self.label_stage.text()) in range(1, 9):
                    self.error_label.hide()
                    self.mode = "Stages"
                    self.stage = int(self.label_stage.text())
                    self.init_gui("Stages", self.stage)
                else:
                    self.show_error("invalid stage")
            except ValueError:
                self.show_error("invalid stage")

        elif self.option2.isChecked():  # survival
            self.error_label.hide()
            self.mode = "Survival"
            self.stage = 0
            self.init_gui("Survival")
        else:
            self.show_error("choose one option")
        return

    def pause(self):
        self.start_pause = time.clock()
        self.is_paused = True
        self.set_message("PAUSED GAME")

        self.button_restart = QPushButton('&Continue', self)
        self.button_restart.resize(self.button_pause.sizeHint())
        self.button_restart.move(875, 480)
        self.button_restart.clicked.connect(self.restart)
        self.button_restart.show()
        self.error_label.show()

    def restart(self):
        if self.cooldown:  # vuelve de la tienda
            self.back_to_store = int(time.clock()) + 10

            self.score = self.store.score

            # cambiar stats de tanque
            self.tank.bombs += self.store.bombs_bought
            self.tank.bullets.extend(self.store.bullets_bought)

            stats = self.store.actual_stats
            self.tank.max_hp = stats["hp"]
            self.tank.harm = stats["harm"]
            self.tank.resistance = stats["resistance"]
            self.tank.shoot = stats["shoot"]
            self.tank.bomb_range = stats["bomb_range"]
            self.tank.speed = stats["speed"]

            # mostrar en interfaz
            self.set_bombs_left(self.tank)
            self.set_next_bullets(self.tank)

        self.button_restart.deleteLater()
        self.set_message("")
        self.is_paused = False
        self.end_pause = time.clock()
        self.paused_time += int(self.end_pause - self.start_pause)

        # reinicio para proximo
        self.start_pause = 0
        self.end_pause = 0

    def restart_game(self):
        self.label_level.hide()
        self.label_time.hide()
        self.label_time_fix.hide()
        self.bombs_label.hide()
        self.bullets_label.hide()
        self.bullet1.hide()
        self.bullet2.hide()
        self.bullet3.hide()
        self.label_score.hide()
        self.label_score_fix.hide()
        self.button_pause.hide()
        self.button_quit.hide()

        self.label_start.show()
        self.option1.show()
        self.option2.show()
        self.label_stage = QLineEdit("", self)
        self.label_stage.move(840, 180)
        self.label_stage.show()
        self.button_start.show()

    def game_over_survival(self, score):
        self.final_score = score
        self.label_score_fix.setText("FINAL SCORE:")
        self.label_score_fix.setFixedWidth(
            self.label_score_fix.sizeHint().width())

        self.label_time.hide()
        self.label_time_fix.hide()
        self.bombs_label.hide()
        self.bullets_label.hide()
        self.bullet1.hide()
        self.bullet2.hide()
        self.bullet3.hide()
        self.button_pause.hide()
        self.button_quit.hide()


        self.submission_label = QLabel("Submit your score:", self)
        self.submission_label.move(840, 180)
        self.submission_label.show()

        self.option_yes = QRadioButton("Yes", self)
        self.option_yes.move(840, 220)
        self.label_user = QLineEdit("usuario", self)
        self.label_user.move(840, 250)
        self.option_yes.show()
        self.label_user.show()

        self.option_no = QRadioButton("No", self)
        self.option_no.move(840, 290)
        self.option_no.show()

        self.button_submit = QPushButton('&Submit', self)
        self.button_submit.resize(self.button_submit.sizeHint())
        self.button_submit.move(875, 480)
        self.button_submit.clicked.connect(self.submit)
        self.button_submit.show()

        self.error_label = QLabel("", self)

    def submit(self):
        self.error_label.show()
        if self.option_yes.isChecked():  # yes
            all_users = self.get_users()

            if self.label_user.text() in all_users:  # repetido
                self.show_error("invalid username")
                self.error_label.move(830, 320)
            else:
                self.error_label.hide()
                with open("scores.txt", "a") as file:
                    file.write("{},{}\n".format(self.label_user.text(),
                                              self.final_score))
                self.show_highscores()

        elif self.option_no.isChecked():  # no
            self.end_game = True
        return

    def get_users(self):
        with open("scores.txt", "r") as file:
            return [line.strip().split(",")[0] for line in file]

    def show_highscores(self):
        with open("scores.txt", "r") as file:
            all_scores = [tuple(line.strip().split(",")) for line in file]

        sorted_scores = sorted(all_scores, key=lambda x: int(x[1]), reverse=True)

        rep = ""
        i = 1
        while i <= 10 and (i - 1) < len(sorted_scores):
            score_tuple = sorted_scores[i - 1]
            rep += "{0: <3d}th|{1: ^30s}|{2: ^8d}\n".format(i, score_tuple[0],
                                                            int(score_tuple[1]))
            i += 1

        self.highscores = QLabel(self)
        self.highscores.setGeometry(130, 100, 700, 480)
        self.highscores.setPixmap(QPixmap(get_asset_path(
            ["highscores.png"])).scaled(700, 480, Qt.KeepAspectRatio))
        self.highscores.show()

        self.show_score = QLabel(rep, self)
        self.score_font = QFont("", 15)
        self.score_font.setBold(True)
        self.show_score.setFont(self.score_font)
        self.show_score.move(165, 195)
        self.show_score.show()

    def quit(self):
        self.label_score_fix.setText("FINAL SCORE:")
        self.label_score_fix.setFixedWidth(self.label_score_fix.sizeHint().width())

        self.label_time.hide()
        self.label_time_fix.hide()
        self.bombs_label.hide()
        self.bullets_label.hide()
        self.bullet1.hide()
        self.bullet2.hide()
        self.bullet3.hide()

        self.end_game = True


if __name__ == '__main__':
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec_()