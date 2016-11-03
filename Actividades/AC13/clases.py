import time


class Team():
    def __init__(self, nombre, *jugadores):
        self.nombre = nombre
        self.jugadores = list(jugadores)
        self.fecha_modificacion = None

    def update_players(self, *jugadores):
        for jugador in jugadores:
            if type(jugador) == Player and not (jugador in self.jugadores):
                self.jugadores.append(jugador)
            else:
                raise Exception("Value is not type Player")

    def show_players(self):
        print(self)
        print(*self.jugadores, sep="\n")

    def __getstate__(self):
        new_dict = self.__dict__.copy()
        new_dict.update({"tiempo_serializacion": time.strftime('%X %x %Z')})
        return new_dict

    def __repr__(self):
        return "Equipo {0}".format(self.nombre)


class Player():
    def __init__(self, ide, nombre):
        self.id = ide
        self.nombre = nombre
        self.asistencias = None
        self.goles = None
        self.amarillas = None
        self.faltas = None
        self.rojas = None
        self.equipo = None
        self.all_updates = list()  # almacena tiempo y tipo de cambios en tuplas

    # agregado por mi
    def update(self, new_attr):
        aux_time = time.strftime('%X %x %Z')
        print("UPDATE - player ID: {} | time: {}".format(self.id, aux_time))

        updates = ""

        new_dict = self.__dict__.copy()
        for key in new_attr.keys():
            if key in self.__dict__.keys():
                new_dict.update({key: new_attr[key]})

                updates += "updated {}: {} -> {}\n".format(key, self.__dict__[key], new_attr[key])

        print(updates)
        self.__dict__ = new_dict  # actualizo
        self.all_updates.append((aux_time, updates))

    def __repr__(self):
        return 'ID Jugador {0}'.format(self.id)
