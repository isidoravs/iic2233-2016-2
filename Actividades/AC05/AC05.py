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
        self.promedio = 0

    def calcular_promedio(self, rondas):  # rondas se la da campeonato
        promedio = lambda rondas: self.puntos / rondas
        self.promedio = promedio
        return promedio

    def ganar(self):
        self.puntos += 6
        self.partidas_ganadas += 1
        return

    def perder(self):
        self.puntos += randint(0, 5)
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
        [self.rondas() for i in range(9)]
        self.definir_ganador()

    def promedio_grupo(self, grupo):
        todos = [jugador.calcular_promedio(self.cantidad_rondas) for jugador in grupo]
        total = sum(todos)
        return total / len(grupo)

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
        print("\nComienza la ronda {}".format(self.cantidad_rondas))
        ganadas = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        grupos = [[jugador for jugador in self.jugadores if jugador.partidas_ganadas == x] for x in ganadas]
        sorted_puntaje = [sorted(grupo, key=lambda x: x.puntos) for grupo in grupos if len(grupo) != 0]
        partidas = [self.emparejar(grupo) for grupo in sorted_puntaje]

        all_partidas = [self.finalizar_partida(partida) for partida in partidas]

        apuesta = randint(0, 1000)
        self.apuestas.append(apuesta)
        self.print_apuesta()
        return

    def emparejar(self, grupo):
        aux = list(enumerate(grupo))
        par = list(filter(lambda x: x[0] % 2 == 0, aux))
        impar = list(filter(lambda x: x[0] % 2 != 0, aux))
        jugadores_par = [tupla[1] for tupla in par]
        jugadores_impar = [tupla[1] for tupla in impar]
        partidas = list(zip(jugadores_par, jugadores_impar))
        return partidas

    def print_apuesta(self):
        a = reduce(lambda x, y: x + y, self.apuestas)
        print("Apuesta acumulada:", a)

    def finalizar_partida(self, partidas):  # partidas es una lista de tuplas (jugador, oponente)
        ganadores = [choice(pareja) for pareja in partidas]
        perdedores = [jugador for jugador in self.jugadores if jugador not in ganadores]

        [ganador.ganar() for ganador in ganadores]
        [perdedor.perder() for perdedor in perdedores]

        grupo = ganadores + perdedores
        # print(self.promedio_grupo(grupo))
        return

    def definir_ganador(self):
        print("")
        ganadas = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        grupos = [[jugador for jugador in self.jugadores if jugador.partidas_ganadas == x] for x in ganadas]
        grupos_clean = [grupo for grupo in grupos if len(grupo) != 0]
        ganador = grupos_clean[0]
        if len(ganador) > 1:
            print("No existe jugador")
        else:
            print("El ganador es", ganador[0].nombre)
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
