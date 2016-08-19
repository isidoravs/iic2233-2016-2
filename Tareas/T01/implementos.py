# articulos a utilizar de cada jugador


class Prograbola:
    def __init__(self):
        self.utilizable = True

    def capturar_programon_salvaje(self, programon):  # RR
        if True:
            self.utilizable = False
            # lo que ocurra con el programon
        else:
            # lo que ocurre si no es capturado
            pass


class Progradex:
    # caracteristicas generales, duplicados cambiar lugar visto/capturado
    def __init__(self, primer_programon):
        self.programones_vistos = []
        # en batallas, nombre y ide
        self.programones_capturados = [primer_programon]
        # con prograbola, toda su info

    def show_programones(self):
        # mostrar vistos y capturados en menu
        # return
        pass

