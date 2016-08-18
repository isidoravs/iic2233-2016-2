

class Animal:
    def __init__(self, nombre, color, sexo):
        self.nombre = nombre
        self.color = color
        self.sexo = sexo
        self.horas_sueno = 0
        self.horas_juego_ind = 0
        self.horas_juego_grup = 0
        self.comidas = 0
        self.horas_regaloneo = 0

    def set_parametros(self, animal):
        if animal.personalidad == 'juguetona':
            self.horas_sueno = 8 * animal.expresion
            self.horas_juego_ind = 1 * animal.expresion
            self.horas_juego_grup = 7 * animal.expresion
            self.comidas = 4 * animal.expresion
            self.horas_regaloneo = 4 * animal.expresion
        else:
            self.horas_sueno = 12 * animal.expresion
            self.horas_juego_ind = 5 * animal.expresion
            self.horas_juego_grup = 1 * animal.expresion
            self.comidas = 4 * animal.expresion
            self.horas_regaloneo = 2 * animal.expresion

    def jugar(self):
        pass

    def comer(self):
        pass

    def __str__(self):
        return "Me llamo {}, soy {} y tengo el pelo {}.".format(self.nombre, self.sexo, self.color)


class Gato(Animal):
    def __init__(self, nombre, color, sexo):
        super().__init__(nombre, color, sexo)

    def maullar(self):
        print("Miauuu!! Miauuu!")
        return

    def jugar(self):
        print("Humano, ahora, juguemos.")
        return

    def comer(self):
        print("El pellet es horrible. Dame comida en lata.")
        return


class Perro(Animal):
    def __init__(self, nombre, color, sexo):
        super().__init__(nombre, color, sexo)

    def ladrar(self):
        print('Guau!! Guau!!')
        return

    def jugar(self):
        print('Tirame la pelota :)')
        return

    def comer(self):
        print('Mami :) Quiero comeeeerr!!')
        return


class SiamePUC(Gato):
    def __init__(self, expresion, nombre, color, sexo):
        super().__init__(nombre, color, sexo)
        self.expresion = expresion
        self.personalidad = 'egoista'
        if self.sexo == "Hembra":
            self.expresion *= 1.5
        self.set_parametros(self)

    def comer(self):
        print("Quiero comida.")
        super().comer()
        super().maullar()


class GoldenPUC(Perro):
    def __init__(self, expresion, nombre, color, sexo):
        super().__init__(nombre, color, sexo)
        self.expresion = expresion
        self.personalidad = 'juguetona'
        if self.sexo == "Hembra":
            self.expresion *= 0.9
        else:
            self.expresion *= 1.1
        self.set_parametros(self)

    def jugar(self):
        print("Quiero jugar.")
        super().jugar()
        self.ladrar()


class PUCTerrier(Perro):
    def __init__(self, expresion, nombre, color, sexo):
        super().__init__(nombre, color, sexo)
        self.expresion = expresion
        self.personalidad = 'egoista'
        if self.sexo == "Hembra":
            self.expresion *= 1
        else:
            self.expresion *= 1.2
        self.set_parametros(self)

    def comer(self):
        print("Quiero comer.")
        super().comer()
        self.ladrar()


def estadisticas(animales):
        sueno, juego_ind, juego_grup, comidas, horas_regaloneo = 1000, 1000, 0, 0, 0
        for animal in animales:
            if animal.horas_sueno < sueno:
                sueno = animal.horas_sueno
            if animal.horas_juego_ind < juego_ind:
                juego_ind = animal.horas_juego_ind
            if animal.horas_juego_grup > juego_grup:
                juego_grup = animal.horas_juego_grup
            comidas += animal.comidas
            horas_regaloneo += animal.horas_regaloneo
        print('''Tiempo de sueno: {}\nTiempo de juego individual: {}
Tiempo de juego grupal: {}\nCantidad de comidas: {}
Tiempo de regaloneo: {}
'''.format(sueno, juego_ind, juego_grup, comidas, horas_regaloneo))
        return    
            
if __name__ == '__main__':
    animals = list()
    animals.append(GoldenPUC(expresion=0.5, nombre="Mara", color="Blanco", sexo="Hembra"))
    animals.append(GoldenPUC(expresion=0.9, nombre="Eddie", color="Rubio", sexo="Macho"))
    animals.append(SiamePUC(expresion=0.9, nombre="Felix", color="Naranjo", sexo="Hembra"))
    animals.append(PUCTerrier(expresion=0.8, nombre="Betty", color="Café", sexo="Hembra"))

    for a in animals:
        print(a)
        a.jugar()
        a.comer()
    
    estadisticas(animals)
