# AC03
import random
from data import *

diccionario = {}
diccionario['sustantivo'] = sustantivos
diccionario['verbos'] = {'verbosN': verbosN, 'verbosV': verbosV}
diccionario['articulo'] = articulos
diccionario['sintagma'] = sintagmas
diccionario['adjetivo'] = adjs
diccionario['adverbio'] = advs

def crear_sujeto(diccionario, complemento_directo=False, palabras_anterior=[]):
    palabras = []
    sustantivo = random.choice(diccionario["sustantivo"])
    while sustantivo in palabras_anterior:
        sustantivo = random.choice(diccionario["sustantivo"])

    articulo = random.choice(diccionario["articulo"])
    while articulo in palabras_anterior:
        articulo = random.choice(diccionario["articulo"])

    palabras.append(articulo)
    palabras.append(sustantivo)

    prob_sintagma = random.randint(1,100)
    azar_sintagma = random.randint(1,100)

    azar_adjetivo = random.randint(1,3)
    if azar_adjetivo == 1:
        adjetivo = random.choice(diccionario["adjetivo"])
        while adjetivo in palabras_anterior:
            adjetivo = random.choice(diccionario["adjetivo"])
        palabras.insert(1, adjetivo)  # antes del sujeto

    if azar_adjetivo == 2:
        adjetivo = random.choice(diccionario["adjetivo"])
        while adjetivo in palabras_anterior:
            adjetivo = random.choice(diccionario["adjetivo"])
        palabras.insert(2, adjetivo)  # despues del sujeto

    if not complemento_directo:
        oracion = articulo[0].upper() + articulo[1:] + " "
        oracion += " ".join(palabras[1:])
    else:
        oracion = " ".join(palabras)

    if azar_sintagma <= prob_sintagma:
        sintagma = random.choice(diccionario["sintagma"])
        while sintagma in palabras_anterior:
            sintagma = random.choice(diccionario["sintagma"])
        oracion += ", {},".format(sintagma)

    return (palabras, oracion)

def crear_predicado(diccionario, palabras_anterior=[]):
    palabras = []
    verbosN = diccionario.get('verbos').get('verbosN')
    verbosV = diccionario.get('verbos').get('verbosV')
    if random.randint(1,2) == 1:
        verbo_n = random.choice(verbosN)
        while verbo_n in palabras_anterior:
            verbo_n = random.choice(verbosN)
        palabras.append(verbo_n)
        all_predicado = predicado(diccionario, 'verbosN')
        palabras.append(all_predicado[0])
        oracion = verbo_n + " " + all_predicado[1]

    else:
        verbo_v = random.choice(verbosV)
        while verbo_v in palabras_anterior:
            verbo_v = random.choice(verbosV)
        palabras.append(verbo_v)
        all_predicado = predicado(diccionario, 'verbosV')
        if all_predicado[0] != "":
            palabras.append(all_predicado[0])
        if all_predicado[1] == ".":
            oracion = verbo_v + all_predicado[1]
        else:
            oracion = verbo_v + " " + all_predicado[1]

    return (palabras, oracion)

def predicado(diccionario, key, palabras_anterior=[]):
    palabras = []
    if 'verbosV' == key:
        ausencia = random.randint(1,2)
        if ausencia == 1:
            return ("", ".")
        else:
            adverbio = random.choice(diccionario['adverbio'])
            while adverbio in palabras_anterior:
                adverbio = random.choice(diccionario['adverbio'])
            palabras.append(adverbio)

            prob_complemento = random.randint(1,2)
            if prob_complemento == 1:
                complemento = crear_sujeto(diccionario, True)[1]
                final = random.randint(1,2)
                if final == 1:
                    palabras.append(complemento)

                else:
                    palabras.insert(0, complemento)

    else:
        adjetivo = random.choice(diccionario['adjetivo'])
        while adjetivo in palabras_anterior:
            adjetivo = random.choice(diccionario['adjetivo'])
        palabras.append(adjetivo)

    unir_palabras = " ".join(palabras)
    if unir_palabras[-1] == ",":
        oracion = unir_palabras[:-1] + "."
    else:
        oracion = unir_palabras + "."
    return (palabras, oracion)

def armar_oracion(diccionario, oraciones):
    used_words = []

    sujeto = crear_sujeto(diccionario)
    predicado = crear_predicado(diccionario)
    used_words.append(sujeto[0] + predicado[0])
    print(sujeto[1] + " " + predicado[1])

    for i in range(1, oraciones):
        sujeto = crear_sujeto(diccionario, False, used_words[i - 1])
        predicado = crear_predicado(diccionario, used_words[i - 1])
        used_words.append(sujeto[0] + predicado[0])
        print(sujeto[1] + " " + predicado[1])

        if (i + 1) % 10 == 0:
            ultimas = []
            k = len(used_words) - 1
            while len(ultimas) < 15:
                anterior = used_words[k]
                while anterior != []:
                    ultimas.append(anterior.pop())
                    if len(ultimas) == 15:
                        break
                k -= 1

            for palabra in ultimas:
                key_aleatoria = random.choice(["sustantivo", "verbos", "articulo", "sintagma", "adjetivo", "adverbio"])
                if key_aleatoria != "verbos":
                    diccionario[key_aleatoria].append(palabra)

oraciones = input("Cantidad de oraciones:")
while not oraciones.isdigit():
    print("Invalido")
    oraciones = input("Cantidad de oraciones:")
armar_oracion(diccionario, int(oraciones))