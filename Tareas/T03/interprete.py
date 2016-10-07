# maneja sintaxis y resultados
from calculo import Calculadora


class Maplemathica:  # almacena las variables y funciones de cada estado
    def __init__(self):
        self.variables = dict()  # (nombre, (variables)): func
        self.functions = dict()
        self.function_names = list()
        self.consultas = {"Divisible": self.isdivisible, "MCM": self.MCM,
                          "MCD": self.MCD}
        self.calculadora = Calculadora()

    def get_command(self, command, file=None):
        if "_]" in command:
            # define funcion
            clean = command.replace(" ", "").split("]=")

            name = clean[0][:clean[0].index("[")]
            num_variable = [i for i, x in enumerate(clean[0]) if x == "_"]
            variables = tuple(clean[0][i - 1] for i in range(len(clean[0]))
                         if i in num_variable)

            # agrego funcion
            check = [x for x in self.functions if name == x[0]]
            if len(check) != 0:
                del self.functions[check[0]]
            self.functions[(name, variables)] = clean[1]

            self.function_names.append(name)
            return "{}{} = {}".format(name, [x for x in variables], clean[1])

        elif "Who" in command:
            self.show_variables(file)
            return

        elif "=" in command:  # RR no se en que otros casos se podria usar
            if "==" in command:  # igualdad
                pass

            elif "!=" in command:  # desigualdad
                pass

            elif "<=" in command:
                pass

            elif ">=" in command:
                pass

            else:  # define variable
                i = command.find("=")
                value = self.calculadora.pre_calculate(command[i + 1:], self)
                self.calculadora.error = False
                name = command[:i].replace(" ", "")
                self.variables[name] = value

                return "{} = {}".format(name, str(value))

        # consultas booleanas
        elif len([x for x in self.consultas if x in command]) > 0:  # consulta
            consult = [x for x in self.consultas if x in command]
            aux = command.replace(" ", "")
            parameters = aux.replace(consult[0], "")  # str de lista con param

            return self.consultas[consult[0]](parameters)  # True o False

        elif "Clear" in command:
            if "AllV" in command:
                self.variables = {}
                print("all variables cleared")

            elif "AllF" in command:
                self.functions = {}
                self.function_names = []
                print("all functions cleared")

            elif "V" in command:
                variable = command.replace("ClearV", "").replace(" ", "")
                if variable in self.variables:
                    del self.variables[variable]
                    print("variable '{}' removed".format(variable))
                else:
                    print("{} not defined as variable".format(variable))

            elif "F" in command:
                name = command.replace("ClearF", "").replace(" ", "")
                key_info = list(filter(lambda x: x[0]== name, self.functions))
                if len(key_info) != 0:
                    del self.functions[key_info[0]]
                    print("function '{}' removed".format(name))
                else:
                    print("{} not defined as function".format(name))

            else:
                print("ERROR - incorrect Clear command")
            return

        else:
            result = self.calculadora.pre_calculate(command, self)

            if file is not None and self.calculadora.error:
                file.write("ERROR in calculation of {}".format(command))

            self.calculadora.error = False
            return result

    def show_variables(self, file):
        if file is None:
            if len(self.variables) == 0:
                print("no variables defined")
            else:
                list(print("{} = {}".format(x, self.variables[x]))
                           for x in self.variables.keys())

        else:  # se escribe en el archivo
            file.writelines("{} = {}\n".format(x, self.variables[x])
                            for x in self.variables.keys())
        return

    def isdivisible(self, parameters):
        aux = parameters[1:-1].split(",")
        num = [int(n) for n in aux]
        if num[0] % num[1] == 0:  # es divisible
            return True
        return False

    def MCM(self, parameters):
        aux = parameters[1:-1].split(",")
        num = [int(n) for n in aux]
        MCM = num[1] * num[2] / self.MCD_recursive(num[1], num[2])  # Euclides
        if num[0] == MCM:
            return True
        return False

    def MCD(self, parameters):
        aux = parameters[1:-1].split(",")
        num = [int(n) for n in aux]
        MCD = self.MCD_recursive(num[1], num[2])  # Euclides
        if num[0] == MCD:
            return True
        return False

    def MCD_recursive(self, b, c):
        # caso base
        if c == 0:
            return b
        # llamada recursiva
        else:
            return self.MCD_recursive(c, b % c)

    def load_file(self):
        # relacion con opcion_importar de Menu
        pass

if __name__ == "__main__":
    print("Module being run directly")
