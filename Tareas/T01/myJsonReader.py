from jsonReader import jsonToDict


def myJsonToDict(path):
    lines = open_file(path)
    if "[" in lines[0] and "]" in lines[-1]:  # lista con diccionarios
        content = lines[1:-1]
        final = listas_diccionario(content)
    else:
        final = recursive_call(lines)

    return final


def recursive_call(convert):
    # caso base: un solo diccionario {'key': value, 'key': value ...}
    dicc = {}  # de lo que estan en listas, no en values
    i = 0
    while i < len(convert):
        if ':' in convert[i]:  # es una key
            if "[" not in convert[i] and "{" not in convert[i]:
                dicc.update(normal_value(dicc, convert[i]))
                i += 1

            elif "[" in convert[i]:
                if "]" in convert[i]:  # caso lista con entero
                    new_key = convert[i].split(':')
                    clean_key = new_key[0].replace('"', '')
                    if "[]" in convert[i]:
                        dicc[clean_key] = []
                    else:
                        aux1 = new_key[1].strip().replace("[", "")
                        aux2 = aux1.replace("]", "")
                        revisar = aux2.split(",")
                        new_list = [int(n) for n in revisar]
                        dicc[clean_key] = new_list
                    i += 1

                else:
                    seleccion = []
                    opened = 0
                    closed = 0
                    for j in range(i, len(convert)):
                        if "]" not in convert[j]:
                            if "[" in convert[j]:
                                opened += 1
                            seleccion.append(convert[j])
                        if "]" in convert[j]:
                            closed += 1
                            if opened == closed:
                                i = j + 1
                                break
                            else:
                                seleccion.append(convert[j])
                    dicc.update(list_value(seleccion))

            elif "{" in convert[i]:
                seleccion = []
                new_key = convert[i].split(':')
                clean_key1 = new_key[0].replace(',', '')
                clean_key2 = clean_key1.replace('"', '')
                opened = 1
                closed = 0
                for j in range(i + 1, len(convert)):
                    if "}" not in convert[j]:
                        if "{" in convert[j]:
                            opened += 1
                        seleccion.append(convert[j])
                    if "}" in convert[j]:
                        closed += 1
                        if opened == closed:
                            i = j + 1
                            break
                        else:
                            seleccion.append(convert[j])
                dicc[clean_key2] = recursive_call(seleccion)
        else:
            i += 1
    return dicc


def normal_value(dicc, line):
    line1 = line.replace('"', '')
    line2 = line1.replace(',', '')
    aux = line2.strip().split(':')
    clean_aux = aux[1].strip()
    if "." in clean_aux and clean_aux[0].isdigit():  # float
        dicc[aux[0]] = float(clean_aux)
    elif clean_aux.isdigit():
        dicc[aux[0]] = int(clean_aux)
    elif clean_aux == "-1":
        dicc[aux[0]] = -1
    else:
        dicc[aux[0]] = clean_aux
    return dicc


def list_value(lista_original):
    new_dicc = {}
    new_key = lista_original[0].split(':')
    clean_key = new_key[0].replace('"', '')
    new_list = []
    j = 1
    while j < len(lista_original):
        if "{" in lista_original[j]:
            new_list = listas_diccionario(lista_original[1:])
            j = len(lista_original)

        else:
            clean_value = lista_original[j].replace('"', '')
            aux = clean_value.strip().replace(',', '')
            clean_aux = aux.strip()
            if "." in clean_aux and clean_aux[0].isdigit():
                new_list.append(float(clean_aux))
            elif clean_aux.isdigit():
                new_list.append(int(clean_aux))
            elif clean_aux == "-1":
                new_list.append(-1)
            else:
                new_list.append(clean_aux)
            j += 1

    new_dicc[clean_key] = new_list
    return new_dicc


def listas_diccionario(content):
    final = []
    i = 0
    inicio = 0
    opened = 0
    close = 0
    while i < len(content):
        if opened != 0 and opened == close:
            final.append(recursive_call(content[inicio:i]))
            opened = 0
            close = 0
            inicio = i
        else:
            if "{" in content[i]:
                opened += 1
            if "}" in content[i]:
                close += 1
            i += 1
    if opened == close:
        final.append(recursive_call(content[inicio:i]))
    return final


def open_file(path):
    clean_lines = []
    with open(path, encoding="utf-8") as json_file:
        for line in json_file.readlines():
            if line != "\n":
                clean_lines.append(line.strip())
    return clean_lines

parser1 = myJsonToDict("datos/programonMoves.json")
parser2 = myJsonToDict("datos/programones.json")
parser3 = myJsonToDict("datos/routes.json")
parser4 = myJsonToDict("datos/moveCategories.json")
parser5 = myJsonToDict("datos/types.json")
parser6 = myJsonToDict("datos/gyms.json")
parser7 = myJsonToDict("datos/infoJugadores.json")


print(parser1)
print(parser2)
print(parser3)
print(parser4)
print(parser5)
print(parser6)
print(parser7)


parser1_original = jsonToDict("datos/programonMoves.json")
parser2_original = jsonToDict("datos/programones.json")
parser3_original = jsonToDict("datos/routes.json")
parser4_original = jsonToDict("datos/moveCategories.json")
parser5_original = jsonToDict("datos/types.json")
parser6_original = jsonToDict("datos/gyms.json")


print(parser1 == parser1_original)
print(parser2 == parser2_original)
print(parser3 == parser3_original)
print(parser4 == parser4_original)
print(parser5 == parser5_original)
print(parser6 == parser6_original)
