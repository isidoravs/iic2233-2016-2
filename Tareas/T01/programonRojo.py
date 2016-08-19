# sistema principal - improvisacion RR
# todos los imports
from jsonReader import jsonToDict, dictToJson


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
            print("Los datos ingresados no son validos, vuelve a intentar.")
        # falta mucho RR
        self.player = actual_player

    def sign_up(self):
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
        new_player = Jugador(new_id, new_name, new_password, new_programon)
        self.player = new_player


class PCBastian:
    def __init__(self, programonRojo):  # juego es objeto de la clase ProgramonRojo
        self.base_programones = jsonToDict("datos/programones.json")  # lista con (151) diccionarios de 12 keys c/u RR
        # no se usa self.base_programones
        self.jugadores = programonRojo.jugadores  # lista con los jugadores


    def ingresar_sistema(self, jugador, nombre_jugador, clave_jugador):
        # jugador es un objeto de la clase Jugador
        # revisar si existe RR
        # revisar datos correctos
        if jugador.unique_name == nombre_jugador and jugador.password == clave_jugador:
            # ingresar
            pass
        # pensar forma de almacenar (dict?) RR
        pass


class Menu:
    def __init__(self, programonRojo):
        # me permite acceder a jugador y casi todas las clases
        self.programonRojo = programonRojo
        self.options = {
                        "1": self.opcion_progradex,
                        "2": self.opcion_caminar,
                        "3": self.opcion_datos_jugador,
                        "4": self.opcion_consulta,
                        "5": self.salir
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
            eleccion = input("Ingrese una opcion: ")
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
        return  # no se si funciona RR

    def opcion_caminar(self):
        print("""
            ~ Caminar ~
                1: Hacia adelante
                2: Hacia atras
            """)
        eleccion = input("Ingrese una opción: ")
        while eleccion not in ["1", "2"]:
            print("{0} no es una opcion valida".format(eleccion))
            eleccion = input("Ingrese una opcion: ")
        # actualizar posicion segun routes.json
        # analizar tres casos RR

        # para la opcion de Gimnasio:
        # gym = Gimnasio()


    def opcion_datos_jugador(self):
        print(self.programonRojo.player)
        opcion = input("[ ENTER ] para volver al menu")
        while opcion != "":
            print("Recuerda:", end="")
            opcion = input("[ ENTER ] para volver al menu")
        return  # no se si funciona RR

    def opcion_consulta(self):
        # 3: jugador es de otro jugador ? RR
        print("""
            ~ Consultas ~
                1: Batalla por programon
                2: Ranking de programones
                3: Jugador
                4: Volver al menu
            """)

        eleccion = input("Ingrese una opción: ")
        while eleccion not in ["1", "2", "3", "4"]:
            print("{0} no es una opcion valida".format(eleccion))
            eleccion = input("Ingrese una opcion: ")

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






