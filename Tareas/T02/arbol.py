# arbol de jugadas representado por un arbol
from myEDD import MyList


class ArbolJugadas:
    def __init__(self, id_nodo, color=None, number=None, x=None, y=None, id_padre=None):  # caso de bifurcacion inicio
        self.id_nodo = id_nodo
        self.color = color
        self.number = number
        self.x = x
        self.y = y
        self.id_padre = id_padre
        self.hijos = MyList()

    def agregar_nodo(self, id_nodo, color, number, x, y, id_padre=None):
        if self.id_nodo == id_padre:
            self.hijos.append(ArbolJugadas(id_nodo, color, number, x, y, id_padre))

        else:
            for hijo in self.hijos:
                hijo.agregar_nodo(id_nodo, color, number, x, y, id_padre)

    def obtener_nodo(self, id_nodo):
        if self.id_nodo == id_nodo:
            return self
        else:
            for hijo in self.hijos:
                nodo = hijo.obtener_nodo(id_nodo)

                if nodo:
                    return nodo

    def __repr__(self):
        def recorrer_arbol(raiz):
            for hijo in raiz.hijos:
                self.ret += "id-nodo: {} -> id_padre: {} -> color: {} -> numero: {}\n".format(hijo.id_nodo,
                                                                                              hijo.id_padre,
                                                                                              hijo.color,
                                                                                              hijo.number)
                recorrer_arbol(hijo)

            return self

        self.ret = 'RAIZ:\nroot-id: {} -> color: {} -> numero: {}\n\nHIJOS:\n'.format(self.id_nodo, self.color,
                                                                                      self.number)
        recorrer_arbol(self)
        return self.ret


if __name__ == '__main__':
    arbol = ArbolJugadas(0, "black", 0)
    arbol.agregar_nodo(1, "white", 1, 0)
    arbol.agregar_nodo(2, "black", 1, 0)
    arbol.agregar_nodo(3, "black", 2, 1)

    print(arbol)
