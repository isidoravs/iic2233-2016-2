# se utiliza para calcular
from functools import reduce
import numpy as np
from matplotlib import pyplot as plt


class Calculadora:
    def __init__(self, maplemathica):
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
        self.inverse_func = {"Ln": "Exp", "Exp": "Ln", "Abs": "Abs", "Sin": "ArcSin",
                             "Cos": "ArcCos", "Tan": "ArcTan", "Sec": "ArcCos",
                             "Csc": "ArcSin", "ArcSin": "Sin", "ArcCos": "Cos",
                             "ArcTan": "Tan"}
        self.integrates = {"Sin": "-1*Cos[#]", "Cos": "Sin[#]",
                           "Tan": "-Ln[Cos[#]]", "Exp": "Exp[#]",
                           "Ln": "#*Ln[#]-#", "Csc": "", "Sec":"",
                           "ArcSin": "1/(1 - #^2)^(1/2)",
                           "ArcCos": "-1/(1 - #^2)^(1/2)",
                           "ArcTan": "1/(1 + x^2)"}
        self.derivations = {"Sin": "Cos[#]", "Cos": "-1*Sin[#]", "Tan": "(Sec[#])^2", "Csc": "-1*Csc[#]/Tan[#]",
                            "Sec": "Sec[#]*Tan[#]", "ArcSin": "1/(1 - #^2)^(1/2)", "ArcCos": "-1/(1 - #^2)^(1/2)",
                            "ArcTan": "1/(1 + #)^2", "Exp": "Exp[#]", "Ln": "1/#"}
        self.temp = None
        self.parenthesis = [1, 0, 0]  # anidaciones, open, close, index
        self.operation = None  # auxiliar
        self.error = False
        self.show_output = True
        self.assign_func = False
        self.maplemathica = maplemathica

    def pre_calculate(self, old_command, maplemathica):
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

        if self.assign_func:
            if "Derivate" in aux2:
                dfunction = self.derivate(aux2[2:-1])
                return dfunction

            else: # integrate
                intfunction = self.integrate(aux2[2:-1])
                return intfunction

        # evalua llamados a comandos especiales
        command_replace = [aux2[i] if aux2[i] not in self.func_commands and
                                      aux2[i] not in maplemathica.function_names
                           else self.func_commands[aux2[i]](aux2[i + 2:(i + 2 + self.parenthesis_index(aux2[i + 2:]))])
                           if aux2[i] in self.func_commands else self.evaluate_f(aux2[i], aux2[i + 2:(i + 2 + self.parenthesis_index(aux2[i + 2:]))], maplemathica)
                           for i in range(len(aux2))]

        # chequeo su implementacion
        if None in command_replace:
            if self.show_output:
                print("ERROR - not implemented function :(")
            return

        if "plot" in command_replace:
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
        elif not self.show_output:
            return
        else:
            print("ERROR - variable not found")
            return

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
            p1 = int(param1)

        if "." in param2:
            p2 = float(param2)
        else:
            p2 = int(param2)

        if op == "*":
            return str(p1 * p2)

        try:
            if op == "/":
                return str(round(p1 / p2, 5))

            if op == "//":
                return str(round(p1 // p2, 5))

            if op == "%":
                return str(round(p1 % p2, 5))

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

    def summatory(self, instruction):
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
        return self.calculate(numeric)

    def simplify(self, param):
        pass

    def derivate(self, param):
        parameters = " ".join(param).split(",")
        variables = parameters[1:]
        if "[" in parameters[0]:
            aux = parameters[0][parameters[0].index("[") + 1:parameters[0].index("]")]

        function = parameters[0].strip().split()  # lista

        function_names = [key[0] for key in self.maplemathica.functions]

        if function[0] in function_names:
            found = [item for item in self.maplemathica.functions.items()
                     if item[0][0] == function[0]]
            check = found[0][1]

            commmand = check.replace(" ", "")
            aux0 = list(commmand)
            str_operations = "".join([x if x not in self.operations
                                      else " {} ".format(str(x))
                                      for x in aux0])

            if "/  /" in str_operations:
                aux1 = str_operations.replace("/  /", "//")
            else:
                aux1 = str_operations

            if "Pi" in str_operations:
                aux2 = aux1.replace("Pi", str(self.pi)).split()
            else:
                aux2 = aux1.split()

            function = aux2

        if function[0] in self.derivations:
            if aux.strip() == variables[0]:
                dfunction = self.derivations[function[0]].replace("#", aux.strip())
            else:  # regla de la cadena
                dfunction = self.derivations[function[0]].replace("#", aux.strip()) \
                            + "*" + self.derivate([aux.strip(), ",{}".format(variables[0])])
            return dfunction

        else:  # polinomio
            if variables[0] not in function:  # constante
                return "0"

            to_solve = "".join(x if x != "-" else "+-"
                               for x in function).replace(" ", "").split("+")

            # diccionario grado: coef
            grado = {self.set_grado(term, variables[0]): self.set_coef(term, variables[0])
                     for term in to_solve}

            if "0" not in grado.keys():
                grado["0"] = "0"

            derivada = {str(int(key)-1):str(int(grado[key])*int(key))
                        for key in grado}

            polinomio = ["{}*x^{}".format(derivada[key], key)
                         for key in derivada if int(key) > 1]

            if "1" in derivada.keys():
                polinomio.append("{}*x".format(derivada["1"]))

            if "0" in derivada.keys():
                polinomio.append(derivada["0"])

            return "+".join(polinomio)

    def integrate(self, param):
        parameters = " ".join(param).split(",")
        variables = [v[1:] for v in parameters[1:]]

        if "}" in variables[0]:
            var = variables[0].replace("}", "")
        else:
            var = variables[0]

        if "[" in parameters[0]:
            aux = parameters[0][parameters[0].index("[")
                                + 1:parameters[0].index("]")]

        function = parameters[0].strip().split()  # lista

        function_names = [key[0] for key in self.maplemathica.functions]

        if function[0] in function_names:
            found = [item for item in self.maplemathica.functions.items()
                     if item[0][0] == function[0]]
            check = found[0][1]

            commmand = check.replace(" ", "")
            aux0 = list(commmand)
            str_operations = "".join([x if x not in self.operations
                                      else " {} ".format(str(x))
                                      for x in aux0])

            if "/  /" in str_operations:
                aux1 = str_operations.replace("/  /", "//")
            else:
                aux1 = str_operations

            if "Pi" in str_operations:
                aux2 = aux1.replace("Pi", str(self.pi)).split()
            else:
                aux2 = aux1.split()

            function = aux2

        if function[0] in self.integrates:
            if aux.strip() == var:
                intfunction = self.integrates[function[0]].replace("#", aux.strip())
            else:  # regla de la cadena
                intfunction = self.integrates[function[0]].replace("#", aux.strip()) + \
                              "/" + self.derivate([aux.strip(), ",{}".format(var)])
            return intfunction

        else:  # polinomio
            if var not in function:  # constante
                return "0"

            to_solve = "".join(x if x != "-" else "+-"
                               for x in function).replace(" ", "").split("+")

            # diccionario grado: coef
            grado = {self.set_grado(term, var): self.set_coef(term, var)
                     for term in to_solve}

            integral = {str(int(key)+1):str(round(int(grado[key])/(int(key) + 1), 5))
                        for key in grado}

            polinomio = ["{}*x^{}".format(integral[key], key)
                         for key in integral if int(key) > 1]

            if "1" in integral.keys():
                polinomio.append("{}*x".format(integral["1"]))

            if "0" in integral.keys():
                polinomio.append(integral["0"])

            return "+".join(polinomio)

    def plot3D(self, param):
        pass

    def region_plot(self, param):
        pass

    def plot(self, param):
        # no alcance a terminar :(
        parameters = "".join(param).replace(" ", "").split(",")
        function = parameters[0]
        linewidth = parameters[-1]
        color = parameters[-2]
        cota_sup = int(parameters[-3])
        cota_inf = int(parameters[-4])
        parameter = parameters[-5]

        if "Sin" in function:
            x = np.linspace(cota_inf, cota_sup, 500)
            plt.plot(x, np.sin(x), color, linewidth=linewidth)
            plt.show()

        elif "Cos" in function:
            x = np.linspace(cota_inf, cota_sup, 500)
            plt.plot(x, np.cos(x), color, linewidth=linewidth)
            plt.show()

        elif "Tan" in function:
            x = np.linspace(cota_inf, cota_sup, 500)
            plt.plot(x, np.tan(x), color, linewidth=linewidth)
            plt.show()

        elif "ArcSin" in function:
            x = np.linspace(cota_inf, cota_sup, 500)
            plt.plot(x, np.asin(x), color, linewidth=linewidth)
            plt.show()

        elif "ArcCos" in function:
            x = np.linspace(cota_inf, cota_sup, 500)
            plt.plot(x, np.acos(x), color, linewidth=linewidth)
            plt.show()

        elif "ArcTan" in function:
            x = np.linspace(cota_inf, cota_sup, 500)
            plt.plot(x, np.atan(x), color, linewidth=linewidth)
            plt.show()

        else:
            print("not able to plot {}".format(function))
        return "plot"

    def solve(self, param):
        parameters = " ".join(param).split(",")
        equation = parameters[0].split("==")

        # revisar trigonometrica, exp, log
        if equation[0].split()[0] in self.other_operations.keys():
            variable = parameters[1][1:-1].split(",")
            self.solve_other(equation, variable)
            return

        # despeje
        if equation[1] != "0":
            equation[0] += "-{}".format(self.calculate(equation[1].split()))
            equation[1] = "0"

        to_solve = "".join(x if x != "-" else "+-"
                           for x in equation[0]).replace(" ","").split("+")
        variable = parameters[1][1:-1].split(",")  # lista var sin parentesis

        # diccionario grado: coef
        grado = {self.set_grado(term, variable[0]):self.set_coef(term, variable[0])
                 for term in to_solve}

        if "0" not in grado.keys():
            grado["0"] = "0"

        maximo = max(grado.items(), key=lambda x: x[0])
        an = abs(int(maximo[1]))  # coeficiente de la variables de mayor grado
        a0 = abs(int(grado["0"]))  # ver si necesita calculate R

        # print("a0 y an:", a0, an)

        # por el Teorema de raiz racional: factores
        p = [x for x in range(1, a0+1) if a0 % x == 0]
        q = [x for x in range(1, an+1) if an % x == 0]

        # print("p y q:",p,q)

        candidates = [p[i] / q[j] for i in range(len(p)) for j in range(len(q))]
        negative_candidates = [-1 * c for c in candidates]
        possibles = candidates + negative_candidates

        print("possible solutions:", possibles)
        if len(possibles) == 0:
            print("x = 0")

        # corrobora resultado
        checking = [(n, self.check_solve(parameters[0].replace(variable[0], str(n))))
                    for n in candidates]

        solutions = []
        list(solutions.append(x[0]) for x in checking
             if x[1] and x[0] not in solutions)

        to_print = ["{} = {}".format(variable[0], sol) for sol in solutions]
        if len(to_print) == 0 and a0 != 0:
            print("no rational solutions for equation")
        else:
            print(*to_print, sep="\n")

        return

    def solve_other(self, equation, variable):
        aux = equation[0].replace(" ", "")
        command = equation[0].split()[0]
        start = aux.index("[")
        end = aux.index("]")

        new_eq = [aux[start + 1:end], "{}[{}]".format(self.inverse_func[command],
                                                      equation[1].replace(" ", ""))]

        print("{} = {}".format(new_eq[0], self.pre_calculate(new_eq[1], self.maplemathica)))
        return

    def check_solve(self, equation):

        compare = equation.replace(" ", "").split("==")
        result = [self.pre_calculate(x, self.maplemathica)
                  for x in compare]
        return result[0] == result[1]  # booleano

    def set_grado(self, term, variable):
        if variable in term:
            if "^" in term:
                return term[term.index("^") + 1]
            else:
                return "1"
        else:
            return "0"

    def set_coef(self, term, variable):
        if variable in term:
            if "*" in term:
                return term[:term.index("*")]
            else:
                return "1"
        else:  # a0
            if "." in term:
                return float(term)
            elif term.isdigit() or "-" in term:
                return int(term)
            else:
                return self.pre_calculate(term, self.maplemathica)

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
    print("Module being run directly")
