# sistema principal
import sys
from jsonReader import jsonToDict, dictToJson
from programones import Programon
from jugador import Jugador
from ciudades import Mapa


class ProgramonRojo:
    def __init__(self):
        self.jugadores = []  # base de datos
        self.player = None

    def log_in(self):
        # RR manera de obtener informacion guardada anteriormente
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
            # no matching username
            print("Los datos ingresados no son validos")

        # falta mucho RR
        self.player = actual_player

    def sign_up(self, PC):
        success = False
        while not success:
            new_name = input("Ingrese un nombre de usuario: ")
            for jugador in self.jugadores:
                if jugador.unique_name == new_name:
                    print("Nombre de usuario no disponible")
                    break
            # new_name disponible
            success = True

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
                # tal vez seria mejor aprovechar el diccionario RR
                # RR implementar funcion para crear programon a partir de id y diccionario
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
        self.player = new_player


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
                      "tu equipo.".format(jugador.name))
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
        print("~ Equipo de {} ~".format(jugador.unique_name))
        equipo = "\n".join("[{}]: {}".format(i + 1, jugador.equipo[i].name) for i in range(len(jugador.equipo)))
        print(equipo)

        print("~ Programones capturados por {} ~".format(jugador.unique_name))
        capturados = "\n".join("[{}]: {}".format(i + 1, jugador.progradex.programones_capturados[i].name) for
                               i in range(len(jugador.progradex.programones_capturados)))
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

        agregar = jugador.progradex.programones_capturados[new_programon - 1]
        # cambio programon
        jugador.equipo[remove - 1] = agregar
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
        print(self.programonRojo.player.progradex.show_programones())
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
        # 3: jugador es de otro jugador ? RR
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
            # utilizar datos de programon.batallas
            # considerar datasets y actualizar en cada batalla
            # dar opcion de nombre incorrecto
            opcion = input("[ ENTER ] para volver al menu")
            while opcion != "":
                opcion = input("[ ENTER ] para volver al menu")
            return

        if eleccion == "2":
            # no entiendo el enunciado RR
            opcion = input("[ ENTER ] para volver al menu")
            while opcion != "":
                opcion = input("[ ENTER ] para volver al menu")
            return

        if eleccion == "3":
            # no entiendo el enunciado RR
            opcion = input("[ ENTER ] para volver al menu")
            while opcion != "":
                opcion = input("[ ENTER ] para volver al menu")
            return

        if eleccion == "4":
            return  # continua en el ciclo while de self.run()

    def salir(self):
        # guardar TODA la informacion RR
        print("Se ha guardado toda tu informacin en el PC\n¡Gracias por jugar ProgramonRojo!\nNos "
              "vemos pronto, {}.".format(self.programonRojo.player.unique_name))
        sys.exit()


if __name__ == "__main__":
    print("Module being run directly")




