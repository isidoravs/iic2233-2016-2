# tablero es representado por un grafo
from myEDD import MyList


class NodeTablero:
    def __init__(self, x_pos, y_pos, link_up, link_down, link_right, link_left, color=None, value=None, piece=False):
        self.color = color  # black / white
        self.x_pos = x_pos  # coordenada x (como numero)
        self.y_pos = y_pos
        self.up = link_up  # None si es un borde, -1 si no está definido
        self.down = link_down
        self.right = link_right
        self.left = link_left
        self.value = value  # Determina el numero de la pieza (piedra)
        self.piece = piece  # True si es una pieza, False si es vacio
        self.square = False  # cambia a True si es un cuadrado de territorio
        self.libertades = 0

    def __repr__(self):
        if self.up is None or self.down is None or self.right is None or self.left is None:
            return "({},{}), esta en un borde".format(self.x_pos, self.y_pos)

        else:
            return "({},{})\n -> UP: ({},{}), DOWN: ({},{}), LEFT: ({},{}), RIGHT: ({},{})\n" \
                   "".format(self.x_pos, self.y_pos, self.up.x_pos, self.up.y_pos, self.down.x_pos,
                             self.down.y_pos, self.left.x_pos, self.left.y_pos, self.right.x_pos, self.right.y_pos)


class Tablero:  # grafo no dirigido
    def __init__(self, node):
        self.root = node
        self.nodes = MyList(node)
        self.actual_node = node
        self.abc = "ABCDEFGHJKLMNOPQRST"
        self.prisioneros_white = 0
        self.prisioneros_black = 0
        self.to_remove = None  # guarda piezas pendientes por eliminar de la interfaz
        self.one_group = MyList()  # atributo temporal para analizar un grupo a la vez

    def set_tablero(self, filas, columnas):  # tablero poblado de NodoTablero, solo cambiar atributos al jugar
        for i in range(filas):
            for j in range(columnas):  # (j, i)
                # luego arreglar link down y right
                if i == 0 and j == 0:
                    self.actual_node.right = -1
                    self.actual_node.down = -1

                else:
                    if i == 0 or i == filas - 1:
                        if i == 0:
                            link_up = None
                            link_down = -1
                        else:
                            link_down = None
                            link_up = self.get_node_position(j, i - 1)
                    else:
                        link_up = self.get_node_position(j, i - 1)
                        link_down = -1

                    if j == 0 or j == columnas - 1:
                        if j == 0:
                            link_left = None
                            link_right = -1
                        else:
                            link_right = None
                            link_left = self.get_node_position(j - 1, i)
                    else:
                        link_left = self.get_node_position(j - 1, i)
                        link_right = -1

                    new_node = NodeTablero(j, i, link_up, link_down, link_right, link_left)
                    self.nodes.append(new_node)

        # ahora reviso que todos tengan conexion
        for node in self.nodes:
            if node.up == -1:
                for other_node in self.nodes:
                    if other_node.y_pos == node.y_pos - 1 and other_node.x_pos == node.x_pos:
                        node.up = other_node
                        break

            if node.down == -1:
                for other_node in self.nodes:
                    if other_node.y_pos == node.y_pos + 1 and other_node.x_pos == node.x_pos:
                        node.down = other_node
                        break

            if node.right == -1:
                for other_node in self.nodes:
                    if other_node.x_pos == node.x_pos + 1 and other_node.y_pos == node.y_pos:
                        node.right = other_node
                        break

            if node.left == -1:
                for other_node in self.nodes:
                    if other_node.x_pos == node.x_pos - 1 and other_node.y_pos == node.y_pos:
                        node.left = other_node
                        break
        return

    def get_node_position(self, x, y):
        for node in self.nodes:  # node de la clase Node y su valor es
            if node.x_pos == x and node.y_pos == y:
                return node
        return None

    def add_piece(self, letter, y, text, color):
        # comienzo con los metodos de Duck Typing (metodos del tablero y window)
        x = self.abc.find(letter)
        selected_node = None

        for node in self.nodes:
            if node.x_pos == x and node.y_pos == y:
                selected_node = node
                break

        if not selected_node.piece:  # es un espacio vacio del tablero
            selected_node.piece = True
            selected_node.value = text
            selected_node.color = color
            valido = self.actualizar_libertades(selected_node)
            if valido:
                return True
            else:
                selected_node.piece = False
                selected_node.value = None
                selected_node.color = None
                return False
        else:
            return False

    def add_square(self, letter, y, color):
        x = self.abc.find(letter)
        selected_node = None

        for node in self.nodes:
            if node.x_pos == x and node.y_pos == y:
                selected_node = node
                break

        if selected_node.piece is None:  # es un espacio vacio del tablero
            selected_node.piece = False
            selected_node.value = None
            selected_node.color = color
        else:
            print("Lugar inválido para agregar un cuadrado de territorio")
        return

    def remove_piece(self, letter, y):
        x = self.abc.find(letter)
        selected_node = None

        for node in self.nodes:
            if node.x_pos == x and node.y_pos == y:
                selected_node = node
                break

        if selected_node.piece is not None:  # es un espacio no vacio del tablero
            # cambio atributos del nodo de modo que sea vacio
            selected_node.piece = None
            selected_node.value = None
            selected_node.color = None
        else:
            print("Lugar inválido para quitar un cuadrado o pieza")
        return

    def actualizar_libertades(self, node):
        nodos_contrarios = MyList()  # lista con los nodos de color contrario juntos al nodo recien agregado
        rodeo_enemigo = 0

        if node.up is None:
            rodeo_enemigo += 1
        else:
            if node.up.piece:  # es una pieza
                if node.up.color != node.color:
                    rodeo_enemigo += 1
                    nodos_contrarios.append(node.up)

        if node.down is None:
            rodeo_enemigo += 1
        else:
            if node.down.piece:
                if node.down.color != node.color:
                    rodeo_enemigo += 1
                    nodos_contrarios.append(node.down)

        if node.right is None:
            rodeo_enemigo += 1
        else:
            if node.right.piece:
                if node.right.color != node.color:
                    rodeo_enemigo += 1
                    nodos_contrarios.append(node.right)

        if node.left is None:
            rodeo_enemigo += 1
        else:
            if node.left.piece:
                if node.left.color != node.color:
                    rodeo_enemigo += 1
                    nodos_contrarios.append(node.left)

        remove_pieces = self.revisar_captura(nodos_contrarios)  # revisa si hay captura

        if remove_pieces is not None:  # hay captura
            self.to_remove = remove_pieces
            return True

        else:
            self.set_grupo(node)
            if len(self.one_group) > 0:
                libertades = 0
                for nodo in self.one_group:
                    if nodo.up is not None and not nodo.up.piece:
                        libertades += 1

                    if nodo.down is not None and not nodo.down.piece:
                        libertades += 1

                    if nodo.right is not None and not nodo.right.piece:
                        libertades += 1

                    if nodo.left is not None and not nodo.left.piece:
                        libertades += 1

                self.one_group = MyList()
                if libertades == 0:  # jugada suicida
                    return False

            if rodeo_enemigo == 4:  # jugada suicida
                return False

            else:
                return True  # jugada comun y corriente

    def revisar_captura(self, nodos_contrarios):  # retorna lista con piezas a eliminar o None si no se captura
        grupos_nodos = MyList()  # lista con grupos unicos (en caso de que la pieza alcance mas de un grupo)

        for i in range(len(nodos_contrarios)):
            # revisar que no pertenezcan al mismo grupo
            if i == 0:
                self.one_group.append(nodos_contrarios[i])
                self.set_grupo(nodos_contrarios[i])
                grupos_nodos.append([nodo for nodo in self.one_group])
                self.one_group = MyList()
            else:
                nodo_unico = True
                for grupo in grupos_nodos:
                    if nodos_contrarios[i] in grupo:
                        nodo_unico = False
                        break
                if nodo_unico:
                    self.one_group.append(nodos_contrarios[i])
                    self.set_grupo(nodos_contrarios[i])
                    grupos_nodos.append([nodo for nodo in self.one_group])
                    self.one_group = MyList()

        all_removes = MyList()
        remove_pieces = MyList()  # lista de listas con las coordenadas de las piezas a eliminar

        for grupo_nodo in grupos_nodos:
            grupo_capturado = True
            for integrante in grupo_nodo:
                if integrante.up is not None and integrante.up.color is None:  # hay libertades
                    grupo_capturado = False
                    break

                if integrante.down is not None and integrante.down.color is None:  # hay libertades
                    grupo_capturado = False
                    break

                if integrante.right is not None and integrante.right.color is None:  # hay libertades
                    grupo_capturado = False
                    break

                if integrante.left is not None and integrante.left.color is None:  # hay libertades
                    grupo_capturado = False
                    break

            if grupo_capturado:
                for integrante in grupo_nodo:
                    integrante.piece = False
                    integrante.color = None
                    integrante.value = None
                    remove_pieces.append(MyList(self.abc[integrante.x_pos], integrante.y_pos))  # coordenadas

                prisioneros = len(grupo_nodo)
                if nodos_contrarios[0].color == "black":
                    self.prisioneros_white += prisioneros
                else:
                    self.prisioneros_black += prisioneros

            if len(remove_pieces) > 0:
                all_removes.append(remove_pieces)

        if len(all_removes) > 0:
            return all_removes
        else:
            return None

    def set_grupo(self, nodo):
        contorno = self.revisar_contorno(nodo)

        to_check = MyList()
        for elem in contorno:
            if elem not in self.one_group:
                self.one_group.append(elem)
                to_check.append(elem)

        if len(to_check) > 0:
            for nodo in to_check:
                return self.set_grupo(nodo)

        else:
            return

    def revisar_contorno(self, nodo):  # retorna lista con nodos del mismo color adyacentes al nodo
        contorno = MyList()

        if nodo.up is not None and nodo.up.color == nodo.color:
            contorno.append(nodo.up)

        if nodo.down is not None and nodo.down.color == nodo.color:
            contorno.append(nodo.down)

        if nodo.right is not None and nodo.right.color == nodo.color:
            contorno.append(nodo.right)

        if nodo.left is not None and nodo.left.color == nodo.color:
            contorno.append(nodo.left)

        return contorno


if __name__ == "__main__":
    first_node = NodeTablero(0, 0, None, None, None, None)
    tablero = Tablero(first_node)
    tablero.set_tablero(5, 5)
    tablero.nodes[1].color = "black"
    tablero.nodes[2].color = "black"
    tablero.nodes[7].color = "black"
