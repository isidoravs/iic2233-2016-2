#AC07
import random

name_list = ['Alfonso', 'Benito', 'Alfredo', 'Geronimo', 'Peter', 'Jack',
             'Simon', 'Jaime', 'Bego', 'Francisca', 'Maida', 'Clara', 'Rocio',
             'Sofia', 'Belen', 'Fausto', 'Juan', 'Miguel', 'Mariana',
             'Fernanda', 'Constanza', 'Valentina', 'Tomas']

lastname_list = ['Fernández', 'Rodríguez', 'González', 'García', 'López',
                 'Martínez', 'Pérez', 'Álvarez', 'Gómez', 'Sánchez',
                 'Díaz', 'Vásquez', 'Castro', 'Romero', 'Suárez']

class MetaOrganization(type):
    def __new__(cls, name, bases, dic):
        def see_members(self):
            for member in self.members:
                print(member)

        def replace_boss(self, other):
            self.boss = other

        def __call__(self, *args, **kwargs):
            i = 0
            for member in self.members:
                i += 1
            print('Organización: {0}, jefe: {1}, trabajadores: {2}'.format(self.name, self.boss, i))

        used_names = []
        original_init = dic["__init__"]

        # def __init__(self, name):
        #     used_names.append(self.name)
        #     if name in used_names:
        #         return None
        #     else:
        #         original_init()

        dic["see_members"] = see_members
        dic["replace_boss"] = replace_boss
        dic["__call__"] = __call__
        #dic["__init__"] = __init__
        dic["used_names"] = used_names
        return super().__new__(cls, name, bases, dic)


class MetaPerson(type):

    def __new__(meta, name, bases, attr):
        # metodos caracteristicos
        def to_order(self):
            print("Esto es una orden!")

        def to_work(self):
            print("Trabajar, trabajar")

        if name == "Boss":
            attr.update(dict({'order': to_order}))

        if name == "Worker":
            attr.update(dict({'to_work': to_work}))

        def __newinit__(self, organization):
            # recibe nombre, apellido y edad aleatorio
            self.name = random.choice(name_list)
            self.last_name = random.choice(lastname_list)
            self.age = random.randint(0, 20)
            self.organization = organization.name
            self.instancia_org = organization

        attr['__init__'] = __newinit__

        # casos
        if "Boss" in name:
            return super().__new__(meta, "Boss", bases, attr)

        if "Worker" in name:
            return super().__new__(meta, "Worker", bases, attr)

    def __call__(cls, *args, **kwargs):

        instancia_org = args[0]

        # metodo por usar
        def add_member(self, member):
            self.instancia_org.members.append(member)

        # revisar jerarquia
        if instancia_org is None:  # no posee un jefe
            if cls.__name__ == "Boss":
                # nuevo metodo
                setattr(cls, 'add_member', add_member)
                instancia = super().__call__(*args, **kwargs)

                # adopta como jefe
                instancia_org.boss = instancia

                # retorna instancia
                return instancia

            else:
                return None

        else:  # posee un jefe
            if cls.__name__ == "Boss":
                instancia = super().__call__(*args, **kwargs)
                instancia_org.replace_boss(instancia)
                setattr(cls, 'add_member', add_member)
                return instancia

            else:
                return super().__call__(*args, **kwargs)


# Solo modificar para agregar metaclass=*
class Boss(metaclass=MetaPerson):
    def __init__(self, organization, *args, **kwargs):
        self.organization = organization

    def __repr__(self):
        return 'Boss: {0.name} {0.last_name}'.format(self)


class Worker(metaclass=MetaPerson):
    def __init__(self, organization, *args, **kwargs):
        self.organization = organization

    def __repr__(self):
        return 'Worker: {0.name} {0.last_name}'.format(self)


class Organization(metaclass=MetaOrganization):

    def __init__(self, name):
        self.name = name
        self.boss = None
        self.members = list()

    def __repr__(self):
        return 'Organizacion: {}'.format(self.name)

    def pick_one_worker(self):
        return random.choice(self.members)


if __name__ == '__main__':
    salo = Organization('Salo')
    print(salo)
    salo()
    print()
    sola = Organization('Sola')
    print(sola)
    sola()

    z = Organization('Salo')
    print("Nombres utilizados {}".format(Organization.used_names))
    print()

    jefe_salo = Boss(salo)
    jefe_sola = Worker(sola)
    jefe_sola = Boss(sola)
    print()

    for i in range(3):
        w = Worker(salo)
        jefe_salo.add_member(w)
        w.to_work()
    salo.pick_one_worker().to_work()
    jefe_salo.order()
    print()
    for i in range(2):
        jefe_sola.add_member(Worker(sola))
    sola.pick_one_worker().to_work()
    jefe_sola.order()

    new_jefe_salo = Boss(salo)

    print('--'*50)
    salo()
    salo.see_members()
    print('--'*50)
    sola()
    sola.see_members()
    print('--'*50)
