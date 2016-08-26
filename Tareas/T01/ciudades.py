# ciudades y sus entidades
from jsonReader import jsonToDict, dictToJson
from programones import Programon
from batallas import Batalla, Trainer
import random


class Ciudad:
    def __init__(self, name, ide, PC):
        self.name = name
        self.ide = ide
        self.PC = PC
        if self.ide != 0:  # Pallet Town
            self.trainers = []
            self.set_trainers()
            self.gimnasio = Gimnasio(self.name, self.ide, self.trainers)

    def set_trainers(self):
        dicc_leader = {}
        list_trainer = []
        base_gyms = jsonToDict("datos/gyms.json")
        for gym in base_gyms:
            if gym["city"] == self.name:
                dicc_leader = gym["leader"]
                list_trainer = gym["trainers"]

        leader_squad = []
        for programon in dicc_leader["programones"]:
            for base in self.PC.base_programones:
                if base["id"] == programon["id"]:
                    stats = [base["hp"], base["special_defense"], base["special_attack"],
                             base["defense"], base["speed"], base["attack"]]
                    evolve_level = -1
                    evolve_to = -1

                    if "evolveLevel" in base.keys():
                        evolve_level = base["evolveLevel"]

                    if "evolveTo" in base.keys():
                        evolve_to = base["evolveTo"]

                    leader_squad.append(Programon(programon["id"], base["name"], base["moves"], base["type"],
                                                  programon["level"], stats, evolve_level, evolve_to))

        # agrego al lider
        self.trainers.append(Trainer("leader", dicc_leader["name"], leader_squad))

        for dicc_trainer in list_trainer:
            trainer_squad = []
            for programon in dicc_trainer["programones"]:
                for base in self.PC.base_programones:
                    if base["id"] == programon["id"]:
                        stats = [base["hp"], base["special_defense"], base["special_attack"], base["defense"],
                                 base["speed"], base["attack"]]
                        evolve_level = -1
                        evolve_to = -1

                        if "evolveLevel" in base.keys():
                            evolve_level = base["evolveLevel"]

                        if "evolveTo" in base.keys():
                            evolve_to = base["evolveTo"]

                        trainer_squad.append(Programon(programon["id"], base["name"], base["moves"], base["type"],
                                                      programon["level"], stats, evolve_level, evolve_to))
            self.trainers.append(Trainer("trainer", dicc_trainer["name"], trainer_squad))
        return

    def menu_ciudad(self, jugador):
        print("""
    ~ Bienvenido ~
        1: Centro Programón
        2: Gimnasio
        3: Tienda de Prograbolas
        4: Volver al menu
            """)
        eleccion = input("Ingrese una opción:\n> ")
        while eleccion not in ["1", "2", "3", "4"]:
            print("{} no es una opcion valida".format(eleccion))
            eleccion = input("Ingrese una opcion:\n> ")
        if eleccion == "4":
            return
        else:
            self.opciones_ciudad(int(eleccion), jugador)


    def opciones_ciudad(self, eleccion, jugador):
        if eleccion == 1:
            print("""
    ~ Centro Programon ~
        1: PC de Bastian (administrar equipo programon)
        2: Volver a {}
                """.format(self.name))

            opcion = input(" > ")
            while opcion not in ["1", "2"]:
                opcion = input("Ingrese una opcion valida\n > ")

            if opcion == "1":
                self.PC.ingresar_sistema(jugador)
                return
            else:
                self.menu_ciudad(jugador)
                return

        elif eleccion == 2:
            self.gimnasio.entrar(jugador, self.PC)
            return

        elif eleccion == 3:
            print("""
    ~ Tienda de Prograbolas ~
        1: Comprar prograbolas (500 yenes c/u)
        2: Volver a {}
                """.format(self.name))

            opcion = input(" > ")
            while opcion not in ["1", "2"]:
                opcion = input("Ingrese una opcion valida\n > ")

            if opcion == "1":
                self.tienda(jugador)
                return
            else:
                self.menu_ciudad(jugador)
                return
        else:
            self.menu_ciudad(jugador)
            return

    def tienda(self, jugador):
        # caso en que no pueda comprar 1 prograbola
        if jugador.yenes < 500:
            print("Lo siento, no tienes suficientes yenes para comprar una prograbola")
            return

        cantidad_prograbolas = input("¿Cuantas prograbolas desea comprar?\n[ ENTER ] para volver a la ciudad\n >")
        if cantidad_prograbolas == "":
            return

        success = False
        while not success:
            if not cantidad_prograbolas.isdigit():
                cantidad_prograbolas = input("Ingrese una cantidad valida\n > ")
            else:
                cantidad_prograbolas = int(cantidad_prograbolas)
                if jugador.yenes < cantidad_prograbolas * 500:
                    print("No tienes suficientes yenes para esa cantidad de prograbolas")
                    cantidad_prograbolas = input("Ingrese una cantidad valida\n > ")
                else:
                    success = True
                    jugador.prograbolas += cantidad_prograbolas
                    jugador.yenes -= (cantidad_prograbolas * 500)
                    print("Total: {} yenes\n ----\nAhora tienes:\n {} prograbolas y "
                          "{} yenes".format(cantidad_prograbolas * 500, jugador.prograbolas, jugador.yenes))
        return


class Gimnasio:
    def __init__(self, city_name, city_id, trainers):  # unico para cada ciudad
        self.city_name = city_name
        self.city_id = city_id
        self.leader = trainers[0]  # trainers[0].trainer_type == "leader"
        self.trainers = trainers[1:]  # lista de objetos de la clase Trainer

    def entrar(self, jugador, PC):
        ciudades_batalla = jugador.batallas.keys()  # ciudades donde ha batallado
        if self.city_name not in ciudades_batalla:
            print("Bienvenido! Al parecer no te has enfrentado a ninguno de nuestros entrenadores:")
            nuevo_gimnasio = [[contrincante.name, 0] for contrincante in self.trainers]
            jugador.batallas[self.city_name] = nuevo_gimnasio
            beated_trainers = 0

        else:
            print("Bienvenido! Veo que no es la primera vez que pasas por aqui.")
            beated_trainers = 0
            display_beated = "Has ganado a:\n"
            for batalla in jugador.batallas[self.city_name]:
                if batalla[1] != 0:
                    beated_trainers += 1
                    display_beated += batalla[0]+"\n"

            if beated_trainers == 0:
                print("Todavia no has ganado a ningun entrenador, esta es tu oportunidad!")
            else:
                print(display_beated)

        if beated_trainers == len(jugador.batallas[self.city_name]):
            print("Felicitaciones! Le has ganado a todos los entrenadores, es tu turno de enfrentarte al lider.")
            print("\n ~ Batalla contra {} ~".format(self.leader.name))
            batalla = Batalla(self.city_name, jugador, self.leader, self.leader.programon_squad, PC, False)

        else:
            print(" ~ Trainers ~ ")
            display = "\n".join("[{}]: {}".format(i + 1, self.trainers[i].name) for i in range(len(self.trainers)))
            print(display)

            while True:
                contrincante = input("Escoge un entrenador para comenzar la batalla:\n >")
                if contrincante.isdigit():
                    if int(contrincante)-1 not in range(len(self.trainers)):
                        print("Ingrese un numero de entrenador valido")
                    else:
                        break
                else:
                    print("Ingrese el numero del entrenador a batallar")

            print("\n ~ Batalla contra {} ~".format(self.trainers[int(contrincante) - 1].name))
            batalla = Batalla(self.city_name, jugador, self.trainers[int(contrincante) - 1],
                              self.trainers[int(contrincante) - 1].programon_squad, PC, False)
        return


class Mapa:
    def __init__(self, jugador, ide, PC):
        self.jugador = jugador
        self.ide = ide  # int [0, 32]
        self.PC = PC
        self.routes = jsonToDict("datos/routes.json")

    def new_location(self, movimiento):  # 1 (avanzar) o -1 (retroceder)
        # no salir de la ciudad si no cumple los requisitos
        if (self.ide % 4 == 0) and (movimiento == 1) and (self.ide != 0):
            if self.jugador.location.name in self.jugador.batallas.keys():
                print("Como ya has batallado en el gimnasio, tienes permitido continuar tu "
                      "camino. ¡Mucha suerte, {}!\n".format(self.jugador.unique_name))
                self.jugador.location = None
            else:
                print("Para poder avanzar hacia la proxima ciudad debes haber batallado, al "
                      "menos, una vez en nuestro gimnasio")
                return

        self.ide += movimiento
        self.jugador.location_id += movimiento
        if self.ide < 0:
            print("¡No puedes retroceder! Este es recien el comienzo, sigue tu camino para "
                  "convertirte en un verdadero Maestro Programón")
            self.ide = 0
            self.jugador.location_id = 0
            return

        elif self.ide == 33:
            print("¡Cinnabar Island es la ultima ciudad! No puedes seguir avanzando, vuelve a "
                  "pelear en los gimnasios de las ciudades anteriores y buscar programones en las rutas.")
            self.ide = 32
            self.jugador.location_id = 32

        elif self.ide == 0:
            print("¡Bienvenido a Pallet Town!\n No hay mucho que hacer por acá, sigue tu "
                  "camino para convertirte en un verdadero Maestro Programón")
            return

        elif self.ide % 4 == 0:
            zip_code = self.ide // 4
            for route in self.routes:
                if route["route"] == zip_code:
                    city = Ciudad(route["destination"], zip_code, self.PC)
            self.jugador.location = city
            print("Has entrado a la ciudad {}".format(city.name))
            city.menu_ciudad(self.jugador)
            return

        else:
            self.jugador.location = None
            self.location_name = ""
            print("Te encuentras en la hierba...")

            azar = random.randint(1,100)
            if azar <= 35:
                programon_salvaje = self.generar_programon_salvaje()
                programon_salvaje.unique_id = len(self.PC.programones[self.jugador.unique_name])  # unique_name
                print("¡Ha aparecido un {} salvaje (nivel {})!".format(programon_salvaje.name,
                                                                                programon_salvaje.level))
                programon_salvaje.visto_capturado = self.ide
                programon_salvaje.unique_id = len(self.jugador.progradex.programones_vistos +
                                                  self.jugador.progradex.programones_capturados)
                print("\n ~ Comienza la batalla ~")
                batalla = Batalla(None, self.jugador, programon_salvaje, [programon_salvaje], self.PC, True)
            else:
                print("... no ocurre nada en especial, continua tu camino.")
            return

    def mostrar(self):
        display = "[ Pallet Town ]\n"
        display += "\n".join(" v\n v Route {}\n v\n[ {} ]".format(i, self.routes[i]["destination"])
                             for i in range(len(self.routes)))
        print(display)

        if self.jugador.location is None:
            print("Te encuentras en la ruta {}".format(self.jugador.location_id // 4 + 1))
        else:
            print("Te encuentras en la ciudad {}".format(self.jugador.location.name))
        return

    def generar_programon_salvaje(self):
        route_id = (self.ide // 4) + 1
        rango_nivel = [0, 0]
        for ruta in self.routes:
            if ruta["route"] == route_id:
                rango_nivel = ruta["levels"]

        level_salvaje = random.randint(rango_nivel[0], rango_nivel[1])
        info_salvaje = random.choice(self.PC.base_programones)

        while True:
            if "evolveLevel" in info_salvaje.keys():  # programon que evoluciona, limite superior
                if info_salvaje["evolveLevel"] <= level_salvaje:
                    # deberia estar evolucionado
                    info_salvaje = random.choice(self.PC.base_programones)
                else:
                    break  # cumple restriccion
            else:  # programon que no evoluciona, no tiene limite superior pero si inferior
                version_unica = True
                for programon in self.PC.base_programones:
                    if "evolveLevel" in programon.keys():
                        if programon["evolveTo"] == info_salvaje["id"]:  # programon seria subevolucion
                            version_unica = False
                            if programon["evolveLevel"] >= level_salvaje:
                                # deberia ser la subevolucion
                                info_salvaje = random.choice(self.PC.base_programones)
                            else:
                                break  # cumple restriccion
                if version_unica:  # no tiene evolucion ni subevolucion
                    break

        stats_salvaje = [info_salvaje["hp"], info_salvaje["special_defense"], info_salvaje["special_attack"],
                         info_salvaje["defense"], info_salvaje["speed"], info_salvaje["attack"]]

        evolve_level = -1
        evolve_to = -1

        if "evolveLevel" in info_salvaje.keys():
            evolve_level = info_salvaje["evolveLevel"]

        if "evolveTo" in info_salvaje.keys():
            evolve_to = info_salvaje["evolveTo"]

        salvaje = Programon(info_salvaje["id"], info_salvaje["name"], info_salvaje["moves"], info_salvaje["type"],
                            level_salvaje, stats_salvaje, evolve_level, evolve_to)

        return salvaje

if __name__ == "__main__":
    print("Module being run directly")
