# sistema principal
import sys
from jsonReader import jsonToDict, dictToJson
from programones import Programon
from jugador import Jugador, Progradex
from ciudades import Ciudad, Mapa


class ProgramonRojo:
    def __init__(self):
        self.jugadores = []  # base de datos
        self.player = None

    def cargar_datos(self, PC):
        data = jsonToDict("datos/infoJugadores.json")
        rutas = jsonToDict("datos/routes.json")
        ide_jugadores = data.keys()

        for ide in ide_jugadores:
            jug = data[ide]
            old_player = Jugador(int(ide), jug["unique_name"], jug["password"], None, PC)
            old_player.yenes = jug["yenes"]
            old_player.medals = jug["medals"]
            old_player.prograbolas = jug["prograbolas"]
            old_player.location_id = jug["location_id"]
            old_player.batallas = jug["batallas"]
            if old_player.location_id % 4 != 0:
                old_player.location = None
            elif old_player.location_id == 0:  # viene predeterminado
                pass
            else:
                for ruta in rutas:
                    zip_code = old_player.location_id // 4
                    if ruta["route"] == zip_code:
                        old_player.location = Ciudad(ruta["destination"], zip_code, PC)

            PC.programones[old_player.unique_name] = []
            self.jugadores.append(old_player)

            for pro in jug["programones_PC"]:
                stats = [pro["hp"], pro["special_defense"], pro["special_attack"], pro["defense"], pro["speed"],
                         pro["attack"]]
                old_programon = Programon(pro["ide"], pro["name"], pro["moves"], pro["tipo"], pro["level"], stats,
                                          pro["evolve_level"], pro["evolve_to"])
                old_programon.iv = pro["iv"]
                old_programon.ev = pro["ev"]
                old_programon.unique_id = pro["unique_id"]
                old_programon.batallas = pro["batallas"]
                old_programon.visto_capturado = pro["visto_capturado"]
                PC.programones[old_player.unique_name].append(old_programon)  # agrega a PC
                old_player.progradex.programones_capturados.append(old_programon)  # agrega a Progradex

                if old_programon.unique_id in jug["equipo"]:
                    old_player.equipo.append(old_programon)  # agrega a equipo

            for pro in jug["programones_vistos"]:
                # el resto de los parametros no son necesarios
                old_visto = Programon(pro["ide"], pro["name"], pro["moves"], pro["tipo"], 0, [0,0,0,0,0,0])
                old_visto.visto_capturado = pro["visto_capturado"]
                old_player.progradex.programones_vistos.append(old_visto)

    def log_in(self):
        success = False
        while not success:
            user = input("Usuario: ")
            password = input("Contraseña: ")
            for jugador in self.jugadores:
                if jugador.unique_name == user and jugador.password == password:
                    print("Log in exitoso...")
                    actual_player = jugador
                    success = True
                    break
            if not success:
                print("Los datos ingresados no son validos")

        self.player = actual_player
        return

    def sign_up(self, PC):
        while True:
            count = 0
            new_name = input("Ingrese un nombre de usuario: ")
            for jugador in self.jugadores:
                count += 1
                if jugador.unique_name == new_name:
                    print("Nombre de usuario no disponible")
            if count == len(self.jugadores):
                break


        new_password = input("Ingrese su nueva contraseña: ")
        new_id = len(self.jugadores)

        print("Bienvenido {}, veo que quieres ser un maestro Programón!".format(new_name))
        print("Para comenzar elige uno de los siguientes programones:")

        success2 = False
        while not success2:
            opcion_programon = input("[1] Charmander\n[2] Squirtle\n[3] Bulbasaur\n >")
            if opcion_programon not in ["1", "2", "3"]:
                print("Ingrese una opción válida")
            else:
                success2 = True
                if int(opcion_programon) == 1:
                    new_programon = Programon(4, "Charmander", ["scratch", "ember", "metal claw"], "fire",
                                              5, [39, 50, 60, 43, 65, 52], 16, 5)
                if int(opcion_programon) == 2:
                    new_programon = Programon(7, "Squirtle", ["tackle", "bubble", "water gun"], "water",
                                              5, [29, 21, 23, 80, 29, 30], 16, 8)
                if int(opcion_programon) == 3:
                    new_programon = Programon(1, "Bulbasaur", ["tackle", "vine whip"], "grass",
                                              5, [45, 65, 65, 49, 45, 49], 16, 2)
        new_player = Jugador(new_id, new_name, new_password, new_programon, PC)
        PC.programones[new_player.unique_name] = [new_player.equipo[0]]
        self.jugadores.append(new_player)
        self.player = new_player
        return

class PCBastian:
    def __init__(self, programonRojo):  # juego es objeto de la clase ProgramonRojo
        self.base_programones = jsonToDict("datos/programones.json")  # lista con (151) diccionarios
        self.sistema = programonRojo
        self.jugadores = programonRojo.jugadores  # lista con los jugadores
        self.programones = {}  # diccionario {"unique_name_jugador": [programon1, programon2, ...]}

    def actualizar_jugadores(self):
        self.jugadores = self.sistema.jugadores
        return

    def ingresar_sistema(self, jugador):
        # actualizar datos
        self.actualizar_jugadores()
        nombre_jugador = input("Ingrese su nombre de usuario: ")
        clave_jugador = input("Ingrese su clave: ")

        login_successful = False
        while not login_successful:
            if jugador.unique_name == nombre_jugador and jugador.password == clave_jugador:
                print("Log in exitoso. {}, a continuacion podras cambiar los programones de "
                      "tu equipo.".format(jugador.unique_name))
                login_successful = True
                self.cambiar_equipo(jugador)
                return
            else:
                print("Usuario y/o clave incorrectos")
                salida = input("[ ENTER ] para salir del sistema\n Presione otra tecla"
                               " para intentar nuevamente\n >")
                if salida == "":
                    return
                else:
                    nombre_jugador = input("Ingrese su nombre de usuario: ")
                    clave_jugador = input("Ingrese su clave: ")

    def cambiar_equipo(self, jugador):
        no_equipo = list(self.programones[jugador.unique_name])
        print("~ Equipo de {} ~".format(jugador.unique_name))
        for i in range(len(jugador.equipo)):
            print("[{}]: {} (nivel = {} | hp = {})".format(i + 1, jugador.equipo[i].name, jugador.equipo[i].level,
                                                           jugador.equipo[i].hp))
            no_equipo.remove(jugador.equipo[i])

        # elimino subevoluciones
        disponibles = []
        for i in range(len(no_equipo)):
            if no_equipo[i].unique_id != -1:
                disponibles.append(no_equipo[i])

        if disponibles == []:
            print("No hay programones disponibles para cambiar")
            return

        print("~ Programones capturados por {} ~\n Disponibles para cambiar:".format(jugador.unique_name))
        capturados = "\n".join("[{}]: {} (nivel = {} | hp = {})".format(
            i + 1, disponibles[i].name, disponibles[i].level, disponibles[i].hp) for i in range(len(disponibles)))
        print(capturados)

        while True:
            remove = input("Escoge un programon para cambiar de tu equipo: ")
            new_programon = input("Escoge un programon para agregar a tu equipo: ")
            if remove.isdigit() and new_programon.isdigit():
                if int(remove) - 1 not in range(len(jugador.equipo)):
                    print("Ingrese un numero de programon de su equipo valido")

                elif int(new_programon) - 1 not in range(len(jugador.progradex.programones_capturados)):
                    print("Ingrese un numero de programon capturado valido")

                else:
                    break
            else:
                print("Ingrese el numero de programon a cambiar / agregar")



        agregar = disponibles[int(new_programon) - 1]
        # cambio programon
        jugador.equipo[int(remove) - 1] = agregar
        print("Ahora {} es parte de tu equipo!".format(agregar.name))
        return


class Menu:
    def __init__(self, programonRojo, PC):
        # me permite acceder a jugador y casi todas las clases
        self.programonRojo = programonRojo
        self.PC = PC
        self.options = {
                        "1": self.opcion_progradex,
                        "2": self.opcion_caminar,
                        "3": self.opcion_datos_jugador,
                        "4": self.opcion_consulta,
                        "5": self.salir,
                        }

    def display_menu(self):
        print("""
    ~ Menu ~
    1: Programones en la Progradex
    2: Caminar
    3: Datos del jugador
    4: Consultas
    5: Salir
            """)

    def run(self):
        while True:
            self.display_menu()
            # en caso de que se encuentre en una ciudad
            if self.programonRojo.player.location is not None and self.programonRojo.player.location_id != 0:
                print("Te encuentras en {}\n    6: Menu ciudad\n".format(self.programonRojo.player.location.name))
            eleccion = input("Ingrese una opcion:\n >")
            # menu ciudad
            if eleccion == "6":
                self.programonRojo.player.location.menu_ciudad(self.programonRojo.player)
            else:
                funcionalidad = self.options.get(eleccion)
                if funcionalidad:
                    funcionalidad()
                else:
                    print("{0} no es una opcion valida".format(eleccion))

    def opcion_progradex(self):
        print(" --- PROGRADEX --- ")
        self.programonRojo.player.progradex.show_programones()

        opcion = input("[ ENTER ] para volver al menu")
        while opcion != "":
            opcion = input("[ ENTER ] para volver al menu")
        return

    def opcion_caminar(self):
        print("""
    ~ Caminar ~
        1: Hacia adelante
        2: Hacia atras
        3: Mostrar mapa
            """)
        eleccion = input("Ingrese una opción:\n >")
        while eleccion not in ["1", "2", "3"]:
            print("{0} no es una opcion valida".format(eleccion))
            eleccion = input("Ingrese una opcion: ")

        if self.programonRojo.player.location_id == 0:
            mapa = Mapa(self.programonRojo.player, self.programonRojo.player.location_id, self.PC)
        else:
            mapa = Mapa(self.programonRojo.player, self.programonRojo.player.location_id, self.PC)

        if eleccion == "1":
            mapa.new_location(1)
        elif eleccion == "2":
            mapa.new_location(-1)
        else:
            mapa.mostrar()
            opcion = input("[ ENTER ] para volver al menu")
            while opcion != "":
                print("Recuerda:", end="")
                opcion = input("[ ENTER ] para volver al menu")
        return

    def opcion_datos_jugador(self):
        print(self.programonRojo.player)
        opcion = input("[ ENTER ] para volver al menu")
        while opcion != "":
            print("Recuerda:", end="")
            opcion = input("[ ENTER ] para volver al menu")
        return

    def opcion_consulta(self):
        print("""
    ~ Consultas ~
        1: Batalla por programon
        2: Ranking de programones
        3: Jugador
        4: Volver al menu
            """)

        eleccion = input("Ingrese una opción:\n >")
        while eleccion not in ["1", "2", "3", "4"]:
            print("{0} no es una opcion valida".format(eleccion))
            eleccion = input("Ingrese una opcion:\n >")

        if eleccion == "1":
            nombre_programon = input("Ingrese el nombre del programon: ")
            buscado = None

            success = False
            while not success:
                for programon in self.PC.programones[self.programonRojo.player.unique_name]:
                    if programon.name == nombre_programon:
                        print("Recolectando informacion de las batallas...")
                        buscado = programon
                        success = True
                if not success:
                    print("No has capturado ningun {}, como para batallar con el".format(nombre_programon))
                    nombre_programon = input("Ingrese el nombre del programon: ")

            print(" ~ Batallas de {} ~".format(nombre_programon))
            if len(buscado.batallas) == 0:
                print("Tu programon no ha batallado aun")
            else:
                for resultado in buscado.batallas:
                    print("Oponente: {} | Resultado: {}".format(resultado[0], resultado[1]))

            opcion = input("[ ENTER ] para volver al menu")
            while opcion != "":
                opcion = input("[ ENTER ] para volver al menu")
            return

        if eleccion == "2":
            print("NO IMPLEMENTADO")
            opcion = input("[ ENTER ] para volver al menu")
            while opcion != "":
                opcion = input("[ ENTER ] para volver al menu")
            return

        if eleccion == "3":
            # arreglar RR
            info_jugador = " -- {} --\n Yenes: {}\n".format(self.programonRojo.player.unique_name,
                                                          self.programonRojo.player.yenes)
            if len(self.programonRojo.player.medals) == 0:
                info_jugador += "Medallas: 0"
            else:
                info_jugador += "Medallas: " + str(len(self.programonRojo.player.medals)) + \
                                "\n > ".join(self.programonRojo.player.medals)
            print(info_jugador)
            for programon in self.PC.programones[self.programonRojo.player.unique_name]:
                print(programon)
                if len(programon.batallas) == 0:
                    print("Tu programon no ha batallado aun")
                else:
                    for resultado in programon.batallas:
                        print("Oponente: {} | Resultado: {}".format(resultado[0], resultado[1]))

            opcion = input("[ ENTER ] para volver al menu")
            while opcion != "":
                opcion = input("[ ENTER ] para volver al menu")
            return

        if eleccion == "4":
            return  # continua en el ciclo while de self.run()

    def salir(self):
        data = {}
        for jug in self.programonRojo.jugadores:
            value = {"unique_name": jug.unique_name, "password": jug.password, "yenes": jug.yenes, "medals": jug.medals,
                     "prograbolas": jug.prograbolas, "location_id": jug.location_id, "equipo": [],
                     "batallas": jug.batallas, "programones_vistos": [], "programones_PC": []}
            vistos = jug.progradex.programones_vistos
            capturados_PC = self.PC.programones[jug.unique_name]

            for pro in jug.equipo:
                value["equipo"].append(pro.unique_id)

            for pro in vistos:
                moves_names = []
                for dicc in pro.moves:
                    moves_names.append(dicc["name"])
                value["programones_vistos"].append({"ide": pro.ide, "name": pro.name, "moves": moves_names,
                                                    "tipo": pro.tipo, "visto_capturado": pro.visto_capturado})
            for pro in capturados_PC:
                moves_names = []
                for dicc in pro.moves:
                    moves_names.append(dicc["name"])
                value["programones_PC"].append({"ide": pro.ide, "unique_id": pro.unique_id, "name": pro.name,
                                                "moves": moves_names, "tipo": pro.tipo, "level": pro.level,
                                                "hp": pro.hp, "special_defense": pro.special_defense,
                                                "special_attack": pro.special_attack, "defense": pro.defense,
                                                "speed": pro.speed, "attack": pro.attack, "iv": pro.iv, "ev": pro.ev,
                                                "evolve_level": pro.evolve_level, "evolve_to": pro.evolve_to,
                                                "batallas": pro.batallas, "visto_capturado": pro.visto_capturado})
            data[jug.unique_id] = value
        dictToJson("datos/infoJugadores.json", data)
        print("Se ha guardado toda tu informacin en el PC\n¡Gracias por jugar ProgramonRojo!\nNos "
              "vemos pronto, {}.".format(self.programonRojo.player.unique_name))
        sys.exit()


if __name__ == "__main__":
    print("Module being run directly")
