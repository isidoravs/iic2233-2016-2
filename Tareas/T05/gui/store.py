from PyQt4.QtGui import QWidget, QLabel, QPixmap, QApplication, QFont, QIntValidator
from PyQt4.QtGui import QRadioButton, QLineEdit, QPushButton
from PyQt4.QtCore import QTimer, Qt
from .utils import get_asset_path


class Store(QWidget):

    def __init__(self, player_score, actual_stats):
        super().__init__()
        self.setFixedSize(1800, 900)
        self.setWindowTitle('Hacker Tanks! - Store')

        self.__timer = QTimer(self)

        self.background = QLabel(self)
        self.background.setGeometry(0, 0, 1800, 900)
        self.background.setPixmap(QPixmap(get_asset_path(["store_background.png"])
                                          ).scaled(1800, 900))

        self.font = QFont("", 20)
        self.font.setBold(True)

        self.label_score = QLabel(str(player_score), self)
        self.label_score.setFont(self.font)
        self.label_score.move(1550, 200)

        self.qty1 = QLineEdit("0", self)
        self.qty1.setGeometry(200, 110, 100, 45)

        self.qty2 = QLineEdit("0", self)
        self.qty2.setGeometry(200, 310, 100, 45)

        self.qty3 = QLineEdit("0", self)
        self.qty3.setGeometry(200, 450, 100, 45)

        self.qty4 = QLineEdit("0", self)
        self.qty4.setGeometry(200, 590, 100, 45)

        self.buy_button = QPushButton('&Buy Power-ups', self)
        self.buy_button.setGeometry(500, 750, 200, 50)
        self.buy_button.clicked.connect(self.buy)

        self.font1 = QFont("", 10)
        self.font1.setBold(True)

        self.buy_message = QLabel("", self)
        self.buy_message.setFont(self.font1)
        self.buy_message.move(200, 760)

        self.stats1 = QRadioButton("", self)
        self.stats1.setGeometry(980, 390, 30, 30)

        self.stats2 = QRadioButton("", self)
        self.stats2.setGeometry(980, 495, 30, 30)

        self.stats3 = QRadioButton("", self)
        self.stats3.setGeometry(980, 605, 30, 30)

        self.stats4 = QRadioButton("", self)
        self.stats4.setGeometry(980, 715, 30, 30)

        self.stats5 = QRadioButton("", self)
        self.stats5.setGeometry(1385, 390, 30, 30)

        self.stats6 = QRadioButton("", self)
        self.stats6.setGeometry(1385, 495, 30, 30)

        self.upgrade_stats_button = QPushButton('&Buy Power-ups', self)
        self.upgrade_stats_button.setGeometry(1500, 750, 200, 50)
        self.upgrade_stats_button.clicked.connect(self.upgrade_stats)

        self._score = player_score
        self.bullets_bought = list()
        self.bombs_bought = 0
        self.actual_stats = actual_stats

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, other):
        self._score = other

    def update_score(self):
        self.label_score.setText(str(self.score))
        self.label_score.setFixedWidth(self.label_score.sizeHint().width())

    def buy(self):
        if self.qty1.text() == "":
            self.qty1.setText("0")

        if self.qty2.text() == "":
            self.qty2.setText("0")

        if self.qty3.text() == "":
            self.qty3.setText("0")

        if self.qty4.text() == "":
            self.qty4.setText("0")

        try:
            cost = int(self.qty1.text()) * 50 + int(self.qty2.text()) * 20 + \
                   int(self.qty3.text()) * 50 + int(self.qty4.text()) * 60
        except ValueError:
            self.edit_buy_message("ERROR: enter valid quantity")
        else:  # si no ocurre error
            if cost > self.score:
                self.edit_buy_message("ERROR: not enough score")
            else:
                self.score -= cost
                self.update_score()
                self.edit_buy_message("SUCCESS! Cost: {}".format(cost))

                if int(self.qty1.text()) > 0:
                    # bombs
                    self.bombs_bought += int(self.qty1.text())

                if int(self.qty2.text()) > 0:
                    # explosive
                    self.bullets_bought.extend(["e", "e", "e"] * int(self.qty2.text()))

                if int(self.qty3.text()) > 0:
                    # penetrante
                    self.bullets_bought.extend(["p", "p", "p"] * int(self.qty3.text()))

                if int(self.qty4.text()) > 0:
                    # ralentizante
                    self.bullets_bought.extend(["r", "r", "r"] * int(self.qty4.text()))

                self.qty1.setText("0")
                self.qty2.setText("0")
                self.qty3.setText("0")
                self.qty4.setText("0")

    def edit_buy_message(self, message):
        self.buy_message.setText(message)
        self.buy_message.setFixedWidth(self.buy_message.sizeHint().width())

    def upgrade_stats(self):
        if self.stats1.isChecked():
            cost = 5 * self.actual_stats["harm"]
            if self.score >= cost:
                self.actual_stats["harm"] += 1
                self.edit_buy_message("SUCCESS! Cost: {}".format(cost))
                self.score -= cost
            else:
                self.edit_buy_message("ERROR: not enough score")

        elif self.stats2.isChecked():
            cost = 5 * self.actual_stats["hp"]
            if self.score >= cost:
                self.actual_stats["hp"] += 1
                self.edit_buy_message("SUCCESS! Cost: {}".format(cost))
                self.score -= cost
            else:
                self.edit_buy_message("ERROR: not enough score")

        elif self.stats3.isChecked():
            cost = 5 * self.actual_stats["speed"]
            if self.score >= cost:
                self.actual_stats["speed"] += 1
                self.edit_buy_message("SUCCESS! Cost: {}".format(cost))
                self.score -= cost
            else:
                self.edit_buy_message("ERROR: not enough score")

        elif self.stats4.isChecked():
            cost = 5 * self.actual_stats["shoot"]
            if self.score >= cost:
                self.actual_stats["shoot"] += 1
                self.edit_buy_message("SUCCESS! Cost: {}".format(cost))
                self.score -= cost
            else:
                self.edit_buy_message("ERROR: not enough score")

        elif self.stats5.isChecked():
            cost = 5 * self.actual_stats["resistance"]
            if self.score >= cost:
                self.actual_stats["resistance"] += 1
                self.edit_buy_message("SUCCESS! Cost: {}".format(cost))
                self.score -= cost
            else:
                self.edit_buy_message("ERROR: not enough score")

        elif self.stats6.isChecked():
            cost = 5 * self.actual_stats["bomb_range"]
            if self.score >= cost:
                self.actual_stats["bomb_range"] += 1
                self.edit_buy_message("SUCCESS! Cost: {}".format(cost))
                self.score -= cost
            else:
                self.edit_buy_message("ERROR: not enough score")

        else:
            self.edit_buy_message("ERROR: choose one stat")

        self.update_score()


if __name__ == '__main__':
    app = QApplication([])
    store_window = Store(1000, {"harm": 0, "hp": 0, "resistance": 0, "speed": 0,
                                "shoot": 0, "bomb_range": 0})
    store_window.show()
    app.exec_()