import gui
from gui.kinds.human import Human
from gui.kinds.skull import Skull
from gui.kinds.orc import Orc
from unidades import Warrior, Archer, Pet
from otras_unidades import Villager, Hero
from random import expovariate, randint


class Ejercito:
    def __init__(self, start_info, ide):  # diccionario de param iniciales
        self.ide = ide
        self.start_info = start_info
        self.race = start_info['race']
        self.god = start_info['god']
        self.hero_rate = round(start_info['hero_rate'])

        # estadisticas
        self.creations = {'warrior': 0, 'archer': 0, 'pet': 0}  # numero
        self.deaths = {'warrior': 0, 'archer': 0, 'pet': 0}  # numero
        self.buildings_data = {'tower': 0, 'barracks': 0}
        self.gold_spent = {'villager': 0, 'pet': 0, 'warrior': 0, 'archer': 0}
        self.god_power = {'name': start_info['power'], 'uses': 0,
                          'effectiveness': []}
        self.gold_extraction = [0]
        self.tasa_creacion = [0]
        self.tasa_muerte = [0]

        # informacion
        self._gold = 800

        # atacado por poder
        self.suffer_power = None
        self.last_deaths = list()
        self.to_revive = list()
        self.max_units = self.set_max_units()

        # unidades (vivas)
        self.warriors = list()
        self.archers = list()
        self.pets = list()
        self.villagers = list()
        self.hero = None
        self.hero_lives = 100
        self.hero_death = None

        self.torretas = list()  # al destruir una se reemplaza por None (para reconstruccion)
        self.mine = None
        self.cuartel = None  # unico, vuelve a ser None si se destruye
        self.temple = None

        self.cuartel_location = None
        self.torretas_location = dict()  # indice de torreta en lista y posicion

        self.creation_list = list()  # para llevar cuenta de los ciclos
        self.set_creation_list()
        self.next_creation = None
        self.next_clock = [0, 0]  # [transcurrido, to_next]
        self.next_time()

        self.cicle_pause = False
        self.aux_clock = 0  # para creacion de aldeanos

        self.time_for_hero = 0

        self.objective_qty = 0

    @property
    def gold(self):
        return self._gold

    @gold.setter
    def gold(self, value):
        self._gold = value

    @property
    def total_units(self):
        return len(self.warriors + self.archers + self.pets)

    @property
    def villager_qty(self):
        return len(self.villagers)

    @property
    def all_buildings(self):  # templo y mina siempre estaran
        torretas = True
        if None in self.torretas:
            torretas = False
        elif True in [t.in_construction for t in self.torretas]:
            torretas = False

        cuartel = True
        if self.cuartel is None:
            cuartel = False
        elif self.cuartel.in_construction:
            cuartel = False

        return cuartel and torretas

    @property
    def complete_army(self):  # retorna lista
        if self.hero is None:
            return self.villagers + self.warriors + self.pets + self.archers
        return self.villagers + self.warriors + self.pets + self.archers + [self.hero]

    @property
    def war_units(self):  # retorna lista
        if self.hero is None:
            return self.warriors + self.archers + self.pets
        return self.warriors + self.archers + self.pets + [self.hero]

    def first_villagers(self):
        # primeros 5 aldeanos
        for i in range(5):
            villager = Villager(self.ide)
            villager.add_villager(self.race, self.temple.cord_x + 20 * i,
                                  self.temple.cord_y + 20 * i)
            self.villagers.append(villager)
            gui.add_entity(villager.unit)

    def set_creation_list(self):
        for _ in range(int(self.start_info['rate']['warrior'])):
            self.creation_list.append('warrior')

        for _ in range(int(self.start_info['rate']['archer'])):
            self.creation_list.append('archer')

        for _ in range(int(self.start_info['rate']['pet'])):
            self.creation_list.append('pet')
        return

    def next_time(self):
        if self.next_creation is None or \
                        (self.next_creation + 1) == len(self.creation_list):  # completo un ciclo
            self.next_creation = 0
        else:
            self.next_creation += 1

        aux = self.creation_list[self.next_creation]
        if aux == "warrior":
            self.next_clock = [0, 5]
        elif aux == "archer":
            self.next_clock = [0, 7]
        elif aux == "pet":
            self.next_clock = [0, 6]
        return

    def set_max_units(self):
        if self.race == "Human":
            return 25

        if self.race == "Orc":
            return 20

        if self.race == "Skull":
            return 30

    def creation_cicle(self):  # llamado al pasar un segundo
        if not self.all_buildings:  # edificacion destruida
            return None, None

        if len(self.villagers) < 6:  # pausa en caso de haber menos aldeanos
            self.aux_clock += 1
            if self.aux_clock == 5:
                if self.gold < 10:
                    self.aux_clock -= 1
                    return None, None  # no agrega si no tiene plata

                self.aux_clock = 0
                to_add = self.new_unit('villager')
                self.villagers.append(to_add)
                return to_add.unit, None
            return None, None

        if not self.cicle_pause:
            self.next_clock[0] += 1  # aumenta solo si no hay pausa

        if self.next_clock[0] == self.next_clock[1]:  # se ha completado una creacion
            unit = self.creation_list[self.next_creation]
            if unit == "warrior":
                if self.gold >= 20 and self.total_units < self.max_units:
                    self.cicle_pause = False
                    self.next_time()
                    # crea nueva unidad
                    to_add = self.new_unit(unit)
                    self.warriors.append(to_add)
                    return to_add.unit, "guerreros"

                else:
                    self.cicle_pause = True

            elif unit == "archer":
                if self.gold >= 30 and self.total_units < self.max_units:
                    self.cicle_pause = False
                    self.next_time()
                    to_add = self.new_unit(unit)
                    self.archers.append(to_add)
                    return to_add.unit, None

                else:
                    self.cicle_pause = True

            else:  # pet
                if self.gold >= 50 and self.total_units < self.max_units:
                    self.cicle_pause = False
                    self.next_time()
                    to_add = self.new_unit(unit)
                    self.pets.append(to_add)
                    return to_add.unit, "mascotas"

                else:
                    self.cicle_pause = True
        return None, None

    def hero_arrival(self):
        self.time_for_hero += 1

        if self.hero is None:  # de no existir
            if self.time_for_hero == self.hero_rate:
                to_add = self.new_unit("hero")
                self.hero = to_add
                return to_add.unit

            if self.race == "Skull" and self.hero_lives < 3 and self.hero_death is not None:  # ya perdio una vida
                if self.time_for_hero == round(0.3 * self.hero_rate):
                    to_add = self.new_unit("hero;{};{}".format(self.hero_death[0],
                                                               self.hero_death[1]))
                    self.hero = to_add
                    return to_add.unit
        return

    def new_unit(self, unit_type):
        self.tasa_creacion[-1] += 1

        if unit_type == "warrior":
            self.gold -= 20
            warrior = Warrior()
            warrior.add_warrior(self.race, self.cuartel.cord_x + 40,
                                self.cuartel.cord_y + 90)
            self.creations['warrior'] += 1
            self.gold_spent['warrior'] += 20
            return warrior

        if unit_type == "archer":
            self.gold -= 30
            archer = Archer()
            archer.add_archer(self.race, self.cuartel.cord_x + 40,
                              self.cuartel.cord_y + 90)
            self.creations['archer'] += 1
            self.gold_spent['archer'] += 30
            return archer

        if unit_type == "pet":
            self.gold -= 50
            pet = Pet()
            pet.add_pet(self.race, self.temple.cord_x + 40,
                        self.temple.cord_y + 90)
            self.creations['pet'] += 1
            self.gold_spent['pet'] += 50
            return pet

        if unit_type == "villager":
            self.gold -= 10
            villager = Villager(self.ide)
            villager.add_villager(self.race, self.temple.cord_x + 40,
                                  self.temple.cord_y + 90)
            self.gold_spent['villager'] += 50
            return villager

        if unit_type == "hero":
            if self.race == "Skull":
                self.hero_lives = 3
            else:
                self.hero_lives = 1

            hero = Hero(self.ide, self.race)
            hero.add_hero(self.race, self.temple.cord_x + 40,
                          self.temple.cord_y + 90)
            return hero

        if ";" in unit_type:  # revivir
            aux = unit_type.split(";")
            hero = Hero(self.ide, self.race)
            hero.add_hero(self.race, int(aux[1]), int(aux[2]))
            return hero

    def count_troops(self):
        if self.suffer_power == "berserker":  # no mueren
            for unit in self.war_units:
                unit.unit.health = 1  # sin importar que lo hayan herido
            return []

        deaths = []
        for villager in self.villagers:
            if villager.health <= 0:
                self.villagers.remove(villager)
                deaths.append((villager.unit, 'villager'))

        for warrior in self.warriors:
            if warrior.health <= 0:
                self.warriors.remove(warrior)
                self.new_death(warrior, 'warrior')
                self.deaths['warrior'] += 1
                deaths.append((warrior.unit, 'guerreros'))  # para objetivo

        for archer in self.archers:
            if archer.health <= 0:
                self.archers.remove(archer)
                self.new_death(archer, 'archer')
                self.deaths['archer'] += 1
                deaths.append((archer.unit, 'arqueros'))

        for pet in self.pets:
            if pet.health <= 0:
                if pet.hero_pet:
                    self.hero.pets.remove(pet)
                    if len(self.hero.pets) == 0:
                        self.hero.aux_clock = 0  # comienza contador
                self.pets.remove(pet)
                self.new_death(pet, 'pet')
                self.deaths['pet'] += 1
                deaths.append((pet.unit, 'mascotas'))

        if self.hero is not None:
            if self.hero.health <= 0:
                self.hero_lives -= 1
                self.time_for_hero = 0
                deaths.append((self.hero.unit, 'hero'))

                if self.race == "Orc":  # mueren tambien mascotas
                    for pet in self.hero.pets:
                        if pet in self.pets:
                            self.pets.remove(pet)
                        deaths.append((pet.unit, 'mascotas'))

                if self.race == "Skull" and self.hero_lives < 3:
                    if self.hero_lives >= 0:  # caso contrario: muerte definitiva
                        self.hero_death = [self.hero.unit.cord_x,
                                           self.hero.unit.cord_y]
                    else:
                        self.hero_death = None
                self.hero = None

        self.tasa_muerte[-1] += len(deaths)
        return deaths

    def new_death(self, dead_ally, kind):
        # para poder de invocar muertos
        if len(self.last_deaths) == 7:
            self.last_deaths.pop(0)  # elimina primero en lista

        self.last_deaths.append((dead_ally, kind))
        return

    def activate_power(self, enemy_army):
        self.god_power['uses'] += 1
        self.god_power['effectiveness'].append(0)

        if self.god_power['name'] == "plaga":
            enemy_army.suffer_power = "plaga"
            for unit in enemy_army.complete_army:
                unit.move -= 1
            return randint(8, 15)

        elif self.god_power['name'] == "berserker":
            self.suffer_power = "berserker"  # no lo sufre el enemigo
            for unit in self.war_units:
                unit.harm *= 2  # doble de daño
                unit.unit.health = 1  # baja hp a 1 (pero inmortal por un tiempo)
            return randint(8, 15)

        elif self.god_power['name'] == "terremoto":
            enemy_army.suffer_power = "terremoto"
            return randint(8, 15)

        elif self.god_power['name'] == "invocar_muertos":
            self.suffer_power = "invocar_muertos"

            for dead_unit in self.last_deaths:  # mantienen atributos
                if dead_unit[1] == "warrior":
                    dead_unit[0].add_warrior(self.race, self.cuartel.cord_x + 40,
                                             self.cuartel.cord_y + 90)
                    dead_unit[0].unit.health = round(dead_unit[0].unit.health * 0.5)
                    self.to_revive.append(dead_unit[0].unit)

                elif dead_unit[1] == "archer":
                    dead_unit[0].add_archer(self.race, self.cuartel.cord_x + 40,
                                            self.cuartel.cord_y + 90)
                    dead_unit[0].unit.health = round(
                        dead_unit[0].unit.health * 0.5)
                    self.to_revive.append(dead_unit[0].unit)

                else:  # pet
                    dead_unit[0].add_pet(self.race, self.temple.cord_x + 40,
                                         self.temple.cord_y + 90)
                    dead_unit[0].unit.health = round(
                        dead_unit[0].unit.health * 0.5)
                    self.to_revive.append(dead_unit[0].unit)

            self.last_deaths = list()  # evita errores
            return 1

        elif self.god_power['name'] == "glaciar":
            enemy_army.suffer_power = "glaciar"
            return randint(8, 15)

    def desactivate_power(self, enemy_army):
        if self.god_power['name'] == "plaga":
            for unit in enemy_army.complete_army:
                unit.move += 1
            enemy_army.suffer_power = None

        elif self.god_power['name'] == "berserker":
            self.suffer_power = None  # seguiran teniendo hp 1 y harm doble

        elif self.god_power['name'] == "terremoto":
            enemy_army.suffer_power = None

        elif self.god_power['name'] == "invocar_muertos":
            self.suffer_power = None

        elif self.god_power['name'] == "glaciar":  # glaciar
            enemy_army.suffer_power = None
        return

    def show_statistics(self):
        statistics = ""
        statistics += "\n > Unidades creadas:\n    " \
                      "Soldados: {} | Arqueros: {} | " \
                      "Mascotas: {}".format(self.creations['warrior'],
                                            self.creations['archer'],
                                            self.creations['pet'])
        statistics += "\n > Unidades muertas:\n    " \
                      "Soldados: {} | Arqueros: {} | " \
                      "Mascotas: {}".format(self.deaths['warrior'],
                                            self.deaths['archer'],
                                            self.deaths['pet'])
        statistics += "\n > N° poderes utilizados por {}: {}".format(
            self.god, self.god_power['uses'])
        statistics += "\n > Efectividad del poder {}: {}".format(
            self.god_power['name'], self.show_power_effectiveness())
        statistics += "\n > Tasa de creacion (x min): {}".format(
            sum(self.tasa_creacion) / len(self.tasa_creacion))
        statistics += "\n > Cantidad de oro gastada en:\n    " \
                      "Soldados: {} | Arqueros: {} | Mascotas: {} | " \
                      "Aldeanos: {}\n    Torretas: {} | Cuartel: {}" \
                      "".format(self.gold_spent['warrior'],
                                self.gold_spent['archer'],
                                self.gold_spent['pet'],
                                self.gold_spent['villager'],
                                self.buildings_data['tower'] * 150,
                                self.buildings_data['barracks'] * 100)
        statistics += "\n > Tasa de muerte (x min): {}".format(
            sum(self.tasa_muerte) / len(self.tasa_muerte))
        statistics += "\n > Tasa de extracción de oro (x min): {}".format(
            sum(self.gold_extraction) / len(self.gold_extraction))
        return statistics

    def show_power_effectiveness(self):
        if self.god_power['uses'] == 0:
            return "no se utilizo el poder"
        else:
            effects = sum(self.god_power['effectiveness']) / \
                      len(self.god_power['effectiveness'])
        return str(effects)


if __name__ == "__main__":
    print("Module being run directly")
