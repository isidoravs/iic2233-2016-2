# tablero es representado por un grafo
from myEDD import MyList


class NodeTablero:
    def __init__(self, x_pos, y_pos, link_up, link_down, link_right, link_left, color=None, value=None, piece=None):
        self.color = color  # black / white
        self.x_pos = x_pos  # coordenada x (como numero)
        self.y_pos = y_pos
        self.up = link_up  # None si es un borde
        self.down = link_down
        self.right = link_right
        self.left = link_left
        self.value = value  # Determina el numero de la pieza (piedra)
        self.piece = piece  # True si es una pieza, False si es un cuadrado de territorio, None si es vacio

    def __repr__(self):
        return self.color


class Tablero:  # grafo no dirigido
    def __init__(self, node):
        self.root = node
        self.nodes = MyList(node)
        self.actual_node = node
        self.abc = "ABCDEFGHJKLMNOPQRST"

    def set_tablero(self, filas, columnas):  # tablero poblado de NodoTablero, solo cambiar atributos al jugar
        for i in range(filas):
            for j in range(columnas):  # (j, i)
                if i == 0 and j == 0:
                    pass

                else:
                    if i == 0 or i == filas - 1:
                        if i == 0:
                            link_up = None
                            link_down = self.get_node_position(j,  + 1)
                        else:
                            link_down = None
                            link_up = self.get_node_position(j, i - 1)
                    else:
                        link_up = self.get_node_position(j, i - 1)
                        link_down = self.get_node_position(j, i + 1)

                    if j == 0 or j == columnas - 1:
                        if j == 0:
                            link_left = None
                            link_right = self.get_node_position(j + 1, i)
                        else:
                            link_right = None
                            link_left = self.get_node_position(j - 1, i)
                    else:
                        link_left = self.get_node_position(j - 1, i)
                        link_right = self.get_node_position(j + 1, i)

                    new_node = NodeTablero(i, j, link_up, link_down, link_right, link_left)
                    self.nodes.append(new_node)
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

        if selected_node.piece is None:  # es un espacio vacio del tablero
            selected_node.piece = True
            selected_node.value = text
            selected_node.color = color
            return True
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


if __name__ == "__main__":
    first_node = NodeTablero(0, 0, None, None, None, None)
    tablero = Tablero(first_node)
    tablero.set_tablero(4, 4)
