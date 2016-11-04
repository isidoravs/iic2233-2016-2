from PyQt4.QtGui import QWidget, QLabel, QPixmap, QApplication, QFont, QIntValidator
from PyQt4.QtGui import QRadioButton, QLineEdit, QPushButton
from PyQt4.QtCore import QTimer, Qt
from .utils import get_asset_path


class Store(QWidget):

    def __init__(self, player_score):
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

        self.qty1 = QLineEdit("", self)
        self.qty1.setGeometry(200, 110, 100, 45)

        self.qty2 = QLineEdit("", self)
        self.qty2.setGeometry(200, 310, 100, 45)

        self.qty3 = QLineEdit("", self)
        self.qty3.setGeometry(200, 450, 100, 45)

        self.qty4 = QLineEdit("", self)
        self.qty4.setGeometry(200, 590, 100, 45)

        self.buy_button = QPushButton('&Buy Power-ups', self)
        self.buy_button.setGeometry(500, 750, 200, 50)
        self.buy_button.clicked.connect(self.buy)

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
        pass

    def upgrade_stats(self):
        pass


if __name__ == '__main__':
    app = QApplication([])
    store_window = Store(1000)
    store_window.show()
    app.exec_()