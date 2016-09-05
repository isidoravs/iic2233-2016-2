# T02 - Isidora Vizcaya
from gui import MainWindow, run
from tablero import NodeTablero, Tablero
from parserSGF import sgfToTree
from arbol import ArbolJugadas

class GoWindow(MainWindow):
    def __init__(self):
        super().__init__()

        first_node = NodeTablero(0, 0, None, None, None, None)
        self.tablero = Tablero(first_node)
        self.tablero.set_tablero(19, 19)

        self.setWindowTitle("GO")
        self.show_message("Jugador Negro comienza la partida")
        self.turn = "black"
        self.jugada = 1
        self.arbol = ArbolJugadas(0)
        self.id_nodo_prox = 1
        self.depth = 0

    def on_piece_click(self, letter, y):  # funciona para el caso lineal
        if self.tablero.add_piece(letter, y - 1, self.jugada, self.turn):
            self.add_piece(letter, y, self.jugada, self.turn)

            x = self.tablero.abc.find(letter)
            # esto se debe cambiar para variaciones RR (depth)
            # opcion A: si cambia depth, llame a set_arbol_jugadas(self) y ajustar parametros
            self.arbol.agregar_nodo(self.id_nodo_prox, self.turn, self.jugada, self.depth, x, y, self.id_nodo_prox - 1)
            self.add_point(self.jugada, self.depth, self.jugada, self.turn)
            self.add_line((self.jugada - 1, self.depth), (self.jugada, self.depth), "black")
            self.jugada += 1
            self.id_nodo_prox += 1

            if self.turn == "black":
                self.turn = "white"
            else:
                self.turn = "black"
            self.show_message("Added {},{}".format(letter, y))

        else:
            self.show_message("Invalid position: {},{}".format(letter, y))
        return

    def on_point_click(self, x, y):
        self.remove_point(x, y)

    def on_open_click(self, path):
        if path[-4:] != ".sgf":
            self.show_message("Archivo invalido, debe tener extension .sgf")
        else:
            arbol_jugadas = sgfToTree(path)
            self.set_arbol_jugadas(arbol_jugadas)
        return

    def set_arbol_jugadas(self, arbol_jugadas, i_anterior=0, j_anterior=0):
        if arbol_jugadas.color is not None:  # deja el espacio a bifurcacion inicial
            self.add_point(arbol_jugadas.number, arbol_jugadas.depth, arbol_jugadas.number, arbol_jugadas.color)
            self.add_line((i_anterior, j_anterior), (arbol_jugadas.number, arbol_jugadas.depth), "black")

        for hijo in arbol_jugadas.hijos:
            self.set_arbol_jugadas(hijo, arbol_jugadas.number, arbol_jugadas.depth)
        return

    def on_save_click(self, path):
        print(path)

    def on_pass_click(self):
        self.remove_line((6, 2), (5, 1))
        print("pass")

    def on_count_click(self):
        print("count")

    def on_resign_click(self):
        print("resign")


if __name__ == '__main__':
    run(GoWindow())
