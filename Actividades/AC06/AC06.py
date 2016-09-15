__author__ = "Juan Cortes, Cristian Cortes, Manuel Silva"


def verify(function):
    def new_function(*args):
        if isinstance(args[1], str) and isinstance(args[2], int) and isinstance(args[3], list) and isinstance(args[4],
                                                                                                              str):
            setattr(args[0], "nombre", args[1])
            setattr(args[0], "level", args[2])
            setattr(args[0], "evolutions", args[3])
            setattr(args[0], "owner", args[4])

        else:
            raise Exception("Los atributos no cumplen con el tipo de datos")
    return new_function


def protect_method(*metodos):  # recibe cantidad no determinada
    def decorador(Clase):
        for metodo in metodos:
            if metodo not in dir(Clase):
                print(metodo, "no es un metodo de la clase")
            else:
                new_name = "__" + metodo

                def new_function(self, *args, **kwargs):
                    if self.owner != "Prof. Oak":
                        print("Metodo privado")
                    else:
                        print("Bienvenido Prof. Oak")  # falta cambiar que si pueda acceder

                old_method = getattr(Clase, metodo)
                setattr(Clase, new_name, old_method)
                setattr(Clase, metodo, new_function)

                return Clase
    return decorador


def my_name(function):
    def new_function(self):
        return self.nombre
    return new_function


def strongest(function):
    def new_function(self):
        fuerte = max(self.pokemon, key=lambda x: x.level)
        print('El mas fuerte es {0.nombre} con level {0.level}'.format(fuerte))

    return new_function


def is_pokemon(function):
    def new_function(self, pokemon, *args):
        if not isinstance(pokemon, Pokemon):
            print("Error, este no es un Pokemon valido !")
        else:
            self.pokemon.append(pokemon)
    return new_function


# CREA LOS DECORADORES ARRIBA
# DESDE AQUI HACIA ABAJO NO PUEDES MODIFICAR NINGUNA DE LAS CLASES Y FUNCIONES, SOLO DECORARLAS
class Pokedex:
    def __init__(self):
        self.pokemon = list()

    @is_pokemon
    def add_pokemon(self, pokemon):
        self.pokemon.append(pokemon)

    @strongest
    def compare(self):
        print('El mas fuerte es {0.nombre}'.format(
            max(self.pokemon, key=lambda x: len(x.nombre))))

    def __str__(self):
        return 'Llevas {} Pokemon:\n{}'.format(len(self.pokemon), self.pokemon)


@protect_method("set_attributes")
class Pokemon:
    @verify
    def __init__(self, nombre, level, evolutions, owner):
        self.nombre = nombre
        self.level = level
        self.evolutions = evolutions
        self.owner = owner

    def set_attributes(self, tipo):
        self.tipo = tipo

    @my_name
    def __repr__(self):
        return 'Hola soy Charmander!'


class Legendario(Pokemon):
    def __init__(self, *args):
        super().__init__(*args)


if __name__ == '__main__':
    try:
        pik = Pokemon('Pikachu', 32.4, ['Raichu'], 'Ash')
    except Exception:
        print('Su verify parece funcionar :)')

mag = Pokemon('Magikarp', 5, ['Gyarados'], 'Ash')
leg = Legendario('Mew', 80, [], 'Prof. Oak')
pokedex = Pokedex()

pokedex.add_pokemon('Charmander')

pokedex.add_pokemon(leg)

pokedex.add_pokemon(mag)

mag.set_attributes('Agua')
leg.set_attributes('All')

print(leg)
print(pokedex)

pokedex.compare()
