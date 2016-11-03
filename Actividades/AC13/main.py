import pickle
import json
from clases import Team, Player
import os
#
# def leer_jugadores(archivo):
#     jugadores = {}
#     with open(archivo, 'r') as file:
#         _jugadores = json.load(file)
#         for k, v in values.items():
#             _player = Player(k, None)
#             _player.update(**v)
#             jugadores[k] = _player
#     return jugadores

def get_team(path):
    jugadores = dict()
    with open(path, "rb") as file:
        team = pickle.load(file)
        for jug in team.jugadores:
            jugadores.update({jug.id: jug})
    return jugadores


class MyEncoder(json.JSONEncoder):
    def default(self, jug):
        if isinstance(jug, Player):
            return {"faltas": int(jug.faltas),
                    "amarillas": int(jug.amarillas),
                    "goles": int(jug.goles),
                    "equipo": jug.equipo,
                    "asistencias": int(
                        jug.asistencias),
                    "id": jug.id,
                    "nombre": jug.nombre,
                    "rojas": int(jug.rojas)}

class ConsultasANPF:
    def __init__(self, json_dict):
        self.data = json_dict

    def show_all(self):
        print("{0: ^30s}|{1: ^7s}|{2: ^11s}|{3: ^7s}".format("NOMBRE", "GOLES", "AMARILLAS", "ROJAS"))
        print("-" * 60)

        for player in self.data.values():  # diccionario de info
            print("{0: <30s}|{1: ^7d}|{2: ^11d}|{3: ^7d}".format(player["nombre"],
                                                                 player["goles"],
                                                                 player["amarillas"],
                                                                 player["rojas"]))

    def get_player(self, ide):
        for player_id in self.data:
            if player_id == ide:  # string segun enunciado
                aux = self.data[player_id]
                print("\n ID: {}".format(ide))
                print("Nombre: {}\n Equipo: {}\n Goles: {}\n Faltas: "
                      "{}\n Amarillas: {}\n Rojas: {}\n Asistencias: {}"
                      "\n".format(aux["nombre"], aux["equipo"], str(aux["goles"]),
                                  str(aux["faltas"]), str(aux["amarillas"]),
                                  str(aux["rojas"]), str(aux["asistencias"])))
                break

    def change_player(self, ide, new_attr):  # kwargs de la forma {attr: value}
        for player_id in self.data:
            if player_id == ide:
                aux = self.data[player_id]

                # instancia
                p = Player(ide, aux["nombre"])
                p.equipo = aux["equipo"]
                p.goles = aux["goles"]
                p.faltas = aux["faltas"]
                p.rojas = aux["rojas"]
                p.amarillas = aux["amarillas"]
                p.asistencias = aux["asistencias"]

                # actualizo
                p.update(new_attr)

                # cambiar en json
                self.data[player_id] = p.__dict__
                break


def main():
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

    # PARTE 2
    with open("all_players.json", "r") as file:
        json_data = json.load(file)

    consultas = ConsultasANPF(json_data)
    consultas.show_all()

    consultas.get_player("920")

    consultas.change_player("920", {"faltas": 1})
    consultas.get_player("920")

    # PARTE 3
    all_teams = list()
    for player in json_data.values():
        if player["equipo"] not in all_teams:
            all_teams.append(player["equipo"])  # diccionario con info

    print("Comprobar serializacion:")
    for team in all_teams:
        jugadores = [player for player in all_players.values()
                     if player.equipo == team]  # player instancia de Player
        new_team = Team(team, *jugadores)

        with open("orden_equipos/{}".format(team), "wb") as file:
            pickle.dump(new_team, file)  # serializa la instancia de Team

        '''
            Comentar estas lineas, eran para comprobar
        '''
        with open("orden_equipos/{}".format(team), "rb") as file:
            equipo = pickle.load(file)  # comprobar
            print("\n {}".format(equipo))
            print(type(equipo))
            print(equipo.tiempo_serializacion)

    # PARTE 4
    





if __name__ == '__main__':
    main()
