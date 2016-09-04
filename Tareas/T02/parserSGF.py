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
    arbol = set_arbol(lines_string[:-1], juego)  #string gigante (sin parentesis  inicial ni final)
    return arbol


def set_arbol(data, juego, arbol=None, id_split=0, number_split=0):
    abc_min = "abcdefghijklmnopqrs"
    if arbol is None:
        if data[0] == "(":  # arbol comienza con una variacion
            arbol = ArbolJugadas(0)  # raiz vacia
            juego.total_nodes += 1
            set_arbol(data, juego, arbol, 0, 0)

        else:
            if data[1] == "B":
                x = abc_min.find(data[3])
                y = abc_min.find(data[4])
                arbol = ArbolJugadas(0, "black", 1, x, y)
                juego.total_nodes += 1
                set_arbol(data[7:], juego, arbol, 0, 1)

            elif data[1] == "W":
                x = abc_min.find(data[3])
                y = abc_min.find(data[4])
                arbol = ArbolJugadas(0, "white", 1, x, y)
                juego.total_nodes += 1
                set_arbol(data[7:], juego, arbol, 0, 1)

            else:
                # RR en caso no contado
                print("revisar codigo")

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
                arbol.agregar_nodo(juego.total_nodes, color, prenumber + 1, x, y, id_padre)

                id_padre = juego.total_nodes
                juego.total_nodes += 1
                prenumber += 1

        elif data[0] == "(":  #variacion
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

            for variation in all_variations:
                set_arbol(variation, juego, arbol, id_split, number_split)

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
                arbol.agregar_nodo(juego.total_nodes, color, prenumber + 1, x, y, id_padre)

                id_padre = juego.total_nodes
                juego.total_nodes += 1
                prenumber += 1

            # llamo recursivamente a las variaciones
            set_arbol(new_data, juego, arbol, id_padre, prenumber)

    return arbol


class InfoJuego:
    def __init__(self):
        self.GM = '1'
        self.FF = '4'
        self.CA = 'UTF-8'
        self.SZ = '19'
        # los atrbutos anteriores siempre tendran esos valores
        self.KM = 6.5
        self.EV=None
        self.DT=None
        self.PB = None
        self.PW = None
        self.WR = None
        self.RE = None
        self.SO = None
        self.total_nodes = 0


arbol = sgfToTree("ejemplos/Ejemplo variaciones simple.sgf")

#arbol = sgfToTree("ejemplos/Chen Yaoye vs Lee Sedol.sgf")
print(arbol)