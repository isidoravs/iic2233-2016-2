import gui
from gui.environment import Wall
from gui.tanks import Tank
from gui.power_ups import PowerUp, Explotion
from random import randint, choice
from math import sqrt
import time
import sys


class HackerTanks:

    def __init__(self):
        self.borders = list()
        self._bombs = list()
        self.walls = list()
        self.explotions = list()

        self.enemies = list()
        self.enemies_bullets = list()

        self.tank = None  # principal

        self.max_time = 0
        self.actual_time = 0  # segundos
        self.aux_timer = list()

        self._score = 200

        self.set_borders()
        self.set_walls(1)  # coordinar con etapas RR

        self.mode = None
        self.stage = None
        self.stages_passed = list()

        self.start_time = None
        self.game_over = False

        self.power_ups = list()

        self.death_score = self.set_death_score()

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, other):
        self._score = other

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

    def set_death_score(self):
        with open("constantes.txt", "r") as file:
            for line in file:
                if "deathScore" in line:
                    aux = line.strip().split(",")
                    return {"Beige": int(aux[1]), "Green": int(aux[2]),
                            "Red": int(aux[3]), "Black": int(aux[4])}

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
            for i in range(4):
                if i < 3:
                    new_wall = Wall("indestructible", pos=(95 + 97*i, 420))
                else:
                    new_wall = Wall("indestructible", pos=(163 + 97 * (i + 1), 420))
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

            to_add = list()
            to_add.extend([(wall.cord_x, y) for y in
                           range(wall.cord_y, wall.cord_y + wall.height())])
            to_add.extend([(wall.cord_x + wall.width(), y) for y in
                           range(wall.cord_y, wall.cord_y + wall.height())])
            to_add.extend([(x, wall.cord_y) for x in
                           range(wall.cord_x, wall.cord_x + wall.width())])
            to_add.extend([(x, wall.cord_y + wall.height()) for x in
                           range(wall.cord_x, wall.cord_x + wall.width())])

            gui.add_forbidden_cords(to_add)
        return

    def tick(self):
        if gui.end_game():
            time.sleep(2)
            sys.exit()

        if self.mode is None:
            self.check_game_info()
        else:
            if not self.game_over and not gui.is_paused():
                # mouse
                gui.track_mouse()

                for bullet in gui.bullets_list() + self.enemies_bullets:
                    bullet.shoot_move(gui.forbidden_cords(),
                                      self.enemies + [self.tank])
                    if bullet.to_remove:
                        if "Enemy" in bullet.kind:
                            self.enemies_bullets.remove(bullet)
                        else:
                            gui.remove_bullet(bullet)
                        bullet.deleteLater()

                    else:
                        for other in gui.bullets_list() + self.enemies_bullets:
                            if bullet != other:
                                if int(bullet.cord_x) in range(int(other.cord_x) - 5, int(other.cord_x) + 5):
                                    if int(bullet.cord_y) in range(int(other.cord_y) - 10, int(other.cord_y) + 10):
                                        # colision
                                        explotion = Explotion("bullet",
                                                              pos=(bullet.cord_x, bullet.cord_y),
                                                              exp=6,
                                                              size=(30, 30))
                                        self.explotions.append(explotion)
                                        gui.add_entity(explotion)

                                        for enemy in self.enemies:
                                            if self.distance(enemy, (bullet.cord_x, bullet.cord_y)) <= 30:
                                                enemy.health -= 5

                                        if self.distance(self.tank, (bullet.cord_x, bullet.cord_y)) <= 30:
                                            self.tank.health -= 5

                                        if "Enemy" in bullet.kind:
                                            self.enemies_bullets.remove(bullet)
                                        else:
                                            gui.remove_bullet(bullet)
                                        bullet.deleteLater()

                                        if "Enemy" in other.kind:
                                            self.enemies_bullets.remove(other)
                                        else:
                                            gui.remove_bullet(other)
                                        other.deleteLater()

                # dinamica de explosiones
                for explotion in self.explotions:
                    explotion.counter -= 1
                    if explotion.counter == 0:
                        self.explotions.remove(explotion)
                        explotion.deleteLater()

                # mantengo actualizado el tiempo
                self.actual_time = int(time.clock()) - gui.paused_time()

                if self.actual_time not in self.aux_timer:  # paso un segundo
                    self.aux_timer.append(self.actual_time)

                    # actions
                    if len(self.bombs) > 0:
                        self.update_bombs()

                    for tank in self.enemies:
                        if tank.color != "Beige":  # quieto
                            tank.movement += 1
                            if tank.direction is not None:
                                self.move_tank_center(tank)

                    # creacion de power ups, random
                    aux1 = randint(0, 20)
                    aux2 = randint(0, 20)
                    if aux1 == aux2:
                        self.show_power_up()

                    # cada dos segundos dispara enemigo
                    if self.actual_time % 2 == 0:
                        for enemy in self.enemies:
                            if enemy.in_vision(self.tank):
                                bullet = enemy.start_shooting()
                                self.enemies_bullets.append(bullet)
                                gui.add_entity(bullet)

                    # tanque principal choque
                    for enemy in self.enemies:
                        if self.distance(self.tank, (enemy.cord_x, enemy.cord_y)) <= 25:
                            self.tank.health -= 1
                            enemy.health -= 1

                forbidden = gui.forbidden_cords()
                for tank in self.enemies:
                    if tank.color == "Red" or tank.color == "Black":
                        old_cord = (tank.cord_x, tank.cord_y)
                        old_barrel_cord = (tank.barrel.cord_x, tank.barrel.cord_y)
                        tank.make_movement(self.tank)
                        if not self.valid_movement(tank, forbidden):
                            # caso especial tanque negro
                            if tank.color == "Black":
                                destructibles = [wall for wall in self.walls
                                                 if "indestructible" not in wall.kind]

                                for wall in destructibles:
                                    corners = [(wall.cord_x, wall.cord_y),
                                                    (wall.cord_x + wall.width(), wall.cord_y),
                                                    (wall.cord_x, wall.cord_y + wall.height()),
                                                    (wall.cord_x + wall.width(), wall.cord_y + wall.height())]

                                    for corner in corners:
                                        if self.distance(tank, corner) <= 100:
                                            self.walls.remove(wall)
                                            self.remove_forbidden_cords(wall)
                                            wall.deleteLater()
                                            return

                            tank.cord_x = old_cord[0]
                            tank.cord_y = old_cord[1]

                            tank.barrel.cord_x = old_barrel_cord[0]
                            tank.barrel.cord_y = old_barrel_cord[1]
                    else:
                        tank.make_movement(self.tank)

                # atrapa un power_up
                for powerup in self.power_ups:
                    if powerup.cord_x in range(self.tank.cord_x, self.tank.cord_x + 45):
                        if powerup.cord_y in range(self.tank.cord_y, self.tank.cord_y + 45):
                            if powerup.kind == "coin":
                                self.score += 250
                                gui.score(self.score)
                            elif "Explosive" in powerup.kind:
                                self.tank.bullets.extend(["e"] * 3)
                            elif "Penetrante" in powerup.kind:
                                self.tank.bullets.extend(["p"] * 3)
                            elif "Ralentizante" in powerup.kind:
                                self.tank.bullets.extend(["r"] * 3)

                            self.power_ups.remove(powerup)
                            powerup.deleteLater()
                            break

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
                        gui.score(self.score)
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
                        gui.score(self.score)

                        # restart
                        self.tank.deleteLater()
                        self.tank.barrel.deleteLater()
                        self.tank = None

                        self.stage = next_stage
                        self.set_walls(next_stage)
                        self.set_max_time(next_stage)
                        self.start_stage()

                        gui.set_level(self.stage)

                        self.actual_time = 0  # segundos
                        self.aux_timer = list()

                        # info
                        gui.set_bombs_left(self.tank)
                        gui.set_next_bullets(self.tank)

                # revisa enemigos muertos
                deaths = [enemy for enemy in self.enemies if enemy.health <= 0]
                for dead in deaths:
                    self.score += self.death_score[dead.color]
                    gui.set_score(str(self.score))
                    self.enemies.remove(dead)
                    dead.barrel.deleteLater()
                    dead.deleteLater()

                # RR propio hp
                if self.tank.health <= 0:
                    # game over
                    print("u dead")
                    self.game_over = True

                # mantiene actualizado
                actual = gui.current_score()
                self.score = actual
                gui.set_score(str(self.score))

                gui.set_next_bullets(self.tank)

            elif self.game_over:  # no funciona RR
                self.tank.barrel.hide()
                self.tank.barrel.deleteLater()
                self.tank.deleteLater()
                self.tank = None

                for wall in self.walls:
                    wall.deleteLater()

                for enemy in self.enemies:
                    enemy.barrel.deleteLater()
                    enemy.deleteLater()

                self.set_walls(1)
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

                # explotion
                explotion = Explotion("bomb", pos=(bomb.cord_x, bomb.cord_y))
                self.explotions.append(explotion)
                gui.add_entity(explotion)
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
                        self.remove_forbidden_cords(wall)
                        wall.deleteLater()

    def remove_forbidden_cords(self, wall):
        to_remove = list()
        to_remove.extend([(wall.cord_x, y) for y in
                          range(wall.cord_y,
                                wall.cord_y + wall.height())])
        to_remove.extend([(wall.cord_x + wall.width(), y) for y in
                          range(wall.cord_y,
                                wall.cord_y + wall.height())])
        to_remove.extend([(x, wall.cord_y) for x in
                          range(wall.cord_x,
                                wall.cord_x + wall.width())])
        to_remove.extend([(x, wall.cord_y + wall.height()) for x in
                          range(wall.cord_x,
                                wall.cord_x + wall.width())])

        gui.remove_forbidden_cords(to_remove)
        return

    def valid_movement(self, tank, forbidden):
        all_borders = self.all_tank_borders(tank)

        x_pos = tank.cord_x
        y_pos = tank.cord_y

        if x_pos < 88 or x_pos + tank.width() > 750 \
                or y_pos < 83 or y_pos + tank.width() > 597:  # bordes
            return False

        for cord in all_borders:
            if cord in forbidden:
                return False

        return True

    def all_tank_borders(self, tank):
        all_borders = list()
        all_borders.extend([(tank.cord_x, y) for y in
                            range(int(tank.cord_y),
                                  int(tank.cord_y + tank.size[0]))])
        all_borders.extend([(tank.cord_x + tank.size[0], y) for y in
                            range(int(tank.cord_y),
                                  int(tank.cord_y + tank.size[0]))])
        all_borders.extend([(x, tank.cord_y) for x in
                            range(int(tank.cord_x),
                                  int(tank.cord_x + tank.size[0]))])
        all_borders.extend([(x, tank.cord_y + tank.size[0]) for x in
                            range(int(tank.cord_x),
                                  int(tank.cord_x + tank.size[0]))])
        return all_borders

    def show_power_up(self):
        power_up = ["coin", "bulletExplosive", "bulletPenetrante",
                    "bulletRalentizante"]
        positions = [(320, 305), (325, 515), (515, 400)]

        aux = choice(power_up)
        if aux == "coin":
            size = (25, 25)
        else:
            size = (16, 28)

        to_show = PowerUp(aux, pos=choice(positions), size=size)
        self.power_ups.append(to_show)
        gui.add_entity(to_show)
        return

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

    def distance(self, obj, cord):
        return sqrt((obj.cord_x - cord[0]) ** 2 + (obj.cord_y - cord[1]) ** 2)


if __name__ == "__main__":
    game = HackerTanks()
    gui.run(game.tick)
