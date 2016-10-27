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


if __name__ == "__main__":
    print("{0:9s}|{1:^9s}|{2:^12s}|{3:^9s}|{4:^12s}".format("TOTAL", "PROCESADO",
                                                           "SINPROCESAR",
                                                           "PERCENT",
                                                           "DELTATIME"))

    process_i, iter_i = read_file("Archivo1")
    print("\n\n{0:5s}|{1:^13s}|{2:^13s}".format("PARTE", "PROCESADOS",
                                                "ITERACIONES"))
    print("{0:5s}|{1:^13d}|{2:^13d}".format("I", process_i, iter_i))
    print("{0:5s}|{1:^13d}|{2:^13d}".format("II", 0, 0))