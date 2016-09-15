from myEDD import MyList


class ArbolJugadas:
    def __init__(self, id_nodo, color=None, number=0, depth=0, x=None, y=None, id_padre=None, resumen="X"*361):
        self.id_nodo = id_nodo
        self.color = color
        self.number = number  # corresponde al numero de jugada (independiente si pasa) y coordenada i
        self.depth = depth  # coordenada j
        self.x = x  # indice de tablero.abc
        self.y = y  # numero del tablero
        self.id_padre = id_padre
        self.hijos = MyList()
        self.resumen = resumen  # resumen del estado del tablero en el momento de agregarlo

    def agregar_nodo(self, id_nodo, color, number, depth, x, y, id_padre=None, resumen=""):
        if self.id_nodo == id_padre:
            self.hijos.append(ArbolJugadas(id_nodo, color, number, depth, x, y, id_padre, resumen))

        else:
            for hijo in self.hijos:
                hijo.agregar_nodo(id_nodo, color, number, depth, x, y, id_padre, resumen)

    def obtener_nodo(self, id_nodo):
        if self.id_nodo == id_nodo:
            return self
        else:
            for hijo in self.hijos:
                nodo = hijo.obtener_nodo(id_nodo)

                if nodo:
                    return nodo

    def obtener_padre(self, id_padre, go=None):
        if self.id_nodo == id_padre:
            return self
        else:
            for hijo in self.hijos:
                nodo = hijo.obtener_padre(id_padre, go)

                if nodo:
                    return nodo

    def obtener_point(self, i, j):
        if self.number == i and self.depth == j:
            return self
        else:
            for hijo in self.hijos:
                nodo = hijo.obtener_point(i, j)

                if nodo:
                    return nodo

    def obtener_resumen(self, resumen):
        if self.resumen == resumen:
            return self
        else:
            for hijo in self.hijos:
                nodo = hijo.obtener_resumen(resumen)

                if nodo:
                    return nodo

    def get_max_depth(self, raiz, go):
        for hijo in raiz.hijos:
            if hijo.depth > go.max_depth:
                go.max_depth = hijo.depth
            self.get_max_depth(hijo, go)

        return self

    def actualizar_depth(self, raiz, limite):  # limite es el depth en donde ocurre la variacion
        for hijo in raiz.hijos:
            if hijo.depth > limite:
                hijo.depth += 1
            self.actualizar_depth(hijo, limite)

        return self

    def __repr__(self):
        def recorrer_arbol(raiz):
            for hijo in raiz.hijos:
                self.ret += "id-nodo: {} -> id_padre: {} -> color: {} -> numero: {} -> depth: " \
                            "{}\n".format(hijo.id_nodo, hijo.id_padre, hijo.color, hijo.number, hijo.depth)
                recorrer_arbol(hijo)

            return self

        self.ret = 'RAIZ:\nroot-id: {} -> color: {} -> numero: {}\n\nHIJOS:\n'.format(self.id_nodo, self.color,
                                                                                      self.number)
        recorrer_arbol(self)
        return self.ret


if __name__ == '__main__':
    print("Module being run diectly")
