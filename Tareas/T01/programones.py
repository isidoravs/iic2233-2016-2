# estructura principal
import random
import math
from batallas import calculo_stats
from jsonReader import jsonToDict, dictToJson


class Programon:
    def __init__(self, ide, name, moves, tipo, level, stats, evolve_level=-1, evolve_to=-1):
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
        self.batallas = []  # lista de listas, [contrincante, resultado]
        self.original_hp = self.hp
        self.visto_capturado = 0
        self.set_moves()  # actualiza moves a sus pp y power base

    def set_moves(self):  # resetea a valores base
        base_moves = jsonToDict("datos/programonMoves.json")
        new_moves = []
        for movimiento in self.moves:
            for dicc in base_moves:
                if movimiento == dicc["name"]:
                    new_moves.append(dicc)
                    break
        self.moves = new_moves

    def evolucionar(self, PC):
        subevolucion = None
        for evolucion in PC.base_programones:
            if evolucion["id"] == self.evolve_to:
                # guardar informacion subevolucion
                sub_stats = [self.hp, self.special_defense, self.special_attack, self.defense, self.speed, self.attack]

                subevolucion = Programon(self.ide, self.name, self.moves, self.tipo, self.level, sub_stats,
                                         self.evolve_level, self.evolve_to)
                subevolucion.moves = self.moves
                subevolucion.unique_id = -1

                # evolucion, mismo unique_id con distintas caracteristicas
                self.ide = evolucion["id"]
                self.tipo = evolucion["type"]
                self.hp = evolucion["hp"]
                self.name = evolucion["name"]
                self.special_defense = evolucion["special_defense"]
                self.special_attack = evolucion["special_attack"]
                self.defense = evolucion["defense"]
                self.speed = evolucion["speed"]
                self.attack = evolucion["attack"]
                self.moves = evolucion["moves"]
                self.set_moves()
                if "evolveLevel" in evolucion.keys():
                    self.evolve_level = evolucion["evolveLevel"]
                    self.evolve_to = evolucion["evolveTo"]
                else:
                    self.evolve_level = -1
                    self.evolve_to = -1
        print(">>> {} evoluciona a {} <<<\nSe ha actualizado la informacion en tu Progradex y en "
              "el PC".format(subevolucion.name, self.name))
        return subevolucion

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

        self.defense = calculo_stats(defense_base, self.iv, self.ev, self.level)
        self.attack = calculo_stats(attack_base, self.iv, self.ev, self.level)
        self.speed = calculo_stats(speed_base, self.iv, self.ev, self.level)
        self.special_defense = calculo_stats(special_defense_base, self.iv, self.ev, self.level)
        self.special_attack = calculo_stats(special_attack_base, self.iv, self.ev, self.level)
        self.hp = calculo_stats(hp_base, self.iv, self.ev, self.level) + self.level + 5

    def atacar(self, entrenador):  # "jugador" o "trainer"
        if entrenador == "jugador":
            print("\n Movimientos de {} (hp = {})".format(self.name, self.hp))
            print("\n".join("[{}]: {} (pp = {})".format(i + 1, self.moves[i]["name"], self.moves[i]["pp"])
                            for i in range(len(self.moves))))

            while True:
                ataque_jugador = input("Ingresa el numero de movimiento para atacar:\n> ")
                if ataque_jugador.isdigit():
                    if int(ataque_jugador) - 1 not in range(len(self.moves)):
                        print("Ingrese un numero de movimiento valido")
                    else:
                        break
                else:
                    print("Ingrese el numero del movimiento a usar")

            move_chosen = self.moves[int(ataque_jugador) - 1]

        if entrenador == "trainer":
            move_chosen = random.choice(self.moves)

        print("{} ataca con {}".format(self.name, move_chosen["name"]))

        # probabilidad de acertar
        prob = int(move_chosen["accuracy"] * 100)
        azar = random.randint(1, 100)
        if azar <= prob:
            # puntos de poder
            for movimiento in self.moves:
                if movimiento["name"] == move_chosen["name"]:
                    movimiento["pp"] -= 1
                    if movimiento["pp"] == 0:
                        self.moves.remove(movimiento)
                    type_move = movimiento["type"]
                    base_move = movimiento["power"]

            return [base_move, type_move]

        else:
            print(self.name, "no ha acertado el ataque")
            return None

    def __str__(self):
        rutas = jsonToDict("datos/routes.json")
        ide = self.visto_capturado
        location = ""
        if ide % 4 == 0:
            for ruta in rutas:
                if (ide // 4) == ruta["route"]:
                    location = ruta["destination"]
        else:
            location = "hierba, ruta {}".format(ide // 4 + 1)
        display = "\n~ {} (nivel: {})~\n ID: {} | Tipo: {}\n Ultima vez visto: {}" \
                  "\n".format(self.name, self.level, self.ide, self.tipo, location)
        stats = "* Stats *\n HP: {}\n Speed: {}\n Attack: {} | Special attack: {}\n Defense: {} | Special defense: " \
                "{}\n".format(self.hp, self.speed, self.attack, self.special_attack, self.defense, self.special_defense)
        display += stats
        base = jsonToDict("datos/programones.json")
        for programon in base:
            if programon["id"] == self.ide:
                if "evolveTo" in programon.keys():
                    for evolucion in base:
                        if programon["evolveTo"] == evolucion["id"]:
                            display += " Evolve to: {} (in level {})".format(evolucion["name"],
                                                                             programon["evolveLevel"])
                else:
                    break
        return display

if __name__ == "__main__":
    print("Module being run directly")
