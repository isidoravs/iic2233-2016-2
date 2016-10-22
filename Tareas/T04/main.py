import gui
from inicio import Inicio
from ejercitos import Ejercito
from edificaciones import Cuartel, Torreta, Mina, Templo
from otras_unidades import Hero
from time import sleep
from sys import exit
from random import randint, choice


class Simulacion:
    def __init__(self, tiempo_max, team1, team2):  # distingue equipos como 1 y 2
        self.tiempo_max = tiempo_max
        self.tiempo_sim = 0
        self.count = 0
        self.army1 = Ejercito(team1, 1)
        self.army2 = Ejercito(team2, 2)
        self.set_map()

        # primeros 5 aldeanos
        self.army1.first_villagers()
        self.army2.first_villagers()

        # primer objetivo
        self.objective = None  # [ide, name, qty, target]
        self.army_power = 0
        self.new_objective()

        self.winner = None

    def tick(self):
        self.count += 1

        # pasa un segundo de la simulacion
        if self.count == 7:  # ALTERABLE RR
            self.tiempo_sim += 1
            self.count = 0

        if self.tiempo_sim < self.tiempo_max and self.winner is None:
            if self.count == 0:  # acaba de pasar un segundo
                if self.tiempo_sim % 60 == 0:  # pasa un minuto
                    # nuevo minuto
                    self.army1.gold_extraction.append(0)
                    self.army2.gold_extraction.append(0)

                    self.army1.tasa_creacion.append(0)
                    self.army2.tasa_creacion.append(0)

                    self.army1.tasa_muerte.append(0)
                    self.army2.tasa_muerte.append(0)

                # oro
                gui.set_gold_t1(self.army1.gold)
                gui.set_gold_t2(self.army2.gold)

                # tarea aldeanos
                for villager in self.army1.villagers:  # mina y templo no estan destruidos
                    mine_x = self.army1.mine.cord_x + 40
                    mine_y = self.army1.mine.cord_y + 75  # centro

                    temple_x = self.army1.temple.cord_x + 30
                    temple_y = self.army1.temple.cord_y + 100 # puerta
                    villager.avanzar((mine_x, mine_y), (temple_x, temple_y),
                                     self.army1)
                    if villager.new_building is not None:  # empezo edificacion
                        gui.add_entity(villager.new_building)
                        if villager.new_building.cost == 100:
                            self.army1.gold -= 100
                            self.army1.buildings_data['barracks'] += 1
                        else:
                            self.army1.gold -= 150
                            self.army1.buildings_data['tower'] += 1
                        villager.new_building = None

                for villager in self.army2.villagers:  # mina y templo no estan destruidos
                    mine_x = self.army2.mine.cord_x + 40
                    mine_y = self.army2.mine.cord_y + 75  # centro

                    temple_x = self.army2.temple.cord_x + 30
                    temple_y = self.army2.temple.cord_y + 100  # puerta
                    villager.avanzar((mine_x, mine_y), (temple_x, temple_y),
                                     self.army2)
                    if villager.new_building is not None:  # empezo edificacion
                        gui.add_entity(villager.new_building)
                        if villager.new_building.cost == 100:
                            self.army2.gold -= 100
                            self.army2.buildings_data['barracks'] += 1
                        else:
                            self.army2.gold -= 150
                            self.army2.buildings_data['tower'] += 1
                        villager.new_building = None

                # nuevas unidades
                new_unit1, kind1 = self.army1.creation_cicle()
                new_unit2, kind2 = self.army2.creation_cicle()

                if new_unit1 is not None:  # se debe crear una unidad
                    gui.add_entity(new_unit1)
                    if self.objective[0] == 2 and self.objective[3] == kind1:
                        self.army1.objective_qty += 1

                if new_unit2 is not None:
                    gui.add_entity(new_unit2)
                    if self.objective[0] == 2 and self.objective[3] == kind1:
                        self.army2.objective_qty += 1

                hero1_arrival = self.army1.hero_arrival()
                hero2_arrival = self.army2.hero_arrival()

                if hero1_arrival is not None:
                    gui.add_entity(hero1_arrival)

                if hero2_arrival is not None:
                    gui.add_entity(hero2_arrival)

                if self.army1.hero is not None and self.army1.hero.new_entity != []:
                    for pet in self.army1.hero.new_entity:
                        gui.add_entity(pet.unit)
                        self.army1.pets.append(pet)
                    self.army1.hero.new_entity = list()

                if self.army2.hero is not None and self.army2.hero.new_entity != []:
                    for pet in self.army2.hero.new_entity:
                        gui.add_entity(pet.unit)
                        self.army2.pets.append(pet)
                    self.army2.hero.new_entity = list()

                if len(self.army1.to_revive) > 0:  # luego de invocar muertos
                    for dead in self.army1.to_revive:
                        gui.add_entity(dead)
                        self.army1.god_power['effectiveness'][-1] += 1
                    self.army1.to_revive = list()

                if len(self.army2.to_revive) > 0:
                    for dead in self.army2.to_revive:
                        gui.add_entity(dead)
                        self.army2.god_power['effectiveness'][-1] += 10
                    self.army2.to_revive = list()

                '''
                    ATAQUE Y AVANZAR
                '''
                # torretas
                for torreta in self.army1.torretas:
                    if torreta is not None:
                        torreta.check_perimeter(self.army2.complete_army)

                for torreta in self.army2.torretas:
                    if torreta is not None:
                        torreta.check_perimeter(self.army1.complete_army)

                # accion de ejercito ARMY1
                if self.army1.suffer_power == "glaciar":  # no se pueden mover ni atacar
                    pass
                else:
                    if self.army1.race == "Human":
                        if self.human_condition(self.army1, self.army2):
                            strongest = sorted(self.army1.war_units, key=lambda x:
                            x.move, reverse=True)

                            for unit in strongest[: len(strongest) // 2]:
                                unit.avanzar(self.army1.race, self.army2.temple,
                                             self.army2.cuartel,
                                             self.army2.torretas,
                                             self.army2.complete_army,
                                             self.army1.complete_army)

                            list_defenders = strongest[len(strongest) // 2:]

                            # heroe no defiende
                            if self.army1.hero is not None and self.army1.hero in list_defenders:
                                list_defenders.remove(self.army1.hero)
                                self.army1.hero.avanzar(self.army1.race,
                                                        self.army2.temple,
                                                        self.army2.cuartel,
                                                        self.army2.torretas,
                                                        self.army2.complete_army,
                                                        self.army1.complete_army)

                            troop1, troop2, troop3 = self.split_defenders(list_defenders)

                            for unit in troop1:  # cuartel
                                if self.army1.cuartel is not None:
                                    unit.defend(self.army1.cuartel,
                                                self.army2.war_units)
                                else:
                                    unit.defend(self.army1.temple,
                                                self.army2.war_units)

                            for unit in troop2:  # torretas
                                if len(self.army1.torretas) > 0 and \
                                                self.army1.torretas[0] is not None:
                                    unit.defend(self.army1.torretas[0],
                                                self.army2.war_units)
                                else:
                                    unit.defend(self.army1.temple,
                                                self.army2.war_units)

                            for unit in troop3:
                                unit.defend(self.army1.temple, self.army2.war_units)

                        else:
                            for unit in self.army1.war_units:
                                unit.defend(self.army1.temple, self.army2.war_units)
                    else:
                        for unit in self.army1.war_units:
                            unit.avanzar(self.army1.race, self.army2.temple,
                                         self.army2.cuartel,
                                         self.army2.torretas,
                                         self.army2.complete_army,
                                         self.army1.complete_army)

                # accion ejercito ARMY2
                if self.army2.suffer_power == "glaciar":
                    pass  # frozen
                else:
                    if self.army2.race == "Human":
                        if self.human_condition(self.army2, self.army1):
                            strongest = sorted(self.army2.war_units, key=lambda x:
                            x.move, reverse=True)

                            for unit in strongest[: len(strongest) // 2]:
                                unit.avanzar(self.army2.race, self.army1.temple,
                                             self.army1.cuartel,
                                             self.army1.torretas,
                                             self.army1.complete_army,
                                             self.army2.complete_army)

                            list_defenders = strongest[len(strongest) // 2:]
                            # heroe no defiende
                            if self.army2.hero is not None and self.army2.hero in list_defenders:
                                list_defenders.remove(self.army1.hero)
                                self.army2.hero.avanzar(self.army2.race,
                                                        self.army1.temple,
                                                        self.army1.cuartel,
                                                        self.army1.torretas,
                                                        self.army1.complete_army,
                                                        self.army2.complete_army)

                            troop1, troop2, troop3 = self.split_defenders(
                                list_defenders)

                            for unit in troop1:  # cuartel
                                if self.army2.cuartel is not None:
                                    unit.defend(self.army2.cuartel,
                                                self.army1.war_units)
                                else:
                                    unit.defend(self.army2.temple,
                                                self.army1.war_units)

                            for unit in troop2:  # torretas
                                if len(self.army2.torretas) > 0 and \
                                                self.army2.torretas[0] is not None:
                                    unit.defend(self.army2.torretas[0],
                                                self.army1.war_units)
                                else:
                                    unit.defend(self.army2.temple,
                                                self.army1.war_units)

                            for unit in troop3:
                                unit.defend(self.army2.temple, self.army1.war_units)

                        else:
                            for unit in self.army2.war_units:
                                unit.defend(self.army2.temple, self.army1.war_units)
                    else:
                        for unit in self.army2.war_units:
                            unit.avanzar(self.army2.race, self.army1.temple,
                                         self.army1.cuartel,
                                         self.army1.torretas,
                                         self.army1.complete_army,
                                         self.army2.complete_army)

                '''
                    EFECTOS DE PODER
                '''
                if self.army1.suffer_power == "terremoto":
                    for torreta in self.army1.torretas:
                        if torreta is not None:
                            torreta.health -= 10
                            self.army2.god_power['effectiveness'][-1] += 10

                    if self.army1.cuartel is not None:
                        self.army1.cuartel.health -= 10
                        self.army2.god_power['effectiveness'][-1] += 10

                    if self.army1.temple.health >= 20:
                        self.army1.temple.health -= 10
                        self.army2.god_power['effectiveness'][-1] += 10

                elif self.army1.suffer_power == "plaga":
                    for unit in self.army1.complete_army:
                        unit.unit.health -= 8

                if self.army2.suffer_power == "terremoto":
                    for torreta in self.army2.torretas:
                        if torreta is not None:
                            torreta.health -= 10
                            self.army1.god_power['effectiveness'][-1] += 10

                    if self.army2.cuartel is not None:
                        self.army2.cuartel.health -= 10
                        self.army1.god_power['effectiveness'][-1] += 10

                    if self.army2.temple.health >= 20:
                        self.army2.temple.health -= 10
                        self.army1.god_power['effectiveness'][-1] += 10

                elif self.army2.suffer_power == "plaga":
                    for unit in self.army2.complete_army:
                        unit.unit.health -= 8

                '''
                    EFECTOS DE ATAQUE
                '''
                # destruccion
                if self.army1.temple.health <= 0:
                    self.army1.temple.deleteLater()  # elimina de interfaz
                    self.army1.temple = None
                    self.winner = self.army2
                    print("{}s destroyed the enemy's Temple!".format(self.army2.race))

                if self.army2.temple.health <= 0:
                    self.army2.temple.deleteLater()
                    self.army2.temple = None
                    self.winner = self.army1
                    print("{}s destroyed the enemy's Temple!".format(self.army1.race))

                for i in range(len(self.army1.torretas)):
                    tower = self.army1.torretas[i]
                    if tower is not None and tower.health <= 0:
                        tower.deleteLater()
                        self.army1.torretas[i] = None

                for i in range(len(self.army2.torretas)):
                    tower = self.army2.torretas[i]
                    if tower is not None and tower.health <= 0:
                        tower.deleteLater()
                        self.army2.torretas[i] = None

                if self.army1.cuartel is not None and self.army1.cuartel.health <= 0:
                    self.army1.cuartel.deleteLater()
                    self.army1.cuartel = None

                if self.army2.cuartel is not None and self.army2.cuartel.health <= 0:
                    self.army2.cuartel.deleteLater()
                    self.army2.cuartel = None

                # efectos magicos
                if self.army1.hero is not None and self.army1.hero.enemy_to_clone is not None:
                    enemy = self.army1.hero.enemy_to_clone
                    new_clone = Hero(self.army1.ide, self.army1.race)

                    # mismas caracteristicas pero sin poder
                    new_clone.clone = True
                    new_clone.move = self.army1.hero.move
                    new_clone.hp = self.army1.hero.hp
                    new_clone.harm = self.army1.hero.harm
                    new_clone.add_hero(self.army1.race, enemy.unit.cord_x,
                                       enemy.unit.cord_y)
                    self.army1.warriors.append(new_clone)

                    self.army1.hero.enemy_to_clone = None
                    gui.add_entity(new_clone.unit)

                if self.army2.hero is not None and self.army2.hero.enemy_to_clone is not None:
                    enemy = self.army2.hero.enemy_to_clone
                    new_clone = Hero(self.army2.ide, self.army2.race)

                    # mismas caracteristicas pero sin poder
                    new_clone.clone = True
                    new_clone.move = self.army2.hero.move
                    new_clone.hp = self.army2.hero.hp
                    new_clone.harm = self.army2.hero.harm
                    new_clone.add_hero(self.army2.race, enemy.unit.cord_x,
                                       enemy.unit.cord_y)
                    self.army2.warriors.append(new_clone)

                    self.army2.hero.enemy_to_clone = None
                    gui.add_entity(new_clone.unit)

                # muertes
                deaths1 = self.army1.count_troops()
                deaths2 = self.army2.count_troops()

                if len(deaths1) > 0:
                    for unit in deaths1:
                        if self.army1.suffer_power == "plaga" or self.army1.suffer_power == "berserker" or self.army1.suffer_power == "glaciar":
                            self.army2.god_power['effectiveness'][-1] += 1

                        unit[0].deleteLater()  # saca de simulacion
                        if self.objective[0] == 1 and self.objective[3] == unit[1]:
                            # suma al objetivo de matar
                            self.army1.objective_qty += 1

                if len(deaths2) > 0:
                    for unit in deaths2:
                        if self.army2.suffer_power == "plaga" or self.army2.suffer_power == "berserker" or self.army2.suffer_power == "glaciar":
                            self.army1.god_power['effectiveness'][-1] += 1
                        unit[0].deleteLater()
                        if self.objective[0] == 1 and self.objective[3] == unit[1]:
                            self.army2.objective_qty += 1

                '''
                    REVISAR CUMPLIMIENTO DE OBJETIVO
                '''
                if self.army1.objective_qty == self.objective[2]:
                    time = self.army1.activate_power(self.army2)
                    self.objective = [4, time, "activate", 0]  # tiempo duracion
                    gui.set_objective("PODER: {}".format(
                        self.army1.god_power['name']))
                    self.army1_power = 1

                if self.army2.objective_qty == self.objective[2]:
                    time = self.army2.activate_power(self.army1)
                    self.objective = [4, time, "activate", 0]  # 0 es contador
                    gui.set_objective("PODER: {}".format(
                        self.army2.god_power['name']))
                    self.army_power = 2

                if self.objective[2] == "activate":
                    self.objective[3] += 1  # suma tiempo
                    if self.objective[3] == self.objective[1]:  # fin del tiempo
                        if self.army_power == 1:
                            self.army1.desactivate_power(self.army2)
                        if self.army_power == 2:
                            self.army2.desactivate_power(self.army1)

                        self.army_power = 0
                        self.new_objective()

        else:
            print(" -- End of Simulation -- ")
            # estadisticas
            self.show_statistics()
            sleep(2)
            exit()

    def set_map(self, path="mapa.csv"):
        with open(path, "r") as archivo:
            lines = [elem.strip().split(",") for elem in archivo.readlines()][1:]

        for line in lines:
            x_pos = int(line[1])
            y_pos = int(line[2])
            if line[3] == "Templo":
                if "1" in line[4]:
                    temple = Templo(self.army1.god, x_pos, y_pos)
                    self.army1.temple = temple

                else:
                    temple = Templo(self.army2.god, x_pos, y_pos)
                    self.army2.temple = temple
                gui.add_entity(temple)

            elif line[3] == "Cuartel":
                cuartel = Cuartel(x_pos, y_pos)
                if "1" in line[4]:
                    self.army1.cuartel = cuartel
                    self.army1.cuartel_location = (x_pos, y_pos)
                else:
                    self.army2.cuartel = cuartel
                    self.army2.cuartel_location = (x_pos, y_pos)
                gui.add_entity(cuartel)

            elif line[3] == "Mina":
                mine = Mina(x_pos, y_pos)
                if "1" in line[4]:
                    self.army1.mine = mine
                else:
                    self.army2.mine = mine
                gui.add_entity(mine)

            elif line[3] == "Torreta":
                torreta = Torreta(x_pos, y_pos)
                if "1" in line[4]:
                    self.army1.torretas.append(torreta)
                    self.army1.torretas_location[
                        self.army1.torretas.index(torreta)] = (x_pos, y_pos)
                else:
                    self.army2.torretas.append(torreta)
                    self.army2.torretas_location[
                        self.army2.torretas.index(torreta)] = (x_pos, y_pos)
                gui.add_entity(torreta)
        return

    def show_statistics(self, to_print=True):
        statistics = " -- Estadisticas {} vs. {} -- ".format(self.army1.race,
                                                             self.army2.race)
        statistics += "\n[{}]".format(self.army1.race)
        statistics += self.army1.show_statistics()
        statistics += "\n\n[{}]".format(self.army2.race)
        statistics += self.army2.show_statistics()
        statistics += "\n\n -- RESULTADO FINAL -- \n "
        statistics += self.set_winner()

        if to_print:
            print(statistics)
        # escribir en archivo
        file_name = "statistics {} vs. {} war.txt".format(self.army1.race,
                                                          self.army2.race)
        with open(file_name, "w") as file:
            file.write(statistics)

        return

    def set_winner(self):
        if self.winner is None:
            return "Ninguna raza ha logrado destruir el templo enemigo." \
                   "\n ~ EMPATE ~"
        else:
            return " ~ GANADOR: {} ~\n Dios: {}".format(self.winner.race,
                                                        self.winner.god)

    def new_objective(self):  # ver como llevar la cuenta
        aux = randint(0, 2)
        if aux == 0:
            qty = randint(200, 500)
            name = "Recolectar {} unidades de oro".format(qty)
            self.objective = [0, name, qty, None]
        elif aux == 1:
            qty = randint(5, 10)
            target = choice(["guerreros", "arqueros", "mascotas"])
            name = "Matar {} {}".format(qty, target)
            self.objective = [1, name, qty, target]
        else:
            if self.army2.god == "flo" or self.army1.god == "flo":
                qty = randint(10, 20)
                name = "Crear {} mascotas".format(qty)
                self.objective = [2, name, qty, "mascotas"]
            else:
                qty = randint(10, 20)
                name = "Crear {} guerreros".format(qty)
                self.objective = [2, name, qty, "guerreros"]

        self.army1.objective_qty = 0
        self.army2.objective_qty = 0

        gui.set_objective(self.objective[1])
        return

    def human_condition(self, human_army, enemy_army):
        if len(human_army.war_units) >= 0.75 * len(enemy_army.war_units):
            return True
        return False

    def split_defenders(self, list_defenders):
        aux = len(list_defenders)
        cut1 = aux // 3
        cut2 = cut1 * 2
        return list_defenders[:cut1], list_defenders[cut1:cut2], list_defenders[cut2:]


if __name__ == "__main__":
    start = Inicio()
    team1 = {'race': start.race1, 'god': start.god1, 'power': start.power1,
             'rate': start.rate1, 'hero_rate': start.heroe1_rate}
    team2 = {'race': start.race2, 'god': start.god2, 'power': start.power2,
             'rate': start.rate2, 'hero_rate': start.heroe2_rate}

    simulation = Simulacion(start.tiempo_max, team1, team2)
    gui.set_size(1024, 680)
    gui.run(simulation.tick)
