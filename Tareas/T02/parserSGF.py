# lector de archivos de tipo SGF
from myEDD import MyList
from arbol import ArbolJugadas


def sgfToTree(path):
    juego = InfoJuego()
    data = open(path, 'r')
    lines = data.readlines()
    lines_string = ""

    start = False
    for line in lines:
        if ";B[" in line:
            start = True

        if start:
            lines_string += line.strip()

    data.seek(0)
    while True:
        line = data.readline()
        if ";B[" in line:
            break

        else:
            if 'KM[' in line:
                i = line.find('KM[')
                j = line[i:].find(']')
                komi = line[i + 3:i + j]
                if komi.isdigit():
                    juego.KM = int(komi)
                else:  # decimal
                    dot = komi.find(".")
                    uni = int(komi[:dot])
                    dec = int(komi[dot + 1:]) / (10**(len(komi[dot + 1:])))
                    juego.KM = uni + dec

            if 'EV[' in line:
                i = line.find('EV[')
                j = line[i:].find(']')
                juego.EV = line[i + 3:i + j]

            if 'DT[' in line:
                i = line.find('DT[')
                j = line[i:].find(']')
                juego.DT = line[i + 3:i + j]

            if 'PB[' in line:
                i = line.find('PB[')
                j = line[i:].find(']')
                juego.PB = line[i + 3:i + j]

            if 'PW[' in line:
                i = line.find('PW[')
                j = line[i:].find(']')
                juego.PW = line[i + 3:i + j]

            if 'WR[' in line:
                i = line.find('WR[')
                j = line[i:].find(']')
                juego.WR = line[i + 3:i + j]

            if 'RE[' in line:
                i = line.find('RE[')
                j = line[i:].find(']')
                juego.RE = line[i + 3:i + j]

            if 'SO[' in line:
                i = line.find('SO[')
                j = line[i:].find(']')
                juego.SO = line[i + 3:i + j]

    # comienza el arbol
    arbol_jugadas = set_arbol(lines_string[:-1], juego)  # string gigante (sin parentesis  inicial ni final)
    return MyList(arbol_jugadas, juego)


def set_arbol(data, juego, arbol_jugadas=None, id_split=0, number_split=0, depth=0):
    abc_min = "abcdefghijklmnopqrs"
    if arbol_jugadas is None:
        if data[0] == "(":  # arbol comienza con una variacion
            arbol_jugadas = ArbolJugadas(0)  # raiz vacia
            juego.total_nodes += 1
            set_arbol(data, juego, arbol_jugadas, 0, 0, 0)

        else:
            if data[1] == "B":
                x = abc_min.find(data[3])
                y = abc_min.find(data[4])
                arbol_jugadas = ArbolJugadas(0)
                arbol_jugadas.agregar_nodo(1, "black", 1, 0, x, y, 0)
                juego.total_nodes += 2
                set_arbol(data[7:], juego, arbol_jugadas, 0, 1, 0)

            elif data[1] == "W":
                x = abc_min.find(data[3])
                y = abc_min.find(data[4])
                arbol_jugadas = ArbolJugadas(0)
                arbol_jugadas.agregar_nodo(1, "white", 1, 0, x, y, 0)
                juego.total_nodes += 2
                set_arbol(data[7:], juego, arbol_jugadas, 0, 1, 0)

    else:
        # caso base
        if data.count("(") == 0 and data.count(")") == 0:  # ;B[ ];W[ ];B[ ];W[ ] ese estilo
            nodes = data.split(";")
            to_append = MyList(*nodes)
            id_padre = id_split
            prenumber = number_split
            for i in range(len(to_append)):
                nodo = to_append[i]
                if nodo[0] == "B":
                    color = "black"
                elif nodo[0] == "W":
                    color = "white"

                if "[]" in nodo:  # paso
                    x = None
                    y = None
                else:
                    x = abc_min.find(nodo[2])
                    y = abc_min.find(nodo[3])

                arbol_jugadas.agregar_nodo(juego.total_nodes, color, prenumber + 1, depth, x, y, id_padre)

                id_padre = juego.total_nodes
                juego.total_nodes += 1
                prenumber += 1

        elif data[0] == "(":  # variacion
            all_variations = MyList()
            opened = 0
            closed = 0
            inicio = 0
            for i in range(len(data)):
                if data[i] == "(":
                    opened += 1

                if data[i] == ")":
                    closed += 1

                if opened != 0 and opened == closed:  # closed en i
                    all_variations.append(data[inicio + 1: i])
                    opened = 0
                    closed = 0
                    inicio = i + 1

            new_depth = depth
            for variation in all_variations:
                set_arbol(variation, juego, arbol_jugadas, id_split, number_split, new_depth)
                new_depth += 1

        else:  # caso en que no es directamente variacion, pero tiene variaciones dentro
            for i in range(len(data)):
                if data[i] == "(":  # comienza la variacion
                    previous = data[:i]
                    new_data = data[i:]  # contiene las variaciones
                    break

            # agrego nodos antes de la variacion
            nodes = previous.split(";")
            to_append = MyList(*nodes)
            id_padre = id_split
            prenumber = number_split
            for i in range(len(to_append)):
                nodo = to_append[i]
                if nodo[0] == "B":
                    color = "black"
                elif nodo[0] == "W":
                    color = "white"

                if "[]" in nodo:  # paso
                    x = None
                    y = None
                else:
                    x = abc_min.find(nodo[2])
                    y = abc_min.find(nodo[3])
                arbol_jugadas.agregar_nodo(juego.total_nodes, color, prenumber + 1, depth, x, y, id_padre)

                id_padre = juego.total_nodes
                juego.total_nodes += 1
                prenumber += 1

            # llamo recursivamente a las variaciones
            set_arbol(new_data, juego, arbol_jugadas, id_padre, prenumber, depth)

    return arbol_jugadas


class InfoJuego:
    def __init__(self):
        self.GM = '1'
        self.FF = '4'
        self.CA = 'UTF-8'
        self.SZ = '19'
        # los atrbutos anteriores siempre tendran esos valores
        self.KM = 6.5
        self.EV = None
        self.DT = None
        self.PB = None
        self.PW = None
        self.WR = None
        self.RE = None
        self.SO = None
        self.total_nodes = 0


if __name__ == '__main__':
    arbol_jugadas = sgfToTree("ejemplos/Ejemplo variaciones simple.sgf")
    # arbol_jugadas = sgfToTree("ejemplos/Chen Yaoye vs Lee Sedol.sgf")
    # arbol_jugadas = sgfToTree("ejemplos/pass_example.sgf")
    # arbol_jugadas = sgfToTree("ejemplos/Ejemplo con capturas y variaciones.sgf")
    print(arbol_jugadas)
