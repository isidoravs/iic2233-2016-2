# modulo para un jugador y su informacion
from implementos import Progradex
from ciudades import Ciudad


class Jugador:
    def __init__(self, unique_id, unique_name, password, primer_programon, PC):
        self.unique_id = unique_id
        self.unique_name = unique_name
        self.password = password
        self.yenes = 1000
        self.progradex = Progradex(primer_programon)  # revisar jugadoresEjemplo.json ? RR
        self.medals = []  # si gana al lider, nombre ciudad
        self.prograbolas = 10
        self.location = Ciudad("Pallet Town", 0, PC)  # objeto de la clase Ciudad o None
        self.location_id = 0
        self.equipo = [primer_programon]
        self.batallas = {}  # almacena informacion de batallas revisar jugadoresEjemplo.json
                            # {"ciudad1": [ ... json ], "ciudad2": [ ... json], ...}

    def __str__(self):
        info_jugador = "-- Jugador {} --\n ".format(self.unique_name)
        info_jugador += "ID: {}\n Yenes: {}\n Prograbolas: {}\n ".format(self.unique_id, self.yenes, self.prograbolas)
        if self.location is None:
            info_jugador += "Ubicacion: Hierba\n "
        else:
            info_jugador += "Ubicacion: {}\n ".format(self.location.name)
        if self.medals == []:
            info_jugador += "Medallas: 0"
        else:
            info_jugador += "Medallas: " + str(len(self.medals)) + "\n > ".join(self.medals)
        return info_jugador

    # metodo para actualizar progradex


if __name__ == "__main__":
    print("Module being run directly")



