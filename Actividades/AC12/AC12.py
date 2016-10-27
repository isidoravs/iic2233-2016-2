# AC12
import time
import os


# Parte 1
def fib(n):
    if n < 2:
        return n
    return fib(n - 2) + fib(n - 1)

def read_file(path):
    with open(path, 'rb') as file:
        all_size = os.path.getsize(path)
        process = 0
        print("{0: <9d}|{1: ^9d}|{2: ^12d}|{3: >8.2f}%|{4: ^1.8f}".format(
            all_size, 0, all_size, 0.00, time.clock()))

        output = open("salida.pdf", "wb")
        i = 1
        while True:
            to_write = file.read(fib(i))
            if to_write == b"":
                break
            output.write(bytearray(to_write)[::-1])
            i += 1

            process += len(to_write)
            print("{0: <9d}|{1: ^9d}|{2: ^12d}|{3: >8.2f}%|{4: ^1.8f}".format(
                all_size,
                process, all_size - process,
                (process / all_size) * 100, time.clock()))
        output.close()
        return process, i - 1

def divisores(numero):
    i=1
    lista=list()
    while i <= numero:
        if numero % i == 0:
            lista.append(i)
        i+=1
    return lista

def numeros_abundantes(numero):
    abundantes = list()
    i = 0
    while numero > len(abundantes):
        lista = divisores(i)
        suma=0
        for k in lista:
            suma+=k
        if suma > 2*i:
            abundantes.append(i)
        i+=1
    return abundantes[numero-1]

def parte_dos(path):
    with open(path, "rb") as file:
        total=bytearray(file.read())
        all_size = len(total)
        suma=0

        for i in range(os.path.getsize(path)-1):
            #print("i",i)
            suma+=total[i]
            #caracter=i.decode("UTF-8")
           # suma+=ord(caracter)

        byte_total=bytearray()
        for i in range(os.path.getsize(path) - 1):
            # print("i",i)
            byte_original=(total[i]+suma) % 256

            byte_total.extend(bytearray(byte_original))
            #with open("resultado","a") as result:
             #   result.write(byte_original.encode())

        archivo_uno=bytearray()
        archivo_dos=bytearray()
        procesados=0
        num_ab=1

        print("{0: <9d}|{1: ^9d}|{2: ^12d}|{3: >8.2f}%|{4: ^1.8f}".format(
            all_size, 0, all_size, 0.00, time.clock()))

        while procesados < len(byte_total):
            archivo_uno.extend(byte_total[:numeros_abundantes(num_ab)])
            archivo_dos.extend(byte_total[:numeros_abundantes(num_ab)])
            num_ab+=1
            procesados+=numeros_abundantes(num_ab)

            print("{0: <9d}|{1: ^9d}|{2: ^12d}|{3: >8.2f}%|{4: ^1.8f}".format(
                all_size,
                procesados, all_size - procesados,
                (procesados / all_size) * 100, time.clock()))

            if (procesados / all_size) * 100 > 100:
                break

        with open('archivo_1.mp3', 'wb') as arc_uno:
            arc_uno.write(bytearray(archivo_uno))
        with open('archivo_2.gif', 'wb') as arc_uno:
            arc_uno.write(bytearray(archivo_uno))

        return procesados, num_ab



if __name__ == "__main__":
    print("PARTE I")
    print("{0:9s}|{1:^9s}|{2:^12s}|{3:^9s}|{4:^12s}".format("TOTAL", "PROCESADO",
                                                           "SINPROCESAR",
                                                           "PERCENT",
                                                           "DELTATIME"))



    process_i, iter_i = read_file("Archivo1")

    print("\nPARTE II")
    print(
        "{0:9s}|{1:^9s}|{2:^12s}|{3:^9s}|{4:^12s}".format("TOTAL", "PROCESADO",
                                                          "SINPROCESAR",
                                                          "PERCENT",
                                                          "DELTATIME"))
    process_ii, iter_ii = parte_dos("salida.pdf")


    # resumen
    print("\n\n{0:5s}|{1:^13s}|{2:^13s}".format("PARTE", "PROCESADOS",
                                                "ITERACIONES"))
    print("{0:5s}|{1:^13d}|{2:^13d}".format("I", process_i, iter_i))
    print("{0:5s}|{1:^13d}|{2:^13d}".format("II", process_ii, iter_ii))