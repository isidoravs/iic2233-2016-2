# estructura principal
import random
import math
from batallas import calculo_stats
from jsonReader import jsonToDict, dictToJson


class Programon:
    def __init__(self, ide, name, moves, tipo, level, stats, evolve_level, evolve_to):
        self.ide = ide
        self.unique_id = 0  # depende de cada jugador
        self.name = name
        self.moves = moves  # lista (al hacer set_moves contiene diccionarios con info base)
        self.tipo = tipo
        self.level = level
        self.hp = stats[0]  # stats es una lista
        self.special_defense = stats[1]
        self.special_attack = stats[2]
        self.defense = stats[3]
        self.speed = stats[4]
        self.attack = stats[5]
        self.evolve_level = evolve_level  # -1 si no evoluciona
        self.evolve_to = evolve_to  # -1 si no evoluciona
        self.iv = random.randint(0, 15)  # generados al instanciar
        self.ev = random.randint(0, 65535)
        self.batallas = []  # alamacena datos de las batallas, para mostrarlas
        self.set_moves()  # actualiza moves a sus pp y power base

    def set_unique_id(self):
        # de alguna manera decidir el id unico por jugador
        pass

    def set_moves(self):  # resetea a valores base
        base_moves = jsonToDict("datos/programonMoves.json")
        new_moves = []
        for movimiento in self.moves:
            for dicc in base_moves:
                if movimiento == dicc["name"]:
                    new_moves.append(dicc)
                    break
        self.moves = new_moves

    def evolucionar(self):
        # evlucion
        pass

    def resumen_batallas(self, nombre_programon):
        # muestra el resumen de batallas
        pass

    def actualizar_stats(self, base_programones):  # si se captura programon o aumenta de nivel
        # base_datos objeto de la clase PCBastian
        info_base = {}

        for dicc in base_programones:
            if dicc["id"] == self.ide:
                info_base = dicc
                break

        defense_base = info_base["defense"]
        attack_base = info_base["attack"]
        speed_base = info_base["speed"]
        special_defense_base = info_base["special_defense"]
        special_attack_base = info_base["special_attack"]
        hp_base = info_base["hp"]

        self.defense = calculo_stats(defense_base, self.iv, self.ev, self.nivel)
        self.attack = calculo_stats(attack_base, self.iv, self.ev, self.nivel)
        self.speed = calculo_stats(speed_base, self.iv, self.ev, self.nivel)
        self.special_defense = calculo_stats(special_defense_base, self.iv, self.ev, self.nivel)
        self.special_attack = calculo_stats(special_attack_base, self.iv, self.ev, self.nivel)
        self.hp = calculo_stats(hp_base, self.iv, self.ev, self.nivel) + self.nivel + 5

    def atacar(self, entrenador): # "jugador" o "trainer"
        if entrenador == "jugador":
            # antes sacar las opciones de pp = 0 RR
            print("\n".join("[{}]: {}".format(i + 1, self.moves[i]["name"]) for i in range(len(self.moves)))) # RR
            ataque_jugador = input("Ingresa el numero de movimiento para atacar: ")

            while True:
                ataque_jugador = input("Ingresa el numero de movimiento para atacar: ")
                if ataque_jugador.isdigit():
                    if int(ataque_jugador)-1 not in range(len(self.moves)):
                        print("Ingrese un numero de movimiento valido")
                    else:
                        break
                else:
                    print("Ingrese el numero del movimiento a usar")

            move_chosen = self.moves[ataque_jugador - 1]  # diccionario de la base

        if entrenador == "trainer":
            move_chosen = random.choices(self.moves)

        # probabilidad de acertar
        prob = int(move_chosen["accuracy"] * 100)
        azar = random.randint(1,100)
        if azar <= prob:
            # puntos de poder
            for movimiento in self.moves:
                if movimiento["name"] == move_chosen["name"]:
                    movimiento["pp"] -= 1
                    if movimiento["pp"] == 0:
                        self.moves.remove(movimiento)  # no se si funciona RR
                    type_move = movimiento["type"]
                    base_move = movimiento["power"]

            return [base_move, type_move]

        else:
            print(self.name,"no ha acertado el ataque")
            return None













