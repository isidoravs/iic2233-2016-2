# se utiliza para calcular
from functools import reduce


class Calculadora:
    def __init__(self):
        self.operations = ["^", "*", "/", "//", "%", "-", "+", "[", "]", "(", ")"]
        self.pi = 3.14159265
        self.other_operations = {"Ln": self.log, "Exp": self.exp, "Abs": self.abs,
                                 "Sin": self.sin, "Cos": self.cos,
                                 "Tan": self.tan, "Sec": self.sec,
                                 "Csc": self.csc, "ArcSin": self.arcsin,
                                 "ArcCos": self.arccos, "ArcTan": self.arctan}
        self.func_commands = {"Sum": self.summatory, "FullSimplify": self.simplify,
                              "Derivate": self.derivate, "Plot3D": self.plot3D,
                              "RegionPlot": self.region_plot, "Plot": self.plot,
                              "Integrate": self.integrate, "Solve": self.solve,
                              "Piecewise": self.piecewise}
        self.temp = None
        self.parenthesis = [1, 0, 0]  # anidaciones, open, close, index
        self.operation = None  # auxiliar
        self.error = False

    def pre_calculate(self, old_command, maplemathica):
        # faltan parentesis () RR
        commmand = old_command.replace(" ", "")
        aux = list(commmand)
        str_operations = "".join([x if x not in self.operations
                                 else " {} ".format(str(x))
                                 for x in aux])

        if "/  /" in str_operations:
            aux1 = str_operations.replace("/  /", "//")
        else:
            aux1 = str_operations

        if "Pi" in str_operations:
            aux2 = aux1.replace("Pi", str(self.pi)).split()
        else:
            aux2 = aux1.split()

        print("Aux2:", aux2)

        if "(" in aux2:  # cambia orden de prioridad
            parenthesis_replace = [aux2[i] if "(" not in aux2[i] else
                                   "({}".format(self.pre_calculate("".join(aux2[i + 2: (i + 2 + self.parenthesis_index(aux2[i + 2:], "()"))]), maplemathica))
                                   for i in range(len(aux2))]


            apearances_start = [i for i, x in enumerate(aux2) if
                                "(" in x]
            apearances_end = [i for i, x in enumerate(aux2) if
                              x == ")"]

            ranges = list(zip(apearances_start, apearances_end))

            no_parenthesis = [parenthesis_replace[k] for k in
                              range(len(parenthesis_replace)) if not
                              any(lower < k <= upper
                                  for (lower, upper) in ranges)]

            aux2 = [x if "(" not in x else x[1:] for x in no_parenthesis]

        # evalua llamados a comandos especiales
        command_replace = [aux2[i] if aux2[i] not in self.func_commands and
                                      aux2[i] not in maplemathica.function_names
                           else self.func_commands[aux2[i]](aux2[i + 2:(i + 2 + self.parenthesis_index(aux2[i + 2:]))])
                           if aux2[i] in self.func_commands else self.evaluate_f(aux2[i], aux2[i + 2:(i + 2 + self.parenthesis_index(aux2[i + 2:]))], maplemathica)
                           for i in range(len(aux2))]

        # chequeo su implementacion
        if None in command_replace:
            print("ERROR - not implemented function :(")
            return

        # elimino lo contenido en parentesis (si paso por las funciones)

        if command_replace != aux2:
            if "[" in command_replace:
                apearances_start = [i for i, x in enumerate(command_replace) if
                                    x == "["]
                apearances_end = [i for i, x in enumerate(command_replace) if x == "]"]

                ranges = list(zip(apearances_start, apearances_end))
                pre_operation = [command_replace[k] for k in
                                 range(len(command_replace)) if not
                                 any(lower <= k <= upper for (lower, upper) in ranges)]

            else:
                pre_operation = command_replace
        else:
            pre_operation = command_replace

        operation = self.eval_variables(pre_operation, maplemathica)

        if operation is not None:
            return self.calculate([str(n) for n in operation])
        elif self.error:
            return
        else:
            print("ERROR - variable not found")
            return
        # falta con self.other_operations RR

    def calculate(self, old_operation):  # lista
        # arregla negativos
        if old_operation[0] == "-":
            operation = ["0"] + old_operation
        else:
            operation = old_operation

        # primero factoriales
        try:
            aux = [n if "!" not in n else str(self.fact(int(n[:-1])))
                         for n in operation]
        except (ValueError) as err:
            print("ERROR - {}, not able to calculate float factorial".format(err))
            return

        # other operations
        other_op = [aux[i] if aux[i] not in self.other_operations
                    else self.other_operations[aux[i]](aux[i + 2 : (i + 2 + self.parenthesis_index(aux[i + 2:]))])
                    for i in range(len(aux))]

        if None in other_op:  # dominio restringido
            self.error = True
            print("ERROR - Parameter not in function domain or indeterminated")
            return

        # elimino lo contenido en parentesis
        if "[" in other_op:
            apearances_start = [i for i, x in enumerate(other_op) if x == "["]
            apearances_end = [i for i, x in enumerate(other_op) if x == "]"]

            ranges = list(zip(apearances_start, apearances_end))
            self.temp = [other_op[k] for k in range(len(other_op))
                         if not any(lower <= k <= upper for (lower, upper) in ranges)]

        else:
            self.temp = other_op

        aux = [self.all_operations(self.temp, k) for k in self.operations[:-4]
               if k in self.temp]

        if "ERROR" in aux:
            self.temp = None
            return

        if "." in self.temp[0]:
            result = float(self.temp[0])
        else:
            result = int(self.temp[0])
        self.temp = None

        return result

    def all_operations(self, operation, op):
        next_operation = [self.basic_op(operation[i - 1], op, operation[i + 1])
                          if operation[i] == op else
                          operation[i] if
                          i != 0 and i != len(operation) - 1 and
                          operation[i + 1] != op and operation[i - 1] != op else
                          operation[i] if i == 0 and operation[i + 1] != op
                          or i == len(operation) - 1 and operation[i - 1] != op else
                          None for i in range(len(operation))]

        if "ERROR" in next_operation:
            return "ERROR"

        clean_operation = [x for x in next_operation if x is not None]
        self.temp = clean_operation
        return

    def basic_op(self, param1, op, param2):
        if "." in param1:  # float
            p1 = float(param1)
        else:  # int
            p1 = int(param1)  # falta cuando es variable RR

        if "." in param2:
            p2 = float(param2)
        else:
            p2 = int(param2)

        if op == "*":
            return str(p1 * p2)

        try:
            if op == "/":
                return str(p1 / p2)

            if op == "//":
                return str(p1 // p2)

            if op == "%":
                return str(p1 % p2)

        except (ZeroDivisionError) as err:
            self.error = True
            print("ERROR - {}".format(err))
            return "ERROR"

        if op == "^":
            return str(p1 ** p2)

        if op == "+":
            return str(p1 + p2)

        if op == "-":
            return str(p1 - p2)

    def eval_variables(self, operation, maplemathica):  # lista con coeficientes y operaciones
        # chequea que las variables sean reemplazadas
        new = [x if x in self.operations or x in self.other_operations or
                    x.isdigit() or "." in x or ("!" in x and x[:-1].isdigit()) else
               self.evaluate_v(x, maplemathica) if "!" not in x else
               str(self.evaluate_v(x[:-1], maplemathica)) + "!" for x in operation]

        if None not in new:
            return new

        else:
            return None

    def evaluate_v(self, variable, maplemathica):
        if variable not in maplemathica.variables.keys():
            return None
        else:
            return maplemathica.variables[variable]

    def evaluate_f(self, name, param, maplemathica):
        key_info = list(filter(lambda x: x[0][0] == name, maplemathica.functions.items()))
        function = key_info[0][1]
        variables = key_info[0][0][1]

        if "[" not in param:
            pre_values = " ".join(param).split(",")
        else:
            str_param = "".join(param)
            apearances_start = [i for i, x in enumerate(str_param) if x == "["]
            apearances_end = [i for i, x in enumerate(str_param) if x == "]"]

            ranges = list(zip(apearances_start, apearances_end))
            aux = [str_param[k] if str_param[k] != "," else "#"
            if not any(lower <= k <= upper for (lower, upper) in ranges) else
            "," for k in range(len(str_param))]

            pre_values = " ".join(aux).split("#")


        values = [str(self.pre_calculate(n, maplemathica)) for n in pre_values]

        aux = list(function)
        str_operations = "".join([x if x not in self.operations
                                  else " {} ".format(str(x))
                                  for x in aux])

        if "/  /" in str_operations:
            aux1 = str_operations.replace("/  /", "//")
        else:
            aux1 = str_operations

        if "Pi" in str_operations:
            aux2 = aux1.replace("Pi", str(self.pi)).split()
        else:
            aux2 = aux1.split()

        assigned = {variables[i]:values[i] for i in range(len(variables))}
        evaluated = [x if x not in assigned else assigned[x] for x in aux2]

        # valor
        return str(self.calculate(evaluated))

    def fact(self, num):
        if num == 0:
            return 1.0
        else:
            factorial = reduce(lambda x,y: x*y, range(1, num + 1))
            return float(factorial)  # retorna float no str

    # reciben una lista con lo que reciben como parametro
    def log(self, param):
        x = self.calculate(param)

        if x <= 0:
            print("'Ln' not defined for x <= 0")
            return


        log_sum = list(map(lambda n: ((x**2 - 1) / (x**2 + 1)) ** (2*n + 1) / (2*n + 1), range(0, 3000)))
        result = reduce(lambda x,y: x+y, log_sum)
        return str(result)

    def exp(self, param):
        x = self.calculate(param)
        exp_sum = list(map(lambda n: x**n / self.fact(n), range(0, 85)))
        result = reduce(lambda x, y: x + y, exp_sum)
        return str(result)

    def abs(self, param):
        value = self.calculate(param)
        return str(abs(value))

    def sin(self, param):
        x = self.calculate(param)
        sin_sum = list(map(lambda n: ((-1) ** n) * x ** (2 * n + 1) /
                                     self.fact(2 * n + 1), range(0, 85)))
        result = reduce(lambda x, y: x + y, sin_sum)

        # en caso de numero muy cercano a cero
        if self.aprox(result):
            result = 0.0

        return str(result)

    def cos(self, param):
        x = self.calculate(param)
        cos_sum = list(map(lambda n: (-1)**n * x**(2*n) / self.fact(2*n),
                           range(0, 85)))
        result = reduce(lambda x, y: x + y, cos_sum)

        if self.aprox(result):
            result = 0.0

        return str(result)

    def tan(self, param):
        sin_result = float(self.sin(param))
        cos_result = float(self.cos(param))
        try:
            return str(sin_result / cos_result)
        except (ZeroDivisionError) as err:
            print("ERROR - {}, undefined result for "
                  "Tan[{}]".format(err, "".join(param)))
            return

    def sec(self, param):
        cos_result = float(self.cos(param))
        try:
            return str(1 / cos_result)
        except (ZeroDivisionError) as err:
            print("ERROR - {}, undefined result for "
                  "Sec[{}]".format(err, "".join(param)))
            return

    def csc(self, param):
        sin_result = float(self.sin(param))
        try:
            return str(1 / sin_result)
        except (ZeroDivisionError) as err:
            print("ERROR - {}, undefined result for "
                  "Csc[{}]".format(err, "".join(param)))
            return

    def arcsin(self, param):
        x = self.calculate(param)
        # restringir dominio
        if x < -1 or x > 1:
            print("'ArcSin' not defined for x not in [-1, 1]")
            return

        arcsin_sum = list(map(lambda n: self.fact(2 * n) * x ** (2 * n + 1)
                                     / (4 ** n * (self.fact(n)) ** 2 *
                                        (2 * n + 1)), range(0, 85)))
        result = reduce(lambda x, y: x + y, arcsin_sum)

        if self.aprox(result):
            result = 0.0

        return str(result)

    def arccos(self, param):
        x = self.calculate(param)
        # restringir dominio
        if x < -1 or x > 1:
            print("'ArcCos' not defined for x not in [-1, 1]")
            return

        result = self.pi / 2 - float(self.arcsin(param))

        if self.aprox(result):
            result = 0.0

        return str(result)

    def arctan(self, param):
        x = self.calculate(param)
        # restringir dominio
        if x < -1 or x > 1:
            print("'ArcTan' not defined for x not in [-1, 1]")
            return

        arctan_sum = list(map(lambda n: (-1)**n * x ** (2 * n + 1) / (2 * n + 1),
                              range(0, 85)))
        result = reduce(lambda x, y: x + y, arctan_sum)

        if self.aprox(result):
            result = 0.0

        return str(result)

    def summatory(self, instruction):  # una variable RR
        param = "".join(instruction).split(",")
        function = param[0]
        variable = param[1][1:]  # saco parentesis
        start = int(param[2])
        end = int(param[3][:-1])  # saco parentesis

        pre_sum = list(self.math_replace(function, variable, i)
                       for i in range(start, end + 1))
        result = reduce(lambda x, y: x + y, pre_sum)
        return str(result)

    def math_replace(self, string, variable, i):
        numeric = string.replace(variable, str(i))
        # tal vez con pre_calculate se reemplazan variables RR
        return self.calculate(numeric)

    def simplify(self, param):
        pass

    def derivate(self, param):
        pass

    def plot3D(self, param):
        pass

    def region_plot(self, param):
        pass

    def plot(self, param):
        pass

    def integrate(self, param):
        pass

    def solve(self, param):
        pass

    def piecewise(self, param):
        pass

    def parenthesis_index(self, lista, paren_type="[]"):  # la continuacion de la lista
        analysis = [self.set_parenthesis(lista[i], i, paren_type) for i in range(len(lista))]
        self.parenthesis = [1, 0, 0]

        resp = [p for p in analysis if p[0] == p[1]]
        return resp[0][2]  # indice de parentesis final

    def set_parenthesis(self, symbol, i, paren_type):
        if symbol == paren_type[0]:
            self.parenthesis[0] += 1
            self.parenthesis[2] = i
            ret = tuple(x for x in self.parenthesis)

        elif symbol == paren_type[1]:
            self.parenthesis[1] += 1
            self.parenthesis[2] = i
            ret = tuple(x for x in self.parenthesis)

        else:
            ret = (1, 0, 0)

        return ret

    def aprox(self, num):  # aproxima numeros muy cercanos a cero dejados como exp
        if num < 0.00000001 and num > -0.00000001:
            return True
        return False


if __name__ == "__main__":
    calculadora = Calculadora()
    print(calculadora.calculate(["1", "+", "3!"]))
