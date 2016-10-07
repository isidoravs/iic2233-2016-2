# interaccion por consola
from interprete import Maplemathica
from sys import exit


class Menu:
    def __init__(self, maplemathica):
        self.maplemathica = maplemathica
        self.help = None
        self.set_help()
        self.consulta()

    def run(self):
        print(" --- Maplemathica --- ")

        # elimino las variables / funciones de consultas.txt
        self.maplemathica.variables = dict()
        self.maplemathica.functions = dict()

        while True:
            eleccion = input("> ")
            if "?" in eleccion:
                command = eleccion[:eleccion.index("?")]
                if command in self.help:
                    resume = self.help[command].split("$")
                    print("{}\n{}".format(resume[0], resume[1]))

                else:
                    print("{} is not a valid command".format(command))

            elif "load" in eleccion:
                path = eleccion.replace("load", "").replace(" ", "").replace(
                    ";","")
                self.load(path)

            elif "save" in eleccion:
                path = eleccion.replace("save", "").replace(" ", "").replace(
                    ";", "")
                self.save(path)

            elif eleccion == "exit;":
                print(" --- Maplemathica --- ")
                exit()

            else:
                # ingresa un comando
                self.opcion_consulta(eleccion)
        return

    def save(self, path):
        if ".txt" not in path:
            path += ".txt"

        file = open("archivos/" + path, "w")

        res = ["---- {} ----\n".format(path)]  # lista de strings
        functions = [self.function_str(x)
                     for x in self.maplemathica.functions.items()]
        variables = ["{} = {};\n".format(x[0], x[1])
                     for x in self.maplemathica.variables.items()]

        res += functions + variables

        file.writelines(res)
        file.close()

        print("{} saved".format(path))
        return

    def function_str(self, item):
        name = item[0][0]
        variables = list(item[0][1])
        func = item[1]
        return "{}{} = {};\n".format(name, variables, func).replace("'", "")

    def load(self, path, to_print=True):
        if ".txt" not in path:
            path += ".txt"
        try:
            file = open("archivos/" + path, 'r')
        except (IOError):
            print('None existing file with that name')
            return

        all_commands = file.readlines()
        list(self.opcion_consulta(x, False) for x in all_commands)

        file.close()
        if to_print:
            print("{} loaded".format(path))
        return

    def consulta(self):
        file = open("archivos\consultas.txt", "r")
        consultas = [line.strip() for line in file]
        file.close()

        resultados = open("archivos/resultados.txt", "w")  # borra datos previos
        list(self.decide_action(x, resultados) for x in consultas)

        resultados.close()
        return

    def decide_action(self, line, file):
        if "txt" in line:  # recibe un nuevo estado
            estado = line.replace(" ", "").split(",")
            result_name = "resultado_{}".format(estado[0])
            file.write("---- {} ----\n".format(result_name))

            # cargo funciones y variables (sin eliminar anteriores)
            self.load(estado[0], False)
        else:
            self.opcion_consulta(line, False, file)
        return

    def opcion_consulta(self, command, to_print=True, file=None):
        if ";" not in command and to_print:
            print("ERROR - missing ';' at the end of statement")
            return

        all_commands = command.split(";")
        result = [self.maplemathica.get_command(c, file) for c in all_commands[:-1]]
        if to_print and not file:  # imprime resultado
            list(print(r) for r in result if r is not None)

        if file is not None:  # resultado en archivo
            file.writelines("{}\n".format(r) for r in result if r is not None)

        return

    def set_help(self):
        help = open("help.txt", "r")
        lines_help = [line.split("#") for line in help.readlines()]
        self.help = {x[0]:x[1] for x in lines_help}
        help.close()

if __name__ == "__main__":
    maplemathica = Maplemathica()
    menu = Menu(maplemathica)
    menu.run()