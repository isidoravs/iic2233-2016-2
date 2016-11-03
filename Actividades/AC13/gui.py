from PyQt4 import QtGui, QtCore
import os
import json
import pickle
import sys
from clases import Team, Player
import time
from main import get_team, MyEncoder, ConsultasANPF


class ANPF(QtGui.QWidget):

    def __init__(self):
        super().__init__()
        self.inicializa_GUI()


    def inicializa_GUI(self):
        self.setFixedSize(1000, 800)
        self.setWindowTitle("ANFP - Consultas y cambios")

        self.etiqueta = QtGui.QLabel('Bienvenido! Seleccione una opcion:', self)
        self.etiqueta.move(50, 50)

        self.boton1 = QtGui.QPushButton('Transformar pickle a json', self)
        self.boton1.move(150, 200)
        self.boton1.resize(self.boton1.sizeHint())
        self.boton1.clicked.connect(self.parte1)

        self.etiqueta1 = QtGui.QLabel('Consultas y cambios:', self)
        self.etiqueta1.move(150, 300)

        self.boton1 = QtGui.QPushButton('Mostrar todos los jugadores', self)
        self.boton1.move(200, 400)
        self.boton1.resize(self.boton1.sizeHint())
        self.boton1.clicked.connect(self.mostrar)


        self.boton1 = QtGui.QPushButton('Get player', self)
        self.boton1.move(200, 450)
        self.boton1.resize(self.boton1.sizeHint())
        self.boton1.clicked.connect(self.get_player_gui)
        self.label_id = QtGui.QLineEdit("", self)
        self.label_id.move(320, 455)

        self.boton1 = QtGui.QPushButton('Change player', self)
        self.boton1.move(200, 500)
        self.boton1.resize(self.boton1.sizeHint())
        self.boton1.clicked.connect(self.change_player_gui)

        self.boton1 = QtGui.QPushButton('Guardar archivos', self)
        self.boton1.move(150, 650)
        self.boton1.resize(self.boton1.sizeHint())
        self.boton1.clicked.connect(self.parte3)



    def parte1(self):
        # PARTE 1
        # deserializacion pickle
        all_files = os.listdir("db/equipos/")

        # guarda todos los jugadores en lista
        all_players = dict()
        for file in all_files:
            team_players = get_team("db/equipos/" + file)
            all_players.update(team_players)

        # crear un nuevo archivo json
        with open("all_players.json", "w") as file:
            json.dump(all_players, file, cls=MyEncoder)

        self.msje1 = QtGui.QLabel('Transformado!', self)
        self.msje1.move(150, 250)
        self.msje1.show()

    def parte3(self):
        all_files = os.listdir("db/equipos/")

        # guarda todos los jugadores en lista
        all_players = dict()
        for file in all_files:
            team_players = get_team("db/equipos/" + file)
            all_players.update(team_players)

        with open("all_players.json", "r") as file:
            json_data = json.load(file)

        all_teams = list()
        for player in json_data.values():
            if player["equipo"] not in all_teams:
                all_teams.append(player["equipo"])  # diccionario con info

        for team in all_teams:
            jugadores = [player for player in all_players.values()
                         if player.equipo == team]  # player instancia de Player
            new_team = Team(team, *jugadores)

            with open("orden_equipos/{}".format(team), "wb") as file:
                pickle.dump(new_team, file)  # serializa la instancia de Team

        self.msje2 = QtGui.QLabel('Transformado!', self)
        self.msje2.move(150, 700)
        self.msje2.show()

    def mostrar(self):
        with open("all_players.json", "r") as file:
            json_data = json.load(file)

        consultas = ConsultasANPF(json_data)
        consultas.show_all()
        self.msje3 = QtGui.QLabel('Jugadores mostrados en consola', self)
        self.msje3.move(600, 400)
        self.msje3.show()

    def get_player_gui(self):
        ide = self.label_id.text()
        with open("all_players.json", "r") as file:
            json_data = json.load(file)

        consultas = ConsultasANPF(json_data)
        consultas.get_player(ide)


    def change_player_gui(self):
        with open("all_players.json", "r") as file:
            json_data = json.load(file)

        consultas = ConsultasANPF(json_data)
        consultas.change_player("920", {"faltas": 1})


if __name__ == '__main__':
    app = QtGui.QApplication([])
    ventana = ANPF()
    ventana.show()
    app.exec_()