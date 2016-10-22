import unittest
from main import Simulacion
from ejercitos import Ejercito
from unidades import Warrior, Archer, Pet, in_perimeter, distance
from otras_unidades import Villager, Hero
from edificaciones import Cuartel, Torreta, Mina, Templo
import gui
from gui.kinds.human import Human


class WarUnitsTest(unittest.TestCase):

    def setUp(self):
        self.sim = Simulacion(30, {'race': "Human", 'god': "flo", 'power': "plaga",
                              'rate': {"warrior": 1, "archer": 2, "pet": 3},
                              'hero_rate': 5.0}, {'race': "Human", 'god': "flo", 'power': "plaga",
                              'rate': {"warrior": 1, "archer": 2, "pet": 3},
                              'hero_rate': 5.0})

        self.army = Ejercito({'race': "Human", 'god': "flo", 'power': "plaga",
                              'rate': {"warrior": 1, "archer": 2, "pet": 3},
                              'hero_rate': 5.0}, 1)

        self.warrior1 = Warrior()
        self.archer1 = Archer()
        self.pet1 = Pet()

        self.warrior2 = Warrior()
        self.archer2 = Archer()
        self.pet2 = Pet()

        self.hero_skull = Hero(1, "Skull")
        self.hero_human = Hero(1, "Human")
        self.hero_orc = Hero(1, "Orc")
        self.villager1 = Villager(1)
        self.villager2 = Villager(2)

        self.aux_warrior = Warrior()
        self.aux_warrior.add_warrior("Skull", 490, 510)

        self.aux_archer = Archer()
        self.aux_archer.add_archer("Skull", 1400, 1400)

        self.aux_pet = Pet()
        self.aux_pet.add_pet("Skull", 1400, 1000)

        self.villager1.add_villager("Human", 0, 0)
        self.warrior1.add_warrior("Human", 205, 205)
        self.archer1.add_archer("Human", 900, 900)
        self.pet1.add_pet("Human", 0, 0)
        self.hero_human.add_hero("Human", 401, 401)

        self.warrior2.add_warrior("Orc", 400, 400)
        self.archer2.add_archer("Orc", 905, 905)
        self.pet2.add_pet("Orc", 0, 0)

        self.army.villagers.append(self.villager1)
        self.army.warriors.append(self.warrior1)
        self.army.archers.append(self.archer1)
        self.army.pets.append(self.pet1)
        self.army.hero = self.hero_human

        self.cuartel = Cuartel(0, 0)
        self.temple = Templo("flo", 500, 500)
        self.torre = Torreta(200, 200)
        self.mina = Mina(300, 300)

    def test_towerInPerimeter(self):
        self.assertTrue(self.torre.in_perimeter(self.warrior1))
        self.assertFalse(self.torre.in_perimeter(self.pet1))

    def test_towerCheckPerimeter(self):
        old_warrior_health = self.warrior1.health
        old_archer_health = self.archer1.health

        self.torre.check_perimeter(self.army.war_units)
        self.assertEqual(old_archer_health, self.archer1.health)
        self.assertNotEqual(old_warrior_health, self.warrior1.health)

        self.torre.in_construction = True
        self.assertIsNone(self.torre.check_perimeter(self.army))

    def test_warriorMove(self):
        old_pos = (self.aux_warrior.unit.cord_x, self.aux_warrior.unit.cord_y)
        self.aux_warrior.avanzar("Orc", self.temple, self.cuartel, [self.torre],
                                 self.army.complete_army,
                                 [self.warrior2, self.archer2, self.pet2])
        # no hay enemigos cerca se mueve al templo
        self.assertNotEqual(old_pos[0], self.aux_warrior.unit.cord_x)
        self.assertNotEqual(old_pos[1], self.aux_warrior.unit.cord_y)

    def test_petMove(self):
        old_enemy_health = self.archer1.health
        self.archer2.avanzar("Orc", self.temple, self.cuartel, [self.torre],
                             self.army.complete_army,
                             [self.warrior2, self.archer2, self.pet2])
        # ataca
        self.assertLess(self.archer1.health, old_enemy_health)

    def test_archerMoveNear(self):
        old_pos = (self.archer2.unit.cord_x, self.archer2.unit.cord_y)
        self.archer2.move_near(self.archer1.unit, False)

        self.assertNotEqual(self.archer2.unit.cord_x, old_pos[0])
        self.assertNotEqual(self.archer2.unit.cord_y, old_pos[1])

    def test_warriorMoveFar(self):
        old_pos = (self.warrior2.unit.cord_x, self.warrior2.unit.cord_y)
        self.warrior2.move_far(self.hero_human.unit)

        self.assertNotEqual(self.archer2.unit.cord_x, old_pos[0])
        self.assertNotEqual(self.archer2.unit.cord_y, old_pos[1])

    def test_buildingDefend(self):
        old_pos = (self.archer1.unit.cord_x, self.archer1.unit.cord_y)
        self.archer1.defend(self.cuartel, self.army.war_units)

        self.assertLess(self.archer1.unit.cord_x, old_pos[0])
        self.assertLess(self.archer1.unit.cord_y, old_pos[1])

    def test_templeInRange(self):
        self.assertTrue(self.aux_warrior.temple_in_range(self.temple))
        self.assertFalse(self.archer1.temple_in_range(self.temple))

    def test_closestInRange(self):
        result = self.aux_warrior.closest_in_range(self.army.war_units)
        self.assertIsNone(result)

    def test_randomMove(self):
        self.assertIsNone(self.aux_archer.random_move())

    def test_distanceUnit(self):
        self.assertEqual(400, distance(self.aux_pet, self.aux_archer.unit))
        self.assertNotEqual(400, distance(self.warrior2, self.aux_archer.unit))

    def test_addUnit(self):
        self.assertIsInstance(self.villager1.unit, Human)

    def test_workingVillager(self):
        self.villager1.working = 0
        self.villager1.avanzar((0, 0), (0, 0), self.army)
        self.assertGreater(self.villager1.working, 0)

    def test_showStatistics(self):
        ret = self.sim.show_statistics(False)
        self.assertIsNone(ret)

    def test_setWinner(self):
        answer = self.sim.set_winner()
        self.assertIsInstance(answer, str)

    def test_setObjective(self):
        self.sim.objective = None

        self.sim.new_objective()
        self.assertIsInstance(self.sim.objective, list)
        self.assertIsInstance(self.sim.objective[0], int)
        self.assertIsInstance(self.sim.objective[1], str)

    def test_splitHumanDefenders(self):
        list1, list2, list3 = self.sim.split_defenders(self.army.war_units)

        self.assertIsInstance(list1, list)
        self.assertIsInstance(list2, list)
        self.assertIsInstance(list3, list)

        self.assertIn(self.warrior1, list1)

    def test_armyProperties(self):
        # listas de unidades
        self.assertIsInstance(self.army.war_units, list)
        self.assertIsInstance(self.army.complete_army, list)

        # aldeanos
        self.assertEqual(1, self.army.villager_qty)

        # cantidad de unidades
        self.assertIsInstance(self.army.total_units, int)

    def test_initialGoldProperty(self):
        # oro inicio
        self.assertEqual(800, self.army.gold)

    def test_armyBuildings(self):
        # todos sus edificaciones
        self.assertFalse(self.army.all_buildings)

        self.army.cuartel = self.cuartel
        self.army.torretas.append(self.torre)

        self.assertTrue(self.army.all_buildings)

        # si alguno esta en construccion
        for torre in self.army.torretas:
            torre.in_construction = True

        self.assertFalse(self.army.all_buildings)

    def test_armyCreationList(self):
        self.army.creation_list = list()

        self.army.set_creation_list()
        self.assertEqual(self.army.creation_list[0], "warrior")
        self.assertEqual(self.army.creation_list[-1], "pet")

        # tambien contiene arqueros
        self.assertIn("archer", self.army.creation_list)
        self.assertEqual(2, len([x for x in self.army.creation_list if x == "archer"]))

        # se crean 6 elementos
        self.assertEqual(len(self.army.creation_list), 6)

    def test_maxQtyUnits(self):
        # segun raza determina max unidades
        self.assertEqual(25, self.army.set_max_units())

    def test_creationCicle(self):
        # not all buildings
        ret1, ret2 = self.army.creation_cicle()
        self.assertIsNone(ret1)
        self.assertIsNone(ret2)

        # all buildings
        self.army.cuartel = self.cuartel
        self.army.torretas.append(self.torre)

        self.assertTrue(self.army.all_buildings)

        # not all villagers
        ret1, ret2 = self.army.creation_cicle()
        self.assertIsNone(ret1)
        self.assertIsNone(ret2)

    def test_heroArrival(self):
        old_time = self.army.time_for_hero

        # cuenta llegada del heroe
        self.army.hero_arrival()
        self.assertLess(old_time, self.army.time_for_hero)

    def test_newArmyUnit(self):
        self.army.cuartel = self.cuartel
        self.army.temple = self.temple

        # creacion de unidades
        self.assertIsInstance(self.army.new_unit('warrior'), Warrior)
        self.assertIsInstance(self.army.new_unit('archer'), Archer)
        self.assertIsInstance(self.army.new_unit('pet'), Pet)
        self.assertIsInstance(self.army.new_unit('villager'), Villager)
        self.assertIsInstance(self.army.new_unit('hero'), Hero)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(WarUnitsTest)
    unittest.TextTestRunner().run(suite)