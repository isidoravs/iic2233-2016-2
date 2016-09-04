# implementacion de mis Estructuras de Datos


class Node:
    def __init__(self, value=None, siguiente=None):
        self.value = value
        self.next = siguiente

    def __repr__(self):
        return str(self.value)


class MyList:
    def __init__(self, root=None, *args):
        self.root = Node(root) if root else None
        self.tail = self.root
        for arg in args:
            self.append(arg)

    def append(self, value):
        if not self.root:
            self.root = Node(value)
            self.tail = self.root
        else:
            self.tail.next = Node(value)
            self.tail = self.tail.next

    def insert_value(self, i, value):
        actual_node = self.root
        while i > 1:
            actual_node = actual_node.next
            i -= 1
        new_node = Node(value, actual_node.next)
        actual_node.next = new_node

    def __len__(self):
        length = 0
        actual_node = self.root
        while actual_node:
            length += 1
            actual_node = actual_node.next
        return length

    def __getitem__(self, i):  # sirve para iterar y elem in lista
        actual_node = self.root
        for _ in range(i):
            if actual_node:  # si es que existe
                actual_node = actual_node.next
        if not actual_node:
            raise IndexError("El indice ingresado está fuera del rango de la lista")
        return actual_node.value

    def __repr__(self):
        ret = "["
        actual_node = self.root
        while actual_node:
            ret += "{}, ".format(actual_node.value)
            actual_node = actual_node.next
        return ret.strip(", ") + "]"
