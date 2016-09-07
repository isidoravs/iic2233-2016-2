# T02 - Isidora Vizcaya
from gui import MainWindow, run
from tablero import NodeTablero, Tablero
from parserSGF import sgfToTree
from arbol import ArbolJugadas
from myEDD import MyList


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
        self.max_depth = 0  # determina numero de variaciones
        self.id_nodo_prox = 1  # nunca reinicia porque es unico
        self.depth = 0
        self.pass_seguidos = 0

        self.seleccion_valida = True  # para comenzar luego de abrir un archivo
        self.end_game = False
        self.new_variation = False  # para crear variaciones en el arbol
        self.actual_node = None
        self.tablero_pasado = MyList()  # determina juegos pasados, listas con nodos
        self.dead_pieces = None  # utilizada al hacer count

    def on_piece_click(self, letter, y):
        if not self.seleccion_valida:  # en caso de que deba escoger un nodo del arbol
            self.show_message("Presiona un nodo en el arbol para continuar esa partida")
            return

        if self.dead_pieces is not None:  # esta seleccionando piezas para eliminar
            for nodo_grafo in self.tablero.nodes:
                x = self.tablero.abc.find(letter)
                if nodo_grafo.x_pos == x and nodo_grafo.y_pos == y - 1:
                    if nodo_grafo.piece:
                        selected_node = nodo_grafo
                        break
                    else:
                        self.show_message("Seleccione una piedra del tablero")
                        return

            # establecer grupo
            self.tablero.one_group.append(selected_node)
            self.tablero.set_grupo(selected_node)

            for nodo in self.tablero.one_group:
                # marco las piedras
                new_letter = self.tablero.abc[nodo.x_pos]
                self.remove_piece(new_letter, nodo.y_pos + 1)
                self.add_piece(new_letter, nodo.y_pos + 1, "X", nodo.color)
                if nodo not in self.dead_pieces:
                    self.dead_pieces.append(nodo)

            self.tablero.one_group = MyList()
            return

        if self.end_game:  # en caso de haber terminado la partida
            self.show_message("La partida ha terminado, solo puedes analizar las jugadas anteriores")
            return

        if self.tablero.add_piece(letter, y - 1, self.jugada, self.turn):
            self.add_piece(letter, y, self.jugada, self.turn)

            if self.tablero.to_remove is not None:  # pieza agregada capturo a otras
                for grupo in self.tablero.to_remove:
                    for coordenada in grupo:
                        letter = coordenada[0]
                        y = coordenada[1] + 1
                        self.remove_piece(letter, y)
                self.tablero.to_remove = None

            if self.new_variation:  # debe determinar si crea una nueva variacion
                divergencia = True
                for hijo in self.actual_node.hijos:
                    if self.tablero.abc[hijo.x] == letter and hijo.y == y:  # no diverge
                        divergencia = False
                        self.actual_node = hijo  # ya va a estar el nodo en el tablero
                        break

                if divergencia:
                    self.set_variation(letter, y)
                    self.new_variation = False

                else:
                    self.jugada += 1
                    self.id_nodo_prox += 1

                    if self.turn == "black":
                        self.turn = "white"
                    else:
                        self.turn = "black"
                    self.show_message("Added {},{}".format(letter, y))

                    if self.pass_seguidos == 1:
                        self.pass_seguidos = 0
                return

            # actualiza el arbol
            x = self.tablero.abc.find(letter)
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

            # reinicia la cuenta de pasos
            if self.pass_seguidos == 1:
                self.pass_seguidos = 0

        else:
            self.show_message("Invalid position: {},{} (already occupied or suicide)".format(letter, y))
        return

    def on_point_click(self, i, j):
        if self.dead_pieces is not None:
            self.show_message("Antes de analizar el juego, seleccione piedras muertas a eliminar.")
            return

        point = self.arbol.obtener_point(i, j)

        if not self.seleccion_valida:
            self.seleccion_valida = True
            if point.color == "black":
                next_color = "Blanco"
            else:
                next_color = "Negro"
            self.show_message("Perfecto! Es el turno del jugador {}".format(next_color))

        # actualiza las piezas del tablero
        self.show_tablero_pasado(point)

        # condiciones siguiente jugada (point es el ultimo)
        self.depth = point.depth
        self.jugada = point.number + 1
        if point.color == "black":
            self.turn = "white"
        else:
            self.turn = "black"
        self.actual_node = point

        self.new_variation = True  # ayuda a determinar cuando las jugadas divergen

        return

    def show_tablero_pasado(self, point):
        def set_jugadas_pasadas(point, go):
            if point.id_padre is None:
                return

            else:
                padre = go.arbol.obtener_padre(point.id_padre, go)
                go.tablero_pasado.append(padre)
                return set_jugadas_pasadas(padre, go)

        # coordenadas de todas las jugadas anteriores a ese punto
        self.tablero_pasado.append(point)
        set_jugadas_pasadas(point, self)

        # reinicio de condiciones
        self.turn = "black"
        self.pass_seguidos = 0
        self.jugada = 1
        # eliminar valores grafos del tablero
        for nodo_grafo in self.tablero.nodes:  # no es muy eficiente pero evita problemas
            if nodo_grafo.piece:
                self.remove_piece(self.tablero.abc[nodo_grafo.x_pos], nodo_grafo.y_pos + 1)
                nodo_grafo.piece = False
                nodo_grafo.value = None
                nodo_grafo.color = None

        # simular jugadas anteriores
        to_recreate = MyList()
        i = len(self.tablero_pasado) - 1
        while i >= 0:
            to_recreate.append(self.tablero_pasado[i])
            i -= 1

        self.tablero_pasado = MyList()

        for nodo_grafo in self.tablero.nodes:
            for nodo_pasado in to_recreate:
                if nodo_grafo.x_pos == nodo_pasado.x and nodo_grafo.y_pos == nodo_pasado.y - 1:
                    self.simular_jugadas_pasada(self.tablero.abc[nodo_pasado.x], nodo_pasado.y,
                                                nodo_pasado.number, nodo_pasado.color)
                    break

        return

    def simular_jugadas_pasada(self, letter, y, text, color):  # falla al agregar la pieza que captura RR
        if self.tablero.add_piece(letter, y - 1, text, color):
            self.add_piece(letter, y, text, color)

            if self.tablero.to_remove is not None:
                for grupo in self.tablero.to_remove:
                    for coordenada in grupo:
                        letter_r = coordenada[0]
                        y_r = coordenada[1] + 1
                        self.remove_piece(letter_r, y_r)
                self.tablero.to_remove = None

            self.jugada += 1
            if self.turn == "black":
                self.turn = "white"
            else:
                self.turn = "black"

        return

    def set_variation(self, letter, y):
        if self.depth < self.max_depth:  # en caso de que la variacion no ocurra al fondo
            # borrar nodos del arbol en la interfaz
            self.clear_arbol(self.arbol)

            # altero el depth de los nodos
            self.arbol.actualizar_depth(self.arbol, self.depth)
            self.set_arbol_jugadas(self.arbol)

        self.depth += 1
        self.max_depth += 1

        x = self.tablero.abc.find(letter)
        self.arbol.agregar_nodo(self.id_nodo_prox, self.turn, self.jugada, self.depth, x, y, self.actual_node.id_nodo)
        self.add_point(self.jugada, self.depth, self.jugada, self.turn)
        self.add_line((self.actual_node.number, self.actual_node.depth), (self.jugada, self.depth), "black")
        self.jugada += 1
        self.id_nodo_prox += 1

        if self.turn == "black":
            self.turn = "white"
        else:
            self.turn = "black"
        self.show_message("Added {},{}".format(letter, y))

        if self.pass_seguidos == 1:
            self.pass_seguidos = 0

        return

    def on_open_click(self, path):
        if self.dead_pieces is not None:
            self.show_message("Debe seleccionar las piedras muertas a eliminar")
            return

        if path[-4:] != ".sgf":
            self.show_message("Archivo invalido, debe tener extension .sgf")
        else:
            arbol_jugadas = sgfToTree(path)

            if len(self.arbol.hijos) != 0:
                # elimino puntos anteriores
                self.clear_arbol(self.arbol)

            # establezco el nuevo arbol
            self.arbol = arbol_jugadas
            self.set_arbol_jugadas(arbol_jugadas)
            self.arbol.get_max_depth(arbol_jugadas, self)

            self.seleccion_valida = False
            self.show_message("Presiona un nodo en el arbol para continuar esa partida")

        return

    def set_arbol_jugadas(self, arbol_jugadas, i_anterior=0, j_anterior=0):
        if arbol_jugadas.color is not None:  # deja el espacio a bifurcacion inicial
            self.add_point(arbol_jugadas.number, arbol_jugadas.depth, arbol_jugadas.number, arbol_jugadas.color)
            self.add_line((i_anterior, j_anterior), (arbol_jugadas.number, arbol_jugadas.depth), "black")

        for hijo in arbol_jugadas.hijos:
            self.set_arbol_jugadas(hijo, arbol_jugadas.number, arbol_jugadas.depth)

        return

    def clear_arbol(self, raiz):
        for hijo in raiz.hijos:
            self.remove_point(hijo.number, hijo.depth)
            self.remove_line((raiz.number, raiz.depth), (hijo.number, hijo.depth))
            self.clear_arbol(hijo)

        return self

    def on_save_click(self, path):
        if self.dead_pieces is not None:
            self.show_message("Debe seleccionar las piedras muertas a remover antes de guardar.")
            return

        return

    def on_pass_click(self):
        self.pass_seguidos += 1
        if self.pass_seguidos == 2:
            self.end_game = True
            self.show_message("Jugadores pasan consecutivamente. Seleccione piedras muertas a remover.")
            self.dead_pieces = MyList()

        else:
            self.arbol.agregar_nodo(self.id_nodo_prox, self.turn, self.jugada, self.depth,
                                    None, None, self.id_nodo_prox - 1)
            self.add_point(self.jugada, self.depth, self.jugada, self.turn)
            self.add_line((self.jugada - 1, self.depth), (self.jugada, self.depth), "black")

            self.jugada += 1
            self.id_nodo_prox += 1

            if self.turn == "black":
                self.turn = "white"
            else:
                self.turn = "black"
            self.show_message("Jugador ha pasado")
        return

    def on_count_click(self):
        if self.dead_pieces is None:
            self.show_message("La opcion 'COUNT' no es valida en este momento.")
            return

        # remover piedras
        for nodo_grafo in self.dead_pieces:
            nodo_grafo.piece = False
            nodo_grafo.color = None
            nodo_grafo.value = None

            letter = self.tablero.abc[nodo_grafo.x_pos]
            self.remove_piece(letter, nodo_grafo.y_pos + 1)

        self.show_message("Se han eliminado las piedras muertas.")

        # contar territorio RR
        return

    def on_resign_click(self):
        if self.turn == "black":
            self.set_result("W + res")

        else:
            self.set_result("B + res")
        self.end_game = True
        self.show_message("Fin del juego")

        return


if __name__ == '__main__':
    run(GoWindow())
