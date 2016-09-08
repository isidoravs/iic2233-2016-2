# AC05
from random import randint, choice
from functools import reduce


class Jugador:
    def __init__(self, jugador, ide):
        self.nombre = jugador[0]
        self.elo = jugador[1]
        self.ide = ide
        self.puntos = 0
        self.partidas_ganadas = 0

    def ganar(self):
        self.puntos += 6
        self.partidas_ganadas += 1
        return

    def perder(self):
        self.puntos += randint(0,5)
        return

    def __repr__(self):
        return "Jugador {}, elo: {}, id: {}, ganadas: {}, puntaje: {}".format(self.nombre, self.elo, self.ide,
                                                                              self.partidas_ganadas, self.puntos)

class Campeonato:
    def __init__(self, jugadores):
        self.jugadores = jugadores
        self.cantidad_rondas = 0
        self.apuestas = []
        self.iniciar()

    def iniciar(self):
        self.primera_ronda()
        ver = self.rondas()
        return ver

    def primera_ronda(self):
        print("Comienza la primera ronda")
        self.cantidad_rondas += 1
        sorted_elo = sorted(self.jugadores, key=lambda x: x.elo)
        par = list(filter(lambda x: x.ide % 2 == 0, sorted_elo))
        impar = list(filter(lambda x: x.ide % 2 != 0, sorted_elo))
        partidas = list(zip(par, impar))
        self.finalizar_partida(partidas)

        apuesta = randint(0, 1000)
        self.apuestas.append(apuesta)
        self.print_apuesta()
        return

    def rondas(self):
        self.cantidad_rondas += 1
        print("Comienza la ronda {}".format(self.cantidad_rondas))
        ganadas = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        grupos = [[jugador for jugador in self.jugadores if jugador.partidas_ganadas == x] for x in ganadas]
        sorted_puntaje = [sorted(grupo, key=lambda x: x.puntos) for grupo in grupos]
        partidas = [] # falta emparejar

        self.finalizar_partida(partidas)

        apuesta = randint(0, 1000)
        self.apuestas.append(apuesta)
        self.print_apuesta()

        return sorted_puntaje

    def print_apuesta(self):
        a = reduce(lambda x, y: x + y, self.apuestas)
        print("Apuesta acumulada:", a)

    def finalizar_partida(self, partidas):  # partidas es una lista de tuplas (jugador, oponente)
        ganadores = [choice(pareja) for pareja in partidas]
        perdedores = [jugador for jugador in self.jugadores if jugador not in ganadores]

        [ganador.ganar() for ganador in ganadores]
        [perdedor.perder() for perdedor in perdedores]

        return


def read(path):
    with open(path) as file:
        lineas = (row.strip() for row in file)
        next(lineas)
        jugadores = (jugador for jugador in read_line(lineas))
        return list(jugadores)

def read_line(gen):
    count = 1
    while True:
        string = next(gen)
        yield Jugador(string.split(","), count)
        count += 1

jugadores = read("jugadores.csv")

campeonato = Campeonato(jugadores)
print(campeonato.iniciar())
