# clases y funciones necesarias para las batallas
import math
import random
from jsonReader import jsonToDict, dictToJson


class Trainer:  # leader es un tipo de trainer (mismos atributos)
    def __init__(self, trainer_type, name, programon_squad):
        self.trainer_type = trainer_type  # "leader" o "trainer"
        self.name = name
        self.programon_squad = programon_squad


class Batalla:
    def __init__(self, city_name, jugador, oponente, equipo_oponente, PC, salvaje):  # salvaje: True o False
        self.city_name = city_name
        self.jugador = jugador
        self.oponente = oponente
        self.equipo_jugador = jugador.equipo
        self.equipo_oponente = equipo_oponente
        self.capturable = salvaje
        self.PC = PC
        primer_programon = self.primer_programon()
        self.elegidos_jugador = [primer_programon]
        self.disponibles_jugador = list(self.equipo_jugador)
        self.elegidos_oponente = [self.equipo_oponente[0]]
        self.disponibles_oponente = list(self.equipo_oponente)
        self.equipo_oponente[0].visto_capturado = self.jugador.location_id
        self.jugador.progradex.programones_vistos.append(self.equipo_oponente[0])
        self.pelear(primer_programon, self.equipo_oponente[0], False)

    def primer_programon(self):
        print("> Equipo de {} <".format(self.jugador.unique_name))
        for i in range(len(self.equipo_jugador)):
            print("[{}] {} (nivel = {} | hp = {})".format(i + 1, self.equipo_jugador[i].name,
                                                          self.equipo_jugador[i].level, self.equipo_jugador[i].hp))

        while True:
            opcion = input("Escoge tu programon para pelear:\n >")
            if opcion.isdigit():
                if int(opcion) not in range(1, len(self.equipo_jugador) + 1):
                    print("Ingresa una opcion valida")
                else:
                    break
            else:
                print("Ingresa el numero del programon a pelear")

        primer_programon = self.equipo_jugador[int(opcion) - 1]

        print("{} esta listo para la batalla!".format(primer_programon.name))
        return primer_programon

    def pelear(self, programon_jugador, programon_oponente, final_batalla, ganador=None):
        # caso base
        if final_batalla:
            self.terminar_batalla(ganador, programon_jugador)
            return

        # llamada recursiva
        if programon_jugador not in self.elegidos_jugador:
            programon_jugador.original_hp = programon_jugador.hp
            self.elegidos_jugador.append(programon_jugador)

        if programon_oponente not in self.elegidos_oponente:
            programon_oponente.original_hp = programon_oponente.hp
            self.elegidos_oponente.append(programon_oponente)

        final_pelea = None
        while final_pelea is None:
            # retorna perdedor, pierde_turno, cobarde, capturado o None
            final_pelea = self.turno_pelea(programon_jugador, programon_oponente)

        if final_pelea == "capturado":
            self.pelear(programon_jugador, programon_oponente, True, "jugador")

        elif final_pelea == "pierde_turno":
            programon_proximo = self.proximo_a_pelear(programon_jugador, "jugador", True)
            if programon_proximo is not None:
                print("Has escogido a {} como tu proximo programon para pelear".format(programon_proximo.name))
            self.pelear(programon_proximo, programon_oponente, False)

        elif final_pelea == "cobarde":
            self.pelear(programon_jugador, programon_oponente, True, "oponente")

        elif final_pelea == "jugador":
            programon_proximo = self.proximo_a_pelear(programon_jugador, final_pelea, False)  # cambiar si puede
            if programon_proximo is not None:
                print("Has escogido a {} como tu proximo programon para pelear".format(programon_proximo.name))
                self.pelear(programon_proximo, programon_oponente, False)  # recursivo
            else:
                self.pelear(programon_jugador, programon_oponente, True, "oponente")  # llega al caso base

        elif final_pelea == "oponente":
            if self.capturable:
                print("¡Has derrotado al programon salvaje!\n... pero como no lo has capturado "
                      "con una prograbola, escapa")
            else:  # oponente es un trainer
                programon_proximo = self.proximo_a_pelear(programon_oponente, final_pelea, False)
                if programon_proximo is not None:
                    print("{} ha escogido a {} como su proximo programon para pelear".format(self.oponente.name,
                                                                                             programon_proximo.name))
                    programon_proximo.visto_capturado = self.jugador.location_id
                    self.jugador.progradex.programones_vistos.append(programon_proximo)
                    self.pelear(programon_jugador, programon_proximo, False)
                else:
                    self.pelear(programon_jugador, programon_oponente, True, "jugador")

    def menu_batalla(self, programon_jugador, programon_oponente):
        ubicacion = self.city_name
        if self.city_name is None:
            ubicacion = "la hierba"
        print("""
    ~ Menu Batalla ~
        1: ¡Pelear!
        2: Cambiar programon
        3: Volver a {}""".format(ubicacion))

        if self.capturable:
            print("        4: Lanzar una prograbola a {}".format(programon_oponente.name))
        eleccion = input("\nIngrese una opcion:\n >")
        while eleccion not in ["1", "2", "3"]:
            if eleccion == "4" and self.capturable:  # unico caso que se permite otra opcion
                break
            print("{0} no es una opcion valida".format(eleccion))
            eleccion = input("Ingrese una opcion:\n >")

        if eleccion == "1":
            return "pelea"
        elif eleccion == "2":
            if len(self.disponibles_jugador) == 1:
                print("{} es tu unico programon en condiciones para pelear! "
                      "No puedes hacer cambio.".format(programon_jugador.name))
                self.menu_batalla(programon_jugador, programon_oponente)
                return
            else:
                return "cambio"
        elif eleccion == "3":
            print("¡Te has retirado!")
            return "cobarde"
        elif eleccion == "4":
            if self.jugador.prograbolas == 0:
                print("No tienes prograbolas para capturar a este programon")
                return
            capturado = self.atrapar_programon_salvaje(programon_oponente)  # capturado es True o False
            if capturado:
                return "capturado"
            else:
                print("Continua la batalla...")
                return "no capturado"

    def turno_pelea(self, programon_jugador, programon_oponente):
        if programon_jugador.speed >= programon_oponente.speed:
            opcion_menu = self.menu_batalla(programon_jugador, programon_oponente)
            if opcion_menu == "cambio":
                return "pierde_turno"
            elif opcion_menu == "cobarde":
                return "cobarde"
            elif opcion_menu == "capturado":
                return "capturado"
            else:
                if programon_jugador.hp == programon_jugador.original_hp and \
                                programon_oponente.hp == programon_oponente.original_hp:
                    print("{} ({}) es mas rapido y comienza el turno!".format(programon_jugador.name,
                                                                              self.jugador.unique_name))
                result = programon_jugador.atacar("jugador")  # parametro es el entrenador del programon
                atacante_gano = resultado_ataque(result, programon_jugador, programon_oponente, self.PC)
                if atacante_gano:
                    return "oponente"
                else:
                    print("\nEs el turno de {} (hp = {} | nivel = {})".format(programon_oponente.name,
                                                                              programon_oponente.hp,
                                                                              programon_oponente.level))

                result = programon_oponente.atacar("trainer")
                atacante_gano = resultado_ataque(result, programon_oponente, programon_jugador, self.PC)
                if atacante_gano:
                    return "jugador"
                else:
                    print("\nEs el turno de {} (hp = {} | nivel = {})".format(programon_jugador.name,
                                                                              programon_jugador.hp,
                                                                              programon_jugador.level))

                return

        else:
            if programon_jugador.hp == programon_jugador.original_hp and \
                            programon_oponente.hp == programon_oponente.original_hp:
                if self.capturable:
                    print("{} es mas rapido y comienza el turno!".format(programon_oponente.name))
                else:
                    print("{} ({}) es mas rapido y comienza el turno!".format(programon_oponente.name,
                                                                              self.oponente.name))
            result = programon_oponente.atacar("trainer")
            atacante_gano = resultado_ataque(result, programon_oponente, programon_jugador, self.PC)
            if atacante_gano:
                return "jugador"
            else:
                print("\nEs el turno de {} (hp = {} | nivel = {})".format(programon_jugador.name,
                                                                          programon_jugador.hp,
                                                                          programon_jugador.level))

            opcion_menu = self.menu_batalla(programon_jugador, programon_oponente)
            if opcion_menu == "cambio":
                return "pierde_turno"

            elif opcion_menu == "cobarde":
                return "cobarde"

            elif opcion_menu == "capturado":
                return "capturado"

            else:
                result = programon_jugador.atacar("jugador")  # parametro es el entrenador del programon
                atacante_gano = resultado_ataque(result, programon_jugador, programon_oponente, self.PC)
                if atacante_gano:
                    return "oponente"
                else:
                    print("\nEs el turno de {} (hp = {} | nivel = {})".format(programon_oponente.name,
                                                                              programon_oponente.hp,
                                                                              programon_oponente.level))

                return

    def proximo_a_pelear(self, programon_actual, entrenador, solo_cambio):
        if entrenador == "jugador":
            if not solo_cambio:  # solo_cambio = True si no ha perdido aun
                programon_actual.batallas.append([self.oponente.name, "perdedor"])
                self.disponibles_jugador.remove(programon_actual)
                print("{} no se encuentra en codiciones para pelear".format(programon_actual.name))
            else:
                programon_actual.batallas.append([self.oponente.name, "intercambio"])

            if len(self.disponibles_jugador) == 0:
                print("Ninguno de tus programones estan en condiciones para pelear")
                return None

            print("Tu equipo:".format(programon_actual.name))
            display = "\n".join("[{}]: {} (nivel = {} | hp = {})"
                                "".format(i + 1, self.disponibles_jugador[i].name, self.disponibles_jugador[i].level,
                                          self.disponibles_jugador[i].hp) for i in range(len(self.disponibles_jugador)))
            print(display)
            while True:
                opcion = input("Escoge un programon para el siguiente turno: ")
                if opcion.isdigit():
                    if int(opcion) - 1 not in range(len(self.disponibles_jugador)):
                        print("Ingresa un numero de programon valido")
                    else:
                        break
                else:
                    print("Ingrese el numero del programon a pelear")

            return self.disponibles_jugador[int(opcion) - 1]

        if entrenador == "oponente":
            self.disponibles_oponente.remove(programon_actual)
            if len(self.disponibles_oponente) == 0:
                print("Felicidades! Le has ganado al entrenador, sus programones no "
                      "estan en condiciones para pelear")
                for trainer in self.jugador.batallas[self.city_name]:
                    if trainer[0] == self.oponente.name:
                        trainer[1] += 1
                        break
                return None
            return self.disponibles_oponente[0]

    def terminar_batalla(self, ganador, programon_jugador):
        print("\n~ Final de la batalla ~")
        base_moves = jsonToDict("datos/programonMoves.json")

        if ganador == "jugador":
            programon_jugador.batallas.append([self.oponente.name, "ganador"])
            if self.capturable:
                print("Te encuentras nuevamente en la hierba")

            # programones suben de nivel
            for programon in self.elegidos_jugador:
                # restore move pp
                for programon_move in programon.moves:
                    for original_move in base_moves:
                        if programon_move["name"] == original_move["name"]:
                            programon_move["pp"] = original_move["pp"]

                # subir nivel, restore hp, actualizar stats
                if programon.hp > 0:
                    programon.level += 1
                    programon.hp = programon.original_hp
                    if programon.level == programon.evolve_level:
                        subevolucion = programon.evolucionar(self.PC)
                        # agregar a Progradex
                        self.jugador.progradex.programones_capturados.append(subevolucion)
                    else:
                        programon.actualizar_stats(self.PC.base_programones)  # evolucionar() tb actualiza stats

                else:
                    programon.hp = programon.original_hp
            # jugador gana 200 yenes
            if not self.capturable:
                print("Has ganado 200 yenes")
                self.jugador.yenes += 200
            # medalla si es contra lider
            if not self.capturable and self.oponente.trainer_type == "leader":
                print("Felicitaciones! Derrotaste al lider del gimnasio, toma una medalla en reconocimiento.")

                self.jugador.medals.append(self.city_name)

        if ganador == "oponente":
            if not self.capturable:
                print("Has perdido la batalla, pierdes 100 yenes.")
                self.jugador.yenes -= 100
            else:
                print("Te encuentras nuevamente en la hierba")

        if not self.capturable:
            # restore pp y hp de cada programon : ENTRENADOR
            for programon in self.elegidos_oponente:
                programon.hp = programon.original_hp
                for programon_move in programon.moves:
                    for original_move in base_moves:
                        if programon_move["name"] == original_move["name"]:
                            programon_move["pp"] = original_move["pp"]

        # restore pp y hp de cada programon : JUGADOR
        for programon in self.elegidos_jugador:
            if ganador != "jugador":
                programon.hp = programon.original_hp
            for programon_move in programon.moves:
                for original_move in base_moves:
                    if programon_move["name"] == original_move["name"]:
                        programon_move["pp"] = original_move["pp"]

        return

    def atrapar_programon_salvaje(self, programon_salvaje):
        print("Lanzas una prograbola a {}".format(programon_salvaje.name))
        self.jugador.prograbolas -= 1
        probabilidad = 0.2 + ((programon_salvaje.original_hp - programon_salvaje.hp)
                              * 0.8) / programon_salvaje.original_hp

        azar = random.randint(1, 100)
        if azar <= (probabilidad * 100):
            print("¡Ya esta!\n{} atrapado".format(programon_salvaje.name))
            # programon salvaje estaba en vistos > capturados
            self.jugador.progradex.programones_vistos.remove(programon_salvaje)
            self.jugador.progradex.programones_capturados.append(programon_salvaje)
            if len(self.jugador.equipo) < 6:  # en caso de que tenga 6
                self.jugador.equipo.append(programon_salvaje)
            self.PC.programones[self.jugador.unique_name].append(programon_salvaje)
            print("Se ha actualizando tu informacion en la Progradex")
            return True
        else:
            print("¡{} se ha escapado!\nTu prograbola no ha podido capturarlo".format(programon_salvaje.name))
            return False


def calculo_stats(base, iv, ev, nivel):
    new_stat = math.floor((((base + iv) * 2 + math.floor(math.ceil(math.sqrt(ev)) / 4)) * nivel) / 100) + 5
    return new_stat


def resultado_ataque(result, programon_ataca, programon_defiende, PC):
    harm = 0
    if result is not None:
        harm = calculo_harm(programon_ataca, programon_defiende, result[0], result[1], PC)
    programon_defiende.hp -= harm
    print("{} ha hecho {} daño a {}".format(programon_ataca.name, harm, programon_defiende.name))

    atacante_gano = False
    if programon_defiende.hp <= 0:
        print("{} ha perdido!".format(programon_defiende.name))
        atacante_gano = True

    if len(programon_defiende.moves) == 0:
        print("{} se ha quedado sin movimientos!".format(programon_defiende.name))
        atacante_gano = True

    return atacante_gano


def calculo_harm(programon_ataca, programon_defiende, base_move, type_move, PC):
    category = jsonToDict("datos/moveCategories.json")
    bonus_tipo = jsonToDict("datos/types.json")

    if type_move in category["physical_moves"]:  # lista con los ataques normales
        harm1 = ((2 * programon_ataca.level + 10) / 250) * (programon_ataca.attack /
                                                            programon_defiende.defense) * base_move + 2

    if type_move in category["special_moves"]:
        harm1 = ((2 * programon_ataca.level + 10) / 250) * (programon_ataca.special_attack /
                                                            programon_defiende.special_defense) * base_move + 2
    # STAB
    if type_move == programon_ataca.tipo:
        stab = 1.5
    else:
        stab = 1

    # tipo
    valor_tipo = 1  # en caso de no existir la combinacion
    combinacion = bonus_tipo[type_move]
    if programon_defiende.tipo in combinacion.keys():
        valor_tipo = combinacion[programon_defiende.tipo]

    # critico
    info_base = {}
    for dicc in PC.base_programones:
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


if __name__ == "__main__":
    print("Module being run directly")
