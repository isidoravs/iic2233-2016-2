# modulo para un jugador y su informacion
from ciudades import Ciudad
from jsonReader import jsonToDict


class Jugador:
    def __init__(self, unique_id, unique_name, password, primer_programon, PC):
        self.unique_id = unique_id
        self.unique_name = unique_name
        self.password = password
        self.yenes = 1000
        self.progradex = Progradex(primer_programon)
        self.medals = []  # si gana al lider, nombre ciudad
        self.prograbolas = 10
        self.location = Ciudad("Pallet Town", 0, PC)  # objeto de la clase Ciudad o None
        self.location_id = 0
        if primer_programon is None:  # cargar datos
            self.equipo = []
        else:
            self.equipo = [primer_programon]
        self.batallas = {}
        # {"ciudad1": [[entrenador, victorias], ... ], "ciudad2": [ ... json], ...}
        # cada value es una lista de listas tipo [trainer, victorias]

    def __str__(self):
        info_jugador = "-- Jugador {} --\n ".format(self.unique_name)
        info_jugador += "ID: {}\n Yenes: {}\n Prograbolas: {}\n ".format(self.unique_id, self.yenes, self.prograbolas)
        if self.location is None:
            info_jugador += "Ubicacion: Hierba\n "
        else:
            info_jugador += "Ubicacion: {}\n ".format(self.location.name)
        if len(self.medals) == 0:
            info_jugador += "Medallas: 0"
        else:
            info_jugador += "Medallas: " + str(len(self.medals)) + "\n > " + "\n > ".join(self.medals)
        return info_jugador


class Progradex:
    # caracteristicas generales, duplicados cambiar lugar visto/capturado
    def __init__(self, primer_programon):
        self.programones_vistos = []
        if primer_programon is None:  # carga de datos
            self.programones_capturados = []
        else:
            self.programones_capturados = [primer_programon]

    def show_programones(self):
        rutas = jsonToDict("datos/routes.json")
        # capturados
        print("----> Programones capturados:")
        for capturado in self.programones_capturados:
            print(capturado)

        # vistos
        print("\n----> Programones vistos:")
        if len(self.programones_vistos) == 0:
            print("No has visto ningun programon")
        else:
            for visto in self.programones_vistos:
                location = "Pallet Town"
                ide = visto.visto_capturado
                if ide % 4 == 0:
                    for ruta in rutas:
                        if (ide // 4) == ruta["route"]:
                            location = ruta["destination"]
                else:
                    location = "hierba, ruta {}".format(ide // 4 + 1)
                print("~ {} ~\n ID: {} | Tipo: {}\n Ultima vez visto: {}\n".format(visto.name, visto.ide,
                                                                                   visto.tipo, location))

        return


if __name__ == "__main__":
    print("Module being run directly")
