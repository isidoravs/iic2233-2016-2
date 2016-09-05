# arbol de jugadas representado por un arbol
from myEDD import MyList


class ArbolJugadas:
    def __init__(self, id_nodo, color=None, number=0, depth=0, x=None, y=None, id_padre=None):
        self.id_nodo = id_nodo
        self.color = color
        self.number = number  # corresponde al numero de jugada (independiente si pasa) y coordenada i
        self.depth = depth # coordenada j
        self.x = x
        self.y = y
        self.id_padre = id_padre
        self.hijos = MyList()

    def agregar_nodo(self, id_nodo, color, number, depth, x, y, id_padre=None):
        if self.id_nodo == id_padre:
            self.hijos.append(ArbolJugadas(id_nodo, color, number, depth, x, y, id_padre))

        else:
            for hijo in self.hijos:
                hijo.agregar_nodo(id_nodo, color, number, depth, x, y, id_padre)

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
                self.ret += "id-nodo: {} -> id_padre: {} -> color: {} -> numero: {} -> depth: {}\n".format(hijo.id_nodo,
                                                                                              hijo.id_padre,
                                                                                              hijo.color,
                                                                                              hijo.number, hijo.depth)
                recorrer_arbol(hijo)

            return self

        self.ret = 'RAIZ:\nroot-id: {} -> color: {} -> numero: {}\n\nHIJOS:\n'.format(self.id_nodo, self.color,
                                                                                      self.number)
        recorrer_arbol(self)
        return self.ret


if __name__ == '__main__':
    print("Module being run diectly")
