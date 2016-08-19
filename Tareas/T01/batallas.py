# clases y funciones necesarias para las batallas
import math
import random
from jsonReader import jsonToDict, dictToJson


class Trainer:  # leader es un tipo de trainer (mismos atributos)
    def __init__(self, trainer_type, name, programon_squad):
        self.trainer_type = trainer_type  # "leader" o "trainer"
        self.name = name
        self.programon_squad = programon_squad
        self.programon_original_hp = [programon.hp for programon in self.programon_squad]
        self.programon_original_moves = [programon.moves for programon in self.programon_squad]


class ProgramonMoves:  # o ataques
    def __init__(self, power_points, accuracy, move_type, base_power, name):
        self.name = name
        self.power_points = power_points
        self.accuracy = accuracy
        self.move_type = move_type
        self.power = base_power


class Batalla:
    def __init__(self, city_name, jugador, oponente, equipo_jugador, equipo_oponente, salvaje):  # salvaje es True o False
        self.city_name = city_name
        self.jugador = jugador
        self.oponente = oponente
        self.equipo_jugador = equipo_jugador
        self.equipo_oponente = equipo_oponente
        self.capturable = salvaje
        self.elegidos_jugador = []
        self.disponibles_jugador = list(self.equipo_jugador)
        self.elegidos_oponente = []
        self.disponibles_oponente = list(self.equipo_oponente)
        self.pelear(self.equipo_jugador[0], self.equipo_oponente[0], False)  # siempre comienza con el primero del equipo
        # revisar como implementar bien esta forma de capturable (tal vez mejor afuera en el menu)
        # if batalla.capturable: o algo asi RR

    def pelear(self, programon_jugador, programon_oponente, final_batalla, ganador=None):
        # caso base
        if final_batalla:
            print("~ Final de la batalla ~")
            if ganador == "jugador":
                # programones suben de nivel
                base_programones = jsonToDict("datos/programones.json")
                for programon in self.elegidos_jugador:
                    if programon.hp > 0:
                        programon.level += 1
                        if programon.level == programon.evolve_level:
                            programon.evolucionar()

                        # RESTORE PP Y HP RR

                        # calculo de nuevos stats
                        programon.actualizar_stats(base_programones)

                # jugador gana 200 yenes
                self.jugador.yenes += 200

                # medalla si es contra lider
                if self.trainer.trainer_type == "leader":
                    print("Felicitaciones! Derrotaste al lider del gimnasio, toma una medalla en reconocimiento.")

                    first_time = True
                    for medal in self.jugador.medals:
                        if medal[0] == self.city_name:
                            first_time = False
                            medal[1] += 1

                    if first_time:
                        self.jugador.medals.append([self.city_name, 1])

            if ganador == "oponente":
                print("Has perdido la batalla, pierdes 100 yenes.")
                self.jugador.yenes -= 100

            # restore pp y hp de cada programon : ENTRENADOR
            for i in range(len(self.equipo_oponente)):
                self.equipo_oponente[i].hp = self.oponente.programon_original_hp[i]
                self.equipo_oponente[i].moves = self.oponente.programon_original_moves[i]

            return

        # llamada recursiva (no se si funcione) RR (sino usar ciclos)
        self.elegidos_jugador.append(programon_jugador)
        self.elegidos_oponente.append(programon_oponente)
        final_pelea = None
        while final_pelea is None:
            final_pelea = self.turno_pelea(programon_jugador, programon_oponente)  # retorna perdedor o None

        if final_pelea == "jugador":
            programon_proximo = self.proximo_a_pelear(programon_jugador, final_pelea, False)  # cambiar si puede
            if programon_proximo is not None:
                self.pelear(programon_proximo, programon_oponente, False)  # recursivo (o hacer return?) RR
            else:
                self.pelear(programon_jugador, programon_oponente, True, "oponente")  # llega al caso base

        if final_pelea == "oponente":
            programon_proximo = self.proximo_a_pelear(programon_oponente, final_pelea, False)
            if programon_proximo is not None:
                self.pelear(programon_proximo, programon_oponente, False)
            else:
                self.pelear(programon_jugador, programon_oponente, True, "ganador")


    def turno_pelea(self, programon_jugador, programon_oponente):  # falta prints que digan lo que pasa RR
        if programon_jugador.speed >= programon_oponente.speed:
            result = programon_jugador.atacar("jugador")  # parametro es el entrenador del programon
            atacante_gano = resultado_ataque(result, programon_jugador, programon_oponente)
            if atacante_gano:
                return "oponente"
            else:
                print("Es el turno de {}".format(programon_oponente.name))  # programon_oponente no perdio

            result = programon_oponente.atacar("trainer")
            atacante_gano = resultado_ataque(result, programon_oponente, programon_jugador)
            if atacante_gano:
                return "jugador"
            else:
                print("Es el turno de {}".format(programon_jugador.name))

            return None

        else:
            result = programon_oponente.atacar("trainer")
            atacante_gano = resultado_ataque(result, programon_oponente, programon_jugador)
            if atacante_gano:
                return "jugador"
            else:
                print("Es el turno de {}".format(programon_jugador.name))  # programon_jugador no perdio

            result = programon_jugador.atacar("jugador")  # parametro es el entrenador del programon
            atacante_gano = resultado_ataque(result, programon_jugador, programon_oponente)
            if atacante_gano:
                return "oponente"
            else:
                print("Es el turno de {}".format(programon_oponente.name))

            return None


    def proximo_a_pelear(self, programon_actual, entrenador, solo_cambio):  # solo_cambio = True si no ha perdido aun
        if solo_cambio:
            pass  # implementar opcion de cambiar por gusto RR
        else:
            if entrenador == "jugador":
                self.disponibles_jugador.remove(programon_actual)
                if len(self.disponibles_jugador) == 0:
                    print("Has perdido! Tus programones no estan en condiciones para pelear")
                    return None
                print("{} no se encuentra en codiciones para pelear\n Tu equipo:".format(programon_actual.name))
                display = "\n".join("[{}]: {}".format(i + 1, self.disponibles_jugador[i].name) for i in
                                    range(len(self.disponibles_jugador)))
                print(display)
                opcion = input("Escoge un programon para la siguiente pelea: ")
                while True:
                    opcion = input("Escoge un programon para la siguiente pelea: ")
                    if opcion.isdigit():
                        if int(opcion) - 1 not in range(len(self.disponibles_jugador)):
                            print("Ingresa un numero de programon valido")
                        else:
                            break  # RR
                    else:
                        print("Ingrese el numero del programon a pelear")

                return self.disponibles_jugador[opcion - 1]

            if entrenador == "oponente":
                self.disponibles_oponente.remove(programon_actual)
                if len(self.disponibles_oponente) == 0:
                    print("Felicidades! Le has ganado al entrenador, sus programones no "
                          "estan en condiciones para pelear")
                    return None
                return self.disponibles_oponente[0]



def calculo_stats(base, iv, ev, nivel):
    new_stat = math.floor((((base + iv) * 2 + math.floor(math.floor(math.sqrt(ev)) / 4)) * nivel) / 100) + 5
    return new_stat


def resultado_ataque(result, programon_ataca, programon_defiende):
    harm = 0
    if result is not None:
        harm = calculo_harm(programon_ataca, programon_defiende, result[0], result[1])
    programon_defiende.hp -= harm

    atacante_gano = False
    if programon_defiende.hp <= 0:
        print("{} ha perdido!".format(programon_defiende.name))
        atacante_gano = True

    if len(programon_oponente.moves) == 0:
        print("{} se ha quedado sin movimientos!".format(programon_defiende.name))
        atacante_gano = True

    return atacante_gano


def calculo_harm(programon_ataca, programon_defiende, base_move, type_move):
    category = dictToJson("datos/moveCategories.json")
    bonus_tipo = dictToJson("datos/types.json")

    if type_move in category["physical_moves"]:  # lista con los ataques normales
        harm1 = ((2 * programon_ataca.nivel + 10) / 250) * (programon_ataca.attack /
                                                            programon_defiende.defensa) * base_move + 2

    if type_move in category["special_moves"]:
        harm1 = ((2 * programon_ataca.nivel + 10) / 250) * (programon_ataca.special_attack /
                                                            programon_defiende.special_defense) * base_move + 2
    # STAB
    if type_move == programon_ataca.tipo:
        stab = 1.5
    else:
        stab = 1

    # tipo
    valor_tipo = 1  # en caso de no existir la combinacion
    combinacion = bonus_tipo[type_move]  # estan todos? RR
    if programon_defiende.tipo in combinacion.keys():
        valor_tipo = combinacion[programon_defiende.tipo]

    # critico
    base_programones = jsonToDict("datos/programones.json")
    info_base = {}
    for dicc in base_programones:
        if dicc["id"] == programon_ataca.ide:
            info_base = dicc
            break
    speed_base = info_base["speed"]

    T = speed_base / 2
    P = random.randint(0, 256)
    critico = 1
    if P <= T:
        critico = 2

    # random
    aleatorio = random.uniform(0.85, 1)

    modificador = stab * valor_tipo * critico * aleatorio
    harm = harm1 * modificador

    return math.floor(harm)






