#myJsonToDict v.2
from jsonReader import jsonToDict


def myJsonToDict(path):
    lines = open_file(path)
    if "[" in lines[0] and "]" in lines[-1]:  # lista con diccionarios
        final = []
        content = lines[1:-1]
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
                    for j in range(i, len(convert)): ##ACA
                        if "]" not in convert[j]:
                            seleccion.append(convert[j])
                        else:
                            i = j + 1
                            break
                    dicc.update(list_value(dicc, seleccion))

            elif "{" in convert[i]:
                seleccion = []
                new_key = convert[i].split(':')
                clean_key1 = new_key[0].replace(',', '')
                clean_key2 = clean_key1.replace('"', '')
                for j in range(i + 1, len(convert)):
                    if "}" not in convert[j]:
                        seleccion.append(convert[j])
                    else:
                        i = j + 1
                        break
                dicc[clean_key2] = dicc_value(seleccion)
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
    else:
        dicc[aux[0]] = clean_aux
    return dicc

def list_value(dicc, lista_original):
    new_dicc = {}
    new_key = lista_original[0].split(':')
    clean_key = new_key[0].replace('"', '')
    new_list = []
    j = 1
    while j < len(lista_original):
        if "{" in lista_original[j]:
            seleccion = []
            for k in range(j + 1, len(lista_original)):
                if "}" not in lista_original[k]:
                    seleccion.append(lista_original[k])
                else:
                    j = k + 1
                    break
            new_list.append(dicc_value(seleccion))

        else:
            clean_value = lista_original[j].replace('"', '')
            aux = clean_value.strip().replace(',', '')
            clean_aux = aux.strip()
            if "." in clean_aux and clean_aux[0].isdigit():
                new_list.append(float(clean_aux))
            elif clean_aux.isdigit():
                new_list.append(int(clean_aux))
            else:
                new_list.append(clean_aux)
            j += 1

    new_dicc[clean_key] = new_list
    return new_dicc

def dicc_value(lista_original):
    new_dicc = {}
    j = 0
    while j < len(lista_original):
        if "{" in lista_original[j]:
            seleccion = []
            new_key = lista_original[j].split(':')
            clean_key1 = new_key[0].replace(',', '')
            clean_key2 = clean_key1.replace('"', '')
            for k in range(j + 1, len(lista_original)):
                if "}" not in lista_original[k]:
                    seleccion.append(lista_original[k])
                else:
                    j = k + 1
                    break
            new_dicc[clean_key2] = dicc_value(seleccion)

        elif "[" in lista_original[j]:
            seleccion = []
            for k in range(j, len(lista_original)):
                if "]" not in lista_original[k]:
                    seleccion.append(lista_original[k])
                else:
                    j = k + 1
                    break
            new_dicc.update(list_value(new_dicc, seleccion))

        elif "]" not in lista_original[j]:
            line1 = lista_original[j].replace('"', '')
            line2 = line1.strip().replace(',', '')
            aux = line2.strip().split(":")
            clean_aux = aux[1].strip() ## ACA
            if "." in clean_aux and clean_aux[0].isdigit():
                new_dicc[aux[0]] = float(clean_aux)
            elif clean_aux.isdigit():
                new_dicc[aux[0]] = int(clean_aux)
            else:
                new_dicc[aux[0]] = clean_aux
            j += 1
        else:
            j += 1
    return new_dicc

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
# parser6 = myJsonToDict("datos/gyms.json")
# parser7 = myJsonToDict("datos/infoJugadores.json")


print(parser1)
print(parser2)
print(parser3)
print(parser4)
print(parser5)
# print(parser6)
# print(parser7)

parser1_original = jsonToDict("datos/programonMoves.json")
parser2_original = jsonToDict("datos/programones.json")
parser3_original = jsonToDict("datos/routes.json")
parser4_original = jsonToDict("datos/moveCategories.json")
parser5_original = jsonToDict("datos/types.json")

print(parser1 == parser1_original)
print(parser2 == parser2_original)
print(parser3 == parser3_original)
print(parser4 == parser4_original)
print(parser5 == parser5_original)



