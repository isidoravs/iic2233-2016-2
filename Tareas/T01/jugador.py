# modulo para un jugador y su informacion


class Jugador:
    def __init__(self, unique_id, unique_name, password, primer_programon):
        self.unique_id = unique_id
        self.unique_name = unique_name
        self.password = password
        self.yenes = 1000
        self.progradex = Progradex(primer_programon)  # revisar jugadoresEjemplo.jason ? RR
        self.medals = []  # si gana al lider, nombre ciudad
        self.prograbolas = 10
        self.location = Ciudad("Pallet Town", 0, [None, None])  # no hay trainers
        self.equipo = [primer_programon]
        self.batallas = {}  # almacena informacion de batallas {"ciudad": [["trainer.name", ganadas, perdidas]]}

    # manera de actualizar la info al cerrar
    # se obtiene del dictionario con la informacion
    def set_location(self, new_location):
        self.location = new_location

    def __str__(self):
        info_jugador = "-- Jugador {} --\n ".format(self.unique_name)
        info_jugador += "ID: {}\n Yenes: {}\n Prograbolas: {}\n Ubicacion: " \
                        "{}\n ".format(self.unique_id, self.yenes, self.prograbolas, self.location)
        if self.medals == []:
            info_jugador += "Medallas: 0"
        else:
            info_jugador += "Medallas: " + str(len(self.medals)) + "\n > ".join(self.medals)
        return info_jugador

    # metodo para actualizar progradex




