from PyQt4.QtGui import QWidget, QLabel, QPixmap, QApplication, QFont, QIcon
from PyQt4.QtGui import QRadioButton, QLineEdit, QPushButton, QAbstractItemView
from PyQt4.QtGui import QTableWidget, QListWidget, QListWidgetItem, QTableWidgetItem
from PyQt4.QtGui import QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsLineItem
from PyQt4.QtGui import QGraphicsItem, QPainterPath, QPainter, QGraphicsPolygonItem
from PyQt4.QtGui import QSpinBox, QColorDialog, QColor, QPen, QPolygonF
from PyQt4.QtCore import QTimer, Qt, QEvent, QSize, QRectF, QPointF, QLineF, QPoint
from random import choice
from math import sin, cos, radians
import os
import time


def get_absolute_path(relative_path):
    return os.path.join(os.path.dirname(__file__), relative_path)


class Game(QWidget):
    def __init__(self, client, player, participants, online, seconds=0, messages=list()):
        super().__init__()
        self.setFixedSize(1225, 680)
        self.setWindowTitle('Programillo - ¡A dibujar!')

        self.background = QLabel(self)
        self.background.setGeometry(0, 0, 1225, 680)
        self.background.setPixmap(QPixmap(get_absolute_path(
            "./images/background_game.png")).scaled(1225, 680))

        self.setMouseTracking(True)

        # participantes
        self.player = player
        self.participants = participants
        self.client = client

        self.seconds = seconds
        self.label_time = QLabel("{} seg.".format(seconds), self)
        self.label_time.move(1150, 160)
        self.pause = True

        # timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        # online / offline
        self.online = online
        self.offline = [x for x in participants if x not in self.online]

        # chat
        self.game_chat = QListWidget(self)
        self.game_chat.setGeometry(880, 210, 330, 400)
        self.messages = messages

        # painter
        self.painter = None
        self.not_painted = list()

        self.button_send = QPushButton("&>", self)
        self.button_send.move(1170, 619)
        self.button_send.resize(40, 35)
        self.button_send.clicked.connect(self.send_chat)

        self.label_message = QLineEdit("", self)
        self.label_message.setGeometry(880, 620, 280, 33)

        self.colors_used = list()

        # participantes
        self.display_participants = ParticipantsTable(self, participants)
        self.display_participants.setGeometry(20, 80, 240, 180)

        self.button_invite = QPushButton("&Invitar", self)
        self.button_invite.move(150, 265)
        self.button_invite.resize(self.button_invite.sizeHint())

        # dibujos ganadores
        self.display_drawings = DrawingsList(self)
        self.display_drawings.setGeometry(100, 320, 160, 350)

        # mostrar cuando este terminada la imagen
        self.button_save = QPushButton("&Guardar imagen", self)
        self.button_save.move(570, 620)
        self.button_save.resize(self.button_save.sizeHint())
        self.button_save.clicked.connect(self.save_image)
        self.button_save.hide()

        # maneja control juego
        self.button_start = QPushButton("&Empezar ronda!", self)
        self.button_start.move(720, 620)
        self.button_start.resize(self.button_save.sizeHint())
        self.button_start.clicked.connect(self.start_round)

        # opciones
        self.button_drawfree = QPushButton("&}", self)
        self.button_drawfree.setGeometry(300, 30, 40, 40)
        self.button_drawfree.clicked.connect(self.drawfree)

        self.button_drawline = QPushButton("&/", self)
        self.button_drawline.setGeometry(350, 30, 40, 40)
        self.button_drawline.clicked.connect(self.drawline)

        self.button_drawcurve = QPushButton("&)", self)
        self.button_drawcurve.setGeometry(400, 30, 40, 40)
        self.button_drawcurve.clicked.connect(self.drawcurve)

        self.label_width = QLabel("Grosor:", self)
        self.label_width.move(480, 15)

        self.linewidth = QSpinBox(self)
        self.linewidth.setMinimum(1)
        self.linewidth.setMaximum(3)
        self.linewidth.setGeometry(480, 40, 60, 30)

        self.color5_button = QPushButton("Ok", self)
        self.color5_button.setGeometry(550, 40, 30, 30)
        self.color5_button.clicked.connect(self.set_linewidth)

        self.label_colors = QLabel("Colores:", self)
        self.label_colors.move(630, 15)

        self.actual_color = (0, 0, 0)
        self.actual_linewidth = 1
        self.actual_style = 'drawfree'  # 'line', 'curve'

        self.color1 = (0, 0, 0)
        self.color2 = (255, 51, 51)
        self.color3 = (0, 128, 255)
        self.color4 = (255, 255, 0)

        self.color1_button = QPushButton("", self)
        self.color1_button.setGeometry(630, 40, 30, 30)
        self.color1_button.setStyleSheet(
            "background-color: rgb{}".format(str(self.color1)))
        self.color1_button.clicked.connect(self.change_color1)

        self.color2_button = QPushButton("", self)
        self.color2_button.setGeometry(670, 40, 30, 30)
        self.color2_button.setStyleSheet(
            "background-color: rgb{}".format(str(self.color2)))
        self.color2_button.clicked.connect(self.change_color2)

        self.color3_button = QPushButton("", self)
        self.color3_button.setGeometry(710, 40, 30, 30)
        self.color3_button.setStyleSheet(
            "background-color: rgb{}".format(str(self.color3)))
        self.color3_button.clicked.connect(self.change_color3)

        self.color4_button = QPushButton("", self)
        self.color4_button.setGeometry(750, 40, 30, 30)
        self.color4_button.setStyleSheet(
            "background-color: rgb{}".format(str(self.color4)))
        self.color4_button.clicked.connect(self.change_color4)

        self.color5_button = QPushButton("+", self)
        self.color5_button.setGeometry(790, 40, 30, 30)
        self.color5_button.clicked.connect(self.search_color)

        # templates
        self.button_circle = QPushButton("&◯", self)
        self.button_circle.setGeometry(830, 80, 40, 40)
        self.button_circle.clicked.connect(self.circle)

        self.button_square = QPushButton("&◻", self)
        self.button_square.setGeometry(830, 130, 40, 40)
        self.button_square.clicked.connect(self.square)

        self.button_triangle = QPushButton("&△", self)
        self.button_triangle.setGeometry(830, 180, 40, 40)
        self.button_triangle.clicked.connect(self.triangle)

        self.button_rectangle = QPushButton("&▯", self)
        self.button_rectangle.setGeometry(830, 230, 40, 40)
        self.button_rectangle.clicked.connect(self.rectangle)

        # dibujo
        self.paint = PaintView(self)
        self.paint.setGeometry(300, 80, 520, 520)

    def send_chat(self):
        # actualizar todos los amigos RR
        message = "{}: {}".format(self.player, self.label_message.text())
        self.update_chat(message)
        self.label_message.setText("")
        return

    def update_chat(self, message):
        self.game_chat.addItem(message)
        self.messages.append(message)
        return

    def choose_painter(self):
        if len(self.not_painted) == 0:
            # fin de la partida
            pass

        else:
            to_paint = choice(self.not_painted)
            self.not_painted.remove(to_paint)
            self.update_chat(" > Ahora dibuja {}".format(to_paint))

            if to_paint == self.player:
                self.button_send.hide()

    def winner_drawing(self, path):
        self.display_drawings.add_drawing(path)
        return

    def save_image(self):  # hacer el proceso de pasar a png
        pass

    def start_round(self):
        self.pause = False
        self.choose_painter()
        self.button_start.hide()
        self.paint.scene().clear()  # borra dibujo anterior

    def end_round(self):
        if self.player == self.painter:
            self.button_send.show()

        self.player = None
        self.pause = True
        self.button_save.show()
        self.button_start.show()

    def update_time(self):
        if not self.pause:
            self.seconds += 1
            self.set_time(self.seconds)

    def set_time(self, time):
        self.label_time.setText("{} seg.".format(str(time)))
        self.label_time.setFixedWidth(self.label_time.sizeHint().width())

    def drawfree(self):
        self.actual_style = 'drawfree'
        self.paint.style = 'drawfree'

    def drawline(self):
        self.actual_style = 'line'
        self.paint.style = 'line'
        self.paint.line_start = None
        self.paint.line_end = None

    def drawcurve(self):
        self.actual_style = 'curve'
        self.paint.style = 'curve'

        self.paint.curve1 = None
        self.paint.curve2 = None
        self.paint.curve3 = None

    def circle(self):
        self.actual_style = 'circle'
        self.paint.style = 'circle'
        self.paint.create_figure()

    def square(self):
        self.actual_style = 'square'
        self.paint.style = 'square'
        self.paint.create_figure()

    def triangle(self):
        self.actual_style = 'triangle'
        self.paint.style = 'triangle'
        self.paint.create_figure()

    def rectangle(self):
        self.actual_style = 'rectangle'
        self.paint.style = 'rectangle'
        self.paint.create_figure()

    def update_color(self, color):
        self.colors_used.append(color)
        all_colors = []

        for color in self.colors_used:
            if color not in all_colors:
                all_colors.append((color, self.colors_used.count(color)))

        most_common = sorted(all_colors, key=lambda x: x[1])

        if len(most_common) >= 4:
            self.color1 = most_common[0][0]
            self.color2 = most_common[1][0]
            self.color3 = most_common[2][0]
            self.color4 = most_common[3][0]

        elif len(most_common) == 3:
            self.color2 = most_common[0][0]
            self.color3 = most_common[1][0]
            self.color4 = most_common[2][0]

        elif len(most_common) == 2:
            self.color3 = most_common[0][0]
            self.color4 = most_common[1][0]

        elif len(most_common) == 1:
            self.color4 = most_common[0][0]

        self.color1_button.setStyleSheet(
            "background-color: rgb{}".format(str(self.color1)))
        self.color2_button.setStyleSheet(
            "background-color: rgb{}".format(str(self.color2)))
        self.color3_button.setStyleSheet(
            "background-color: rgb{}".format(str(self.color3)))
        self.color4_button.setStyleSheet(
            "background-color: rgb{}".format(str(self.color4)))

    def change_color1(self):
        self.actual_color = self.color1
        self.paint.color = self.color1
        self.update_color(self.color1)

    def change_color2(self):
        self.actual_color = self.color2
        self.paint.color = self.color2
        self.update_color(self.color2)

    def change_color3(self):
        self.actual_color = self.color3
        self.paint.color = self.color3
        self.update_color(self.color3)

    def change_color4(self):
        self.actual_color = self.color4
        self.paint.color = self.color4
        self.update_color(self.color4)

    def search_color(self):
        self.color_dialog = QColorDialog(self)
        color = QColor(0, 0, 0, 0).rgba()
        self.color_dialog.setCustomColor(0, color)

        selected = self.color_dialog.getColor()

        if selected.isValid():
            rgb = (selected.red(), selected.green(), selected.blue())
            self.actual_color = rgb
            self.paint.color = rgb
            self.update_color(rgb)

    def set_linewidth(self):
        self.actual_linewidth = self.linewidth.value()
        self.paint.actual_linewdith = self.linewidth.value() * 2

    def closeEvent(self, QCloseEvent):
        to_send = "game;close;{};{}".format(self.player, ";".join(self.participants))
        if self.client is not None:
            self.client.send(to_send)
        QCloseEvent.accept()

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


class PaintView(QGraphicsView):
    def __init__(self, parent):
        QGraphicsView.__init__(self, parent)

        self.style = 'drawfree'
        self.color = (0, 0, 0)
        self.actual_linewdith = 2

        self.line_start = None
        self.line_end = None

        self.curve1 = None
        self.curve2 = None
        self.curve3 = None

        self.next_point = None
        self.drawing = True

        self.add_item = None

        self.setScene(QGraphicsScene(self))
        self.setSceneRect(QRectF(self.viewport().rect()))

    def mouseMoveEvent(self, event):
        if self.drawing:
            start = QPointF(self.mapToScene(event.pos()))

            if self.next_point is not None:
                line = QGraphicsLineItem(QLineF(start, self.next_point))
                pen = QPen(QColor(self.color[0], self.color[1], self.color[2]))
                pen.setWidth(self.actual_linewdith)

                line.setPen(pen)
                self.scene().addItem(line)
                self.next_point = start

            else:
                line = QGraphicsLineItem(QLineF(start, start))
                pen = QPen(QColor(self.color[0], self.color[1], self.color[2]))
                pen.setWidth(self.actual_linewdith)

                line.setPen(pen)
                self.scene().addItem(line)
                self.next_point = start

    def mousePressEvent(self, event):
        if self.style == "line":
            if self.line_start is None:  # inicio
                self.line_start = event.pos()
            else: # fin
                self.line_end = event.pos()

        elif self.style == "curve":
            if self.curve1 is None:  # inicio
                self.curve1 = event.pos()
            elif self.curve2 is None:
                self.curve2 = event.pos()
            else:  # fin
                self.curve3 = event.pos()

        elif self.style == "circle" or self.style == "rectangle":
            if self.add_item is not None:
                pos = QPointF(self.mapToScene(event.pos()))
                self.add_item.setPos(pos.x() - self.add_item.boundingRect().width()//2,
                                     pos.y() - self.add_item.boundingRect().height()//2)
                self.add_item = None

        elif self.style == "square" or self.style == "triangle":
            if self.add_item is not None:
                pos = QPointF(self.mapToScene(event.pos()))
                self.add_item.setPos(pos.x(), pos.y())
                self.add_item = None

        elif self.style == "drawfree":
            self.drawing = True

    def mouseReleaseEvent(self, event):
        if self.style == "line":
            if self.line_start is not None and self.line_end is not None:
                start = QPointF(self.mapToScene(self.line_start))
                end = QPointF(self.mapToScene(self.line_end))

                line = QGraphicsLineItem(QLineF(start, end))
                pen = QPen(QColor(self.color[0], self.color[1], self.color[2]))
                pen.setWidth(self.actual_linewdith)

                line.setPen(pen)
                self.scene().addItem(line)

                self.line_start = None
                self.line_end = None

        elif self.style == "curve":
            if self.curve1 is not None and self.curve2 is not None and self.curve3 is not None:
                start = QPointF(self.mapToScene(self.curve1))
                control = QPointF(self.mapToScene(self.curve2))
                end = QPointF(self.mapToScene(self.curve3))

                cubicPath = QPainterPath(start)
                cubicPath.cubicTo(control, control, end)

                pen = QPen(QColor(self.color[0], self.color[1], self.color[2]))
                pen.setWidth(self.actual_linewdith)

                self.scene().addPath(cubicPath, pen)

                self.curve1 = None
                self.curve2 = None
                self.curve3 = None

        elif self.style == "drawfree":
            self.drawing = False
            self.next_point = None

    def create_figure(self):
        if self.style == "circle":
            self.add_item = QGraphicsEllipseItem(0, 0, 50, 50)

            pen = QPen(QColor(self.color[0], self.color[1], self.color[2]))
            pen.setWidth(self.actual_linewdith)

            self.add_item.setPen(pen)
            self.scene().addItem(self.add_item)

        elif self.style == "square":
            polygon = self.createPoly(4, 50, 45)
            self.add_item = QGraphicsPolygonItem(polygon)

            pen = QPen(QColor(self.color[0], self.color[1], self.color[2]))
            pen.setWidth(self.actual_linewdith)
            self.add_item.setPen(pen)

            self.scene().addItem(self.add_item)

        elif self.style == "triangle":
            polygon = self.createPoly(3, 50, 270)
            self.add_item = QGraphicsPolygonItem(polygon)

            pen = QPen(QColor(self.color[0], self.color[1], self.color[2]))
            pen.setWidth(self.actual_linewdith)
            self.add_item.setPen(pen)

            self.scene().addItem(self.add_item)

        elif self.style == "rectangle":
            polygon = self.createPoly(4, 50, 0, True)
            self.add_item = QGraphicsPolygonItem(polygon)

            pen = QPen(QColor(self.color[0], self.color[1], self.color[2]))
            pen.setWidth(self.actual_linewdith)
            self.add_item.setPen(pen)

            self.scene().addItem(self.add_item)

    def createPoly(self, n, r, s, rectangle=False):  # n puntos, radio y angulo
        polygon = QPolygonF()

        if rectangle:
            polygon.append(QPointF(0, 0))
            polygon.append(QPointF(100, 0))
            polygon.append(QPointF(100, 50))
            polygon.append(QPointF(0, 50))
            return polygon

        w = 360 / n  # angle per step
        for i in range(n):  # add the points of polygon
            t = w * i + s
            x = r * cos(radians(t))
            y = r * sin(radians(t))
            polygon.append(QPointF(x, y))

        return polygon


if __name__ == "__main__":
    app = QApplication([])
    game = Game(None, "isidora", ["tere", "antonia"], ["tere", "antonia"])
    game.show()
    game.winner_drawing("./images/1.jpg")
    game.winner_drawing("./images/2.jpg")
    game.winner_drawing("./images/3.jpg")
    game.winner_drawing("./images/4.gif")
    app.exec_()

