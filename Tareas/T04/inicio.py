

class Inicio:
    def __init__(self):
        self.god1 = None
        self.god2 = None
        self.power1 = None
        self.power2 = None
        self.race1 = None
        self.race2 = None
        self.rate1 = None  # diccionarios
        self.rate2 = None
        self.heroe1_rate = 0
        self.heroe2_rate = 0
        self.tiempo_max = 0
        self.set_parameters()

    def set_parameters(self):
        print(" --- Guerra de dioses --- ")

        # tiempo simulacion
        while True:
            tiempo = input("Ingrese tiempo de simulación: ")
            try:
                self.tiempo_max = int(tiempo)
                break

            except (ValueError) as err:
                print("[ERROR]: {}".format(err))
                print("Tiempo de simulacion debe ser un numero entero")

        # raza
        self.set_race()

        # dioses
        self.set_god()

        # powers
        self.set_power()

        # rates
        self.set_rate()

        # heroe
        self.set_heroe_rate()
        return

    def set_god(self):
        dioses = ["GodPezoa", "Jundead", "GodessFlo", "Godolfo"]
        format_dioses = ["pezoa", "june", "flo", "rodolfo"]

        print("\n[Team 1]")
        god1 = input("Seleccione dios de su ejercito:\n"
                      "[1] {}\n[2] {}\n[3] {}\n[4] {}\n "
                     ">".format(dioses[0], dioses[1], dioses[2], dioses[3]))

        while god1 not in ["1", "2", "3", "4"]:
            god1 = input("TEAM 1: Ingrese opción válida\n >")

        self.god1 = format_dioses[int(god1) - 1]
        dioses.pop(int(god1) - 1)  # evita escoger repetidos
        format_dioses.pop(int(god1) - 1)

        print("[Team 2]")
        god2 = input("Seleccione dios de su ejercito:\n"
                      "[1] {}\n[2] {}\n[3] {}\n >"
                     "".format(dioses[0], dioses[1], dioses[2]))

        while god2 not in ["1", "2", "3"]:
            god2 = input("TEAM 2: Ingrese opción válida\n >")

        self.god2 = format_dioses[int(god2) - 1]

    def set_power(self):
        powers = ["plaga", "berserker", "terremoto", "invocar_muertos", "glaciar"]

        print("\n[Team 1]")
        power1 = input("Seleccione el poder de {}:\n"
                     "[1] {}\n[2] {}\n[3] {}\n[4] {}\n[5] {}\n >"
                       "".format(self.god1, powers[0], powers[1],
                                 powers[2], powers[3], powers[4]))

        while power1 not in ["1", "2", "3", "4", "5"]:
            power1 = input("TEAM 1: Ingrese opción válida\n >")

        self.power1 = powers[int(power1) - 1]
        powers.pop(int(power1) - 1)

        print("[Team 2]")
        power2 = input("Seleccione el poder de {}:\n"
                       "[1] {}\n[2] {}\n[3] {}\n[4] {}\n >"
                       "".format(self.god1, powers[0], powers[1],
                                 powers[2], powers[3]))
        while power2 not in ["1", "2", "3", "4"]:
            power2 = input("TEAM 2: Ingrese opción válida\n >")

        self.power2 = powers[int(power2) - 1]

    def set_race(self):
        races = ["Human", "Orc", "Skull"]

        print("\n[Team 1]")
        race1 = input("Seleccione raza de su ejercito:\n"
                      "[1] {}\n[2] {}\n[3] {}\n >".format(races[0], races[1],
                                                          races[2]))

        while race1 not in ["1", "2", "3"]:
            race1 = input("TEAM 1: Ingrese opción válida\n >")

        self.race1 = races[int(race1) - 1]
        races.pop(int(race1) - 1)

        print("[Team 2]")
        race2 = input("Seleccione raza de su ejercito:\n"
                      "[1] {}\n[2] {}\n >".format(races[0], races[1]))
        while race2 not in ["1", "2"]:
            race2 = input("TEAM 2: Ingrese opción válida\n >")

        self.race2 = races[int(race2) - 1]

    def set_rate(self):
        print("\n[Team 1]")
        rate1 = input("Ingrese razon de creacion 'guerreros:arqueros:"
                      "mascotas'\n >")

        clean1 = rate1.replace(" ", "").split(":")
        valid = [n.isdigit() for n in clean1]

        while len(clean1) != 3 or False in valid:
            rate1 = input("TEAM 1: Ingrese en formato especificado\n >")
            clean1 = rate1.replace(" ", "").split(":")
            valid = [n.isdigit() for n in clean1]

        print("[Team 2]")
        rate2 = input("Ingrese razon de creacion 'guerreros:arqueros:"
                      "mascotas'\n >")

        clean2 = rate2.replace(" ", "").split(":")
        valid = [n.isdigit() for n in clean2]

        while len(clean2) != 3 or False in valid:
            rate2 = input("TEAM 2: Ingrese en formato especificado\n >")
            clean2 = rate2.replace(" ", "").split(":")
            valid = [n.isdigit() for n in clean1]

        self.rate1 = {"warrior": clean1[0], "archer": clean1[1], "pet": clean1[2]}
        if self.god1 == "flo":  # cambia proporcion
            greatest = max(int(self.rate1['warrior']), int(self.rate1['archer']),
                           int(self.rate1['pet']))
            self.rate1['pet'] = greatest + 2

        self.rate2 = {"warrior": clean2[0], "archer": clean2[1], "pet": clean2[2]}
        if self.god2 == "flo":  # cambia proporcion
            greatest = max(int(self.rate2['warrior']), int(self.rate2['archer']),
                           int(self.rate2['pet']))
            self.rate2['pet'] = greatest + 2

    def set_heroe_rate(self):
        while True:
            heroe1 = input("\n[Team 1]\nIngrese tasa de invocacion del heroe\n >")

            if "/" in heroe1:  # fraccion
                try:
                    values = heroe1.split("/")
                    num = int(values[0])
                    den = int(values[1])
                    self.heroe1_rate = num / den
                except ValueError:
                    print("[ERROR] incorrect fraction format")
                else:
                    break

            else:
                try:
                    self.heroe1_rate = float(heroe1)
                except ValueError as err:
                    print("[ERROR] {}".format(err))
                else:
                    break

        while True:
            heroe2 = input("[Team 2]\nIngrese tasa de invocacion del heroe\n >")

            if "/" in heroe2:  # fraccion
                try:
                    values = heroe2.split("/")
                    num = int(values[0])
                    den = int(values[1])
                    self.heroe2_rate = num / den
                except ValueError:
                    print("[ERROR] incorrect fraction format")
                else:
                    break

            else:
                try:
                    self.heroe2_rate = float(heroe2)
                except ValueError as err:
                    print("[ERROR] {}".format(err))
                else:
                    break

if __name__ == "__main__":
    print("Module being run directly")
