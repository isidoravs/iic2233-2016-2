# maneja sintaxis y resultados
from calculo import Calculadora


class Maplemathica:  # almacena las variables y funciones de cada estado
    def __init__(self):
        self.variables = dict()  # (nombre, (variables)): func
        self.functions = dict()
        self.function_names = list()
        self.consultas = {"Divisible": self.isdivisible, "MCM": self.MCM,
                          "MCD": self.MCD}
        self.calculadora = Calculadora(self)
        self.consultas_matriz ={"MatrixMultiply": self.multiply, "Det": self.det,
                                "Range": self.range, "Dim": self.dim,
                                "Trans": self.trans, "Inv": self.inv}

    def get_command(self, command, file=None):
        if "_]" in command:
            # define funcion
            clean = command.replace(" ", "").split("]=")

            if "Derivate" in clean[1]:  # asigna a funcion el valor
                self.calculadora.assign_func = True
                clean[1] = self.calculadora.pre_calculate(clean[1], self)
                self.calculadora.assign_func = False

            if "Integrate" in clean[1]:
                self.calculadora.assign_func = True
                clean[1] = self.calculadora.pre_calculate(clean[1], self)
                self.calculadora.assign_func = False

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

        elif "[[" in command:  # matriz
            matrix_def = command.replace(" ", "").split("=")

            matr = matrix_def[1]

            if "|" in matr:
                clean = matr.replace("|", ",")
            else:
                clean = matr

            if "],[" in clean:
                pre_matrix = clean.replace("],[", "#").split("#")
            else:
                pre_matrix = clean

            pre_matrix[0] = pre_matrix[0][2:]
            pre_matrix[-1] = pre_matrix[-1][:-2]

            def content(x, maple):
                result = [int(k) if k.isdigit() else maple.variables[k]
                if k in maple.variables else None for k in x.split(",")]

                if None in result:
                    return
                else:
                    return result

            matrix = [content(x, self) for x in pre_matrix]

            if None in matrix:
                print("Variable not defined")
                return
            else:
                self.variables[matrix_def[0]] = matrix
                return "{} = {}".format(matrix_def[0], matrix)

        elif True in [key in command for key in self.consultas_matriz]:
            if "=" in command:  # define variable
                splitted = command.split("=")
                aux = splitted[1]
                variable = splitted[0]
            else:
                aux = command
                variable = None

            func = [self.consultas_matriz[key] for key in self.consultas_matriz
                    if key in aux]
            result = func[0](aux[aux.index("[") + 1: aux.index("]")])

            if variable is None:
                print(result)
                return
            else:
                self.variables[variable] = result
                print("{} = {}".format(variable.strip(), result))
                return

        elif "Who" in command:
            self.show_variables(file)
            return

        elif "=" in command or "<" in command or ">" in command:  # booleanos
            if "Piecewise" in command:
                pass

            else:
                if "==" in command:  # igualdad
                    if "Solve" in command:
                        self.calculadora.show_output = False
                        result = self.calculadora.pre_calculate(command, self)

                        if file is not None and self.calculadora.error:
                            file.write("ERROR in calculation of {}".format(command))

                        self.calculadora.error = False
                        self.calculadora.show_output = True
                        return result

                    else:
                        compare = command.replace(" ","").split("==")
                        result = [self.calculadora.pre_calculate(x, self)
                                  for x in compare]
                        return result[0] == result[1]

                elif "!=" in command:  # desigualdad
                    compare = command.replace(" ", "").split("!=")
                    result = [self.calculadora.pre_calculate(x, self)
                              for x in compare]
                    return result[0] != result[1]

                elif "<=" in command:
                    compare = command.replace(" ", "").split("<=")
                    result = [self.calculadora.pre_calculate(x, self)
                              for x in compare]
                    return result[0] <= result[1]

                elif ">=" in command:
                    compare = command.replace(" ", "").split(">=")
                    result = [self.calculadora.pre_calculate(x, self)
                              for x in compare]
                    return result[0] >= result[1]

                elif "<" in command:
                    compare = command.replace(" ", "").split("<")
                    result = [self.calculadora.pre_calculate(x, self)
                              for x in compare]
                    return result[0] < result[1]

                elif ">" in command:
                    compare = command.replace(" ", "").split(">")
                    result = [self.calculadora.pre_calculate(x, self)
                              for x in compare]
                    return result[0] > result[1]

                else:  # define variable
                    i = command.find("=")
                    value = self.calculadora.pre_calculate(command[i + 1:], self)
                    self.calculadora.error = False
                    name = command[:i].replace(" ", "")
                    self.variables[name] = value

                    return "{} = {}".format(name, str(value))

        elif "&&" in command and "||" in command:  # comparacion de booleanos
            if "Piecewise" not in command and "Solve" not in command:
                if "&&" in command:
                    compare = command.replace(" ", "").split("&&")
                    result = [self.get_command(x, self) for x in compare]
                    return result[0] and result[1]

                elif "||" in command:
                    compare = command.replace(" ", "").split("||")
                    result = [self.get_command(x, self) for x in compare]
                    return result[0] or result[1]

            elif "Solve" in command:
                pass

            else:  # Piecewise
                pass

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

    def multiply(self, matrix):
        # help from http://www.programiz.com/python-programming/examples/multiply-matrix
        all_matrix = matrix.replace(" ","").split(",")
        A = self.variables[all_matrix[0]]
        B = self.variables[all_matrix[1]]
        C = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]

        if len(A[0]) != len(B):
            return "ERROR - not able to multiply both matrix"

        def change(X, Y, result, i, j, k):
            result[i][j] += X[i][k] * Y[k][j]

        list(change(A, B, C, i, j, k) for i in range(len(A))
             for j in range(len(B[0])) for k in range(len(B)))

        return C

    def det(self, matrix):
        return "ERROR - not implemented function :("

    def range(self, matrix):
        return "ERROR - not implemented function :("

    def dim(self, matrix):
        matr = self.variables[matrix]
        m = len(matr[0])
        n = len(matr)
        return "{} x {}".format(m, n)

    def trans(self, matrix):
        # http://stackoverflow.com/questions/10169919/python-matrix-transpose-and-zip
        matr = self.variables[matrix]
        return list(map(list, zip(*matr)))

    def inv(self, matrix):
        return "ERROR - not implemented function :("

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
