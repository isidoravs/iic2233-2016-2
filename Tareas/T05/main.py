import gui
from gui.environment import Wall
from gui.tanks import Tank
import time
import sys


class HackerTanks:

    def __init__(self):
        self.borders = list()
        self.coins = list()
        self._bombs = list()
        self.walls = list()

        self.enemies = list()

        self.tank = None  # principal

        self.max_time = 0
        self.actual_time = 0  # segundos
        self.aux_timer = list()

        self.score = 0

        self.set_borders()
        self.set_walls(1)  # coordinar con etapas RR

        self.mode = None
        self.stage = None
        self.stages_passed = list()

        self.start_time = None
        self.game_over = False

    @property
    def paused_time(self):
        return gui.paused_time()

    @property
    def bombs(self):  # todas las bombas RR
        return self._bombs + gui.ppal_bombs()

    def set_borders(self):
        for i in range(8):  # bordes
            new_border_up = Wall("indestructible", pos=(30 + 97*i, 30))
            new_border_down = Wall("indestructible", pos=(30 + 97*i, 590))
            self.borders.append(new_border_up)
            gui.add_entity(new_border_up)

            self.borders.append(new_border_down)
            gui.add_entity(new_border_down)

        for i in range(5):  # bordes
            new_border_right = Wall("indestructible_inv", pos=(30, 90 + 100*i), size=(66, 99))
            new_border_left = Wall("indestructible_inv", pos=(742, 90 + 100*i), size=(66, 99))

            self.borders.append(new_border_right)
            gui.add_entity(new_border_right)

            self.borders.append(new_border_left)
            gui.add_entity(new_border_left)

    def set_walls(self, level):
        for old_wall in self.walls:  # eliminar anteriores
            old_wall.deleteLater()
        gui.erase_forbidden_cords()

        self.walls = list()

        # agregar proximas
        if level == 1:
            return

        elif level == 2:
            for i in range(3):
                new_wall = Wall("destructible_inv", pos=(370, 180 + 97 * i),
                                size=(66, 99))
                self.walls.append(new_wall)

        elif level == 3:  # solo una pared RR
            for i in range(4):
                new_wall = Wall("indestructible", pos=(280 + 97*i, 240))
                self.walls.append(new_wall)

        elif level == 4:
            for i in range(3):
                new_wall_1 = Wall("destructible_inv", pos=(340, 180 + 97 * i),
                                size=(66, 99))
                self.walls.append(new_wall_1)

                if i < 2:
                    new_wall_2 = Wall("indestructible", pos=(406 + 97*i, 320))
                    self.walls.append(new_wall_2)

        elif level == 5:
            for i in range(4):
                new_wall = Wall("destructible_inv", pos=(250, 141 + 97 * i),
                                  size=(66, 99))
                self.walls.append(new_wall)

            new_wall_1 = Wall("destructible", pos=(150, 200))
            self.walls.append(new_wall_1)

            for i in range(2):
                new_wall = Wall("indestructible", pos=(315 + 97*i, 400))
                self.walls.append(new_wall)

        elif level == 6:
            for i in range(5):
                if i < 3:
                    new_wall = Wall("indestructible", pos=(95 + 97*i, 450))
                else:
                    new_wall = Wall("indestructible", pos=(163 + 97 * i, 450))
                self.walls.append(new_wall)

            for i in range(3):
                new_wall = Wall("destructible_inv", pos=(388, 220 + 97 * i),
                                size=(66, 99))
                self.walls.append(new_wall)

        elif level == 7:
            for i in range(3):
                new_wall = Wall("destructible", pos=(178 + 97 * i, 440))
                self.walls.append(new_wall)

            for i in range(4):
                new_wall_1 = Wall("destructible_inv", pos=(550, 140 + 97*i),
                                  size=(66, 99))
                self.walls.append(new_wall_1)

                if i < 1:
                    new_wall_2 = Wall("destructible_inv", pos=(180, 340),
                                      size=(66, 99))
                    self.walls.append(new_wall_2)

        elif level == 8:
            for i in range(4):
                if i < 3:
                    new_wall = Wall("indestructible", pos=(200 + 97*i, 180))
                else:
                    new_wall = Wall("indestructible", pos=(267 + 97 * i, 180))

                self.walls.append(new_wall)

            for i in range(3):
                new_wall_1 = Wall("indestructible_inv", pos=(200, 239 + 97*i),
                                  size=(66, 99))
                self.walls.append(new_wall_1)

                if i < 2:
                    new_wall_2 = Wall("indestructible_inv", pos=(493, 178 + 97 * i),
                                      size=(66, 99))
                    self.walls.append(new_wall_2)

        else:  # survival, regenera cad cierto tiempo
            for i in range(5):
                if i < 2:
                    new_wall = Wall("indestructible", pos=(95 + 97 * i, 160))
                elif i < 4:
                    new_wall = Wall("indestructible", pos=(165 + 97 * i, 160))
                else:
                    new_wall = Wall("indestructible", pos=(165 + 97 * i, 355))

                self.walls.append(new_wall)

            for i in range(3):
                new_wall_1 = Wall("destructible_inv", pos=(293, 158 + 97 * i),
                                  size=(66, 99))
                self.walls.append(new_wall_1)

                if i < 2:
                    new_wall_2 = Wall("destructible_inv", pos=(556, 158 + 97 * i),
                                      size=(66, 99))
                    self.walls.append(new_wall_2)

            for i in range(2):
                new_wall = Wall("indestructible", pos=(210 + 97 * i, 452))
                self.walls.append(new_wall)

        for wall in self.walls:
            gui.add_entity(wall)

            gui.add_forbidden_cords([(x, y)
                                     for x in range(wall.cord_x, wall.cord_x + wall.width())
                                     for y in range(wall.cord_y, wall.cord_y + wall.height())])
        return

    def tick(self):
        if gui.end_game():
            time.sleep(2)
            sys.exit()

        if self.mode is None:
            self.check_game_info()
        else:
            if not self.game_over and not gui.is_paused():
                # mantengo actualizado el tiempo
                self.actual_time = int(time.clock()) - gui.paused_time()

                if self.actual_time not in self.aux_timer:  # paso un segundo
                    self.aux_timer.append(self.actual_time)

                    # actions
                    if len(self.bombs) > 0:
                        self.update_bombs()

                    # estados de movimiento
                    self.tank.movement += 1
                    for tank in self.enemies:
                        if tank.color != "Beige":  # quieto
                            tank.movement += 1
                            if tank.direction is not None:
                                self.move_tank_center(tank)

                for tank in self.enemies:
                    tank.make_movement(self.tank)

                if self.mode == "Stages":
                    lapse = self.actual_time - self.start_time
                    time_left = self.max_time - lapse
                    gui.set_time(time_left)
                    if time_left == 0:  # fin del tiempo RR
                        self.game_over = True
                        gui.set_message("GAME OVER")
                else:
                    gui.set_time(self.actual_time)

                # reviso si paso etapa
                if self.mode == "Stages" and len(self.enemies) == 0:
                    self.stages_passed.append(self.stage)
                    if len(self.stages_passed) == 8:
                        # dio vuelta
                        gui.set_message("All stages complete!")
                        self.score += 1000
                        self.game_over = True

                    else:
                        next_stage = self.stage + 1
                        if self.stage == 8:
                            for i in range(1, 8):
                                if i not in self.stages_passed:
                                    next_stage = i
                                    break
                        # score
                        self.score += lapse
                        self.score += self.tank.health

                        # restart
                        self.tank.deleteLater()
                        self.tank = None

                        self.stage = next_stage
                        self.set_walls(next_stage)
                        self.set_max_time(next_stage)
                        self.start_stage()

                        self.actual_time = 0  # segundos
                        self.aux_timer = list()

                        # info
                        gui.set_bombs_left(self.tank)
                        gui.set_next_bullets(self.tank)

                # mantiene actualizado
                gui.set_score(str(self.score))

            elif self.game_over:  # no funciona RR
                self.tank.deleteLater()
                self.tank = None

                for wall in self.walls:
                    wall.deleteLater()

                for enemy in self.enemies:
                    enemy.hide()
                    enemy.deleteLater()

                self.set_walls(1)
                self.coins = list()
                self._bombs = list()
                self.enemies = list()

                self.max_time = 0
                self.actual_time = 0  # segundos
                self.aux_timer = list()
                self.score = 0

                self.mode = None
                self.stage = None
                self.stages_passed = list()

                self.start_time = None
                self.game_over = False
                gui.restart_game()

    def update_bombs(self):
        for bomb in self.bombs:
            bomb.health -= 1  # time_to_explode en bombas
            if bomb.health == 0:

                if bomb in gui.ppal_bombs():
                    gui.delete_bomb(bomb)
                else:
                    self._bombs.remove(bomb)

                # explota QTimers RR
                # gui.show_explotion((bomb.cord_x, bomb.cord_y))
                self.bomb_destruction(bomb)

                # elimino
                bomb.deleteLater()

    def bomb_destruction(self, bomb):
        x_limit1 = bomb.cord_x - bomb.attack_range - 100
        x_limit2 = bomb.cord_x + bomb.attack_range + 100
        y_limit1 = bomb.cord_y - bomb.attack_range - 100
        y_limit2 = bomb.cord_y + bomb.attack_range + 100
        for enemy in self.enemies:
            if x_limit1 < enemy.cord_x and x_limit2 > enemy.cord_x:
                if y_limit1 < enemy.cord_y and y_limit2 > enemy.cord_y:
                    enemy.health -= bomb.harm
                    enemy.health += enemy.resistance

        if x_limit1 < self.tank.cord_x and x_limit2 > self.tank.cord_x:
            if y_limit1 < self.tank.cord_y and y_limit2 > self.tank.cord_y:
                self.tank.health -= bomb.harm
                self.tank.health += self.tank.resistance

        for wall in self.walls:
            if "indestructible" not in wall.kind:
                x_limit1 = bomb.cord_x - bomb.attack_range - wall.width()
                x_limit2 = bomb.cord_x + bomb.attack_range + wall.width()
                y_limit1 = bomb.cord_y - bomb.attack_range - wall.height()
                y_limit2 = bomb.cord_y + bomb.attack_range + wall.height()
                if x_limit1 < wall.cord_x and x_limit2 > wall.cord_x:
                    if y_limit1 < wall.cord_y and y_limit2 > wall.cord_y:
                        self.walls.remove(wall)
                        gui.remove_forbidden_cords(
                            [(x, y) for x in range(wall.cord_x, wall.cord_x + wall.width())
                             for y in range(wall.cord_y, wall.cord_y + wall.height())])

                        wall.deleteLater()

    def check_game_info(self):
        if self.mode is not None:
            return
        aux_mode, aux_stage = gui.get_info()
        if aux_mode is not None:  # acaba de cambiar
            self.mode = aux_mode
            self.stage = aux_stage
            self.set_walls(aux_stage)
            self.set_max_time(aux_stage)
            self.start_stage()

            # info
            gui.set_bombs_left(self.tank)
            gui.set_next_bullets(self.tank)

    def start_stage(self):  # comienza etapa
        # crear tanque
        self.tank = Tank("Blue", 1, self.tank_stats(0), hp=200)
        self.tank.angle = 90
        self.tank.barrel.angle = 90
        if self.mode == "Stages":
            self.tank.bullets *= int(self.stage)
        else:
            self.tank.bullets *= 8
        gui.add_entity(self.tank)
        gui.main_tank(self.tank)

        if self.stage == 1:
            tank1 = Tank("Beige", 1, self.tank_stats(1), pos=(600, 120))  # quieto
            tank2 = Tank("Red", 1, self.tank_stats(3), pos=(480, 480))  # guiador

            tank1.angle = 270
            tank1.barrel.angle = 270

            self.enemies.append(tank1)
            self.enemies.append(tank2)

            gui.add_entity(tank1)
            gui.add_entity(tank2)

        elif self.stage == 2:
            tank1 = Tank("Beige", 1, self.tank_stats(1), pos=(160, 520))  # quieto
            tank2 = Tank("Red", 1, self.tank_stats(3), pos=(590, 110))  # guiador
            tank3 = Tank("Red", 1, self.tank_stats(3), pos=(470, 360))  # guiador

            self.enemies.append(tank1)
            self.enemies.append(tank2)
            self.enemies.append(tank3)

            gui.add_entity(tank1)
            gui.add_entity(tank2)
            gui.add_entity(tank3)

        elif self.stage == 3:
            tank1 = Tank("Beige", 1, self.tank_stats(1), pos=(630, 100))  # quieto
            tank2 = Tank("Beige", 1, self.tank_stats(1), pos=(430, 300))  # quieto
            tank3 = Tank("Red", 1, self.tank_stats(3), pos=(530, 180))  # guiador
            tank4 = Tank("Red", 1, self.tank_stats(3), pos=(580, 520))  # guiador
            tank5 = Tank("Green", 1, self.tank_stats(2), pos=(170+50, 460),
                         center=(170, 460), radio=50, direction="x>")  # circulo

            tank1.angle = 270
            tank1.barrel.angle = 270
            tank2.angle = 180
            tank2.barrel.angle = 180
            tank4.angle = 315
            tank4.barrel.angle = 315

            self.enemies.append(tank1)
            self.enemies.append(tank2)
            self.enemies.append(tank3)
            self.enemies.append(tank4)
            self.enemies.append(tank5)

            gui.add_entity(tank1)
            gui.add_entity(tank2)
            gui.add_entity(tank3)
            gui.add_entity(tank4)
            gui.add_entity(tank5)

        elif self.stage == 4:
            tank1 = Tank("Red", 1, self.tank_stats(3), pos=(410, 260))  # guiador
            tank2 = Tank("Red", 1, self.tank_stats(3), pos=(410, 390))  # guiador
            tank3 = Tank("Red", 1, self.tank_stats(3), pos=(630, 100))  # guiador
            tank4 = Tank("Green", 1, self.tank_stats(2), pos=(150+25, 400),
                         center=(150, 500), radio=25, direction="y<")  # circulo
            tank5 = Tank("Green", 1, self.tank_stats(2), pos=(580+50, 460),
                         center=(580, 460), radio=50, direction="x<")  # circulo

            tank2.angle = 90
            tank2.barrel.angle = 90
            tank3.angle = 270
            tank3.barrel.angle = 270

            self.enemies.append(tank1)
            self.enemies.append(tank2)
            self.enemies.append(tank3)
            self.enemies.append(tank4)
            self.enemies.append(tank5)

            gui.add_entity(tank1)
            gui.add_entity(tank2)
            gui.add_entity(tank3)
            gui.add_entity(tank4)
            gui.add_entity(tank5)

        elif self.stage == 5:
            tank1 = Tank("Beige", 1, self.tank_stats(1), pos=(100, 520))  # quieto
            tank2 = Tank("Beige", 1, self.tank_stats(1), pos=(310, 465))  # quieto
            tank3 = Tank("Beige", 1, self.tank_stats(1), pos=(380, 340))  # quieto
            tank4 = Tank("Red", 1, self.tank_stats(3), pos=(620, 180))  # guiador
            tank5 = Tank("Red", 1, self.tank_stats(3), pos=(630, 480))  # guiador
            tank6 = Tank("Red", 1, self.tank_stats(3), pos=(160, 340))  # guiador
            tank7 = Tank("Green", 1, self.tank_stats(2), pos=(550+55, 300),
                         center=(550, 300), radio=55, direction="x<")  # circulo
            tank8 = Tank("Green", 1, self.tank_stats(2), pos=(400+35, 200),
                         center=(400, 200), radio=35, direction="x>")  # circulo

            tank2.angle = 90
            tank3.angle = 45
            tank5.angle = 315
            tank6.angle = 270
            tank2.barrel.angle = 90
            tank3.barrel.angle = 45
            tank5.barrel.angle = 315
            tank6.barrel.angle = 270

            self.enemies.append(tank1)
            self.enemies.append(tank2)
            self.enemies.append(tank3)
            self.enemies.append(tank4)
            self.enemies.append(tank5)
            self.enemies.append(tank6)
            self.enemies.append(tank7)
            self.enemies.append(tank8)

            gui.add_entity(tank1)
            gui.add_entity(tank2)
            gui.add_entity(tank3)
            gui.add_entity(tank4)
            gui.add_entity(tank5)
            gui.add_entity(tank6)
            gui.add_entity(tank7)
            gui.add_entity(tank8)

        elif self.stage == 6:
            tank1 = Tank("Black", 1, self.tank_stats(4), hp=100,
                         size=(55, 55), pos=(160, 515))  # grande
            tank1.angle = 90
            tank1.barrel.angle = 90

            self.enemies.append(tank1)
            gui.add_entity(tank1)

        elif self.stage == 7:
            tank1 = Tank("Beige", 1, self.tank_stats(1), pos=(490, 270))  # quieto
            tank2 = Tank("Red", 1, self.tank_stats(3), pos=(180, 500))  # guiador
            tank3 = Tank("Black", 1, self.tank_stats(4),
                         hp=100, size=(55, 55), pos=(630, 520))  # grande

            tank1.angle = 315
            tank2.angle = 270
            tank1.barrel.angle = 315
            tank2.barrel.angle = 270

            self.enemies.append(tank1)
            self.enemies.append(tank2)
            self.enemies.append(tank3)

            gui.add_entity(tank1)
            gui.add_entity(tank2)
            gui.add_entity(tank3)

        elif self.stage == 8:
            tank1 = Tank("Beige", 1, self.tank_stats(1), pos=(100, 530))  # quieto
            tank2 = Tank("Beige", 1, self.tank_stats(1), pos=(270, 250))  # quieto
            tank3 = Tank("Red", 1, self.tank_stats(3), pos=(630, 100))  # guiador
            tank4 = Tank("Green", 1, self.tank_stats(2), pos=(550+20, 450),
                         center=(550, 450), radio=20, direction="x<")  # circulo
            tank5 = Tank("Green", 1, self.tank_stats(2), pos=(350+60, 450),
                         center=(350, 450), radio=60, direction="y<")  # circulo

            tank2.angle = 180
            tank3.angle = 270
            tank2.barrel.angle = 180
            tank3.barrel.angle = 270

            self.enemies.append(tank1)
            self.enemies.append(tank2)
            self.enemies.append(tank3)
            self.enemies.append(tank4)
            self.enemies.append(tank5)

            gui.add_entity(tank1)
            gui.add_entity(tank2)
            gui.add_entity(tank3)
            gui.add_entity(tank4)
            gui.add_entity(tank5)

        else:  # survival
            # inicia con un tanque guiador
            tank1 = Tank("Red", 1, self.tank_stats(3), pos=(500, 470))  # guiador
            tank1.angle = 90
            tank1.barrel.angle = 90

            self.enemies.append(tank1)
            gui.add_entity(tank1)
        return

    def tank_stats(self, ide):
        with open("constantes.txt", "r") as file:
            for line in file:
                aux = line.strip().split(",")
                if aux[0] == "stats" + str(ide):
                    return [int(x) for x in aux[1:]]

    def move_tank_center(self, tank):
        old_center = tank.center
        if tank.direction == "x>":
            if tank.cord_x + tank.radio == 700:
                tank.direction = "x<"
            else:
                tank.center = (old_center[0] + 2, old_center[1])

        elif tank.direction == "x<":
            if tank.cord_x + tank.radio == 100:
                tank.direction = "x>"
            else:
                tank.center = (old_center[0] - 2, old_center[1])

        elif tank.direction == "y>":
            if tank.cord_y + tank.radio == 550:
                tank.direction = "y<"
            else:
                tank.center = (old_center[0], old_center[1] + 2)

        elif tank.direction == "y<":
            if tank.cord_y + tank.radio == 100:
                tank.direction = "y>"
            else:
                tank.center = (old_center[0], old_center[1] - 2)

    def set_max_time(self, stage):
            with open("constantes.txt", "r") as file:
                for line in file:
                    aux = line.strip().split(",")
                    if "timeMax" in aux[0] and aux[0][-1] == str(stage):
                        self.max_time = int(aux[1])
                        gui.set_time(aux[1])
                        self.start_time = int(time.clock())
                        return

    def game_over_survival(self):
        gui.game_over_survival(self.score)


if __name__ == "__main__":
    game = HackerTanks()
    gui.run(game.tick)
