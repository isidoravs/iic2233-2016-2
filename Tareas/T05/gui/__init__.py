from .main_window import MainWindow
from PyQt4.QtGui import QApplication, QWidget


__app = QApplication([])
__main_widget = MainWindow()


def ppal_bombs():
    return __main_widget._bombs


def delete_bomb(bomb):
    __main_widget._bombs.remove(bomb)


def is_paused():
    return __main_widget.is_paused


def end_game():
    return __main_widget.end_game


def paused_time():
    return __main_widget.paused_time


def current_score():
    return __main_widget.score


def show_explotion(position):
    # usar QTimers
    __main_widget.show_explotion(position)


def add_entity(entity):
    __main_widget.add_entity(entity)
    entity.move(entity.cord_x, entity.cord_y)
    if hasattr(entity, "barrel"):  # tanque
        __main_widget.add_entity(entity.barrel)
        entity.barrel.move(entity.barrel.cord_x, entity.barrel.cord_y)


def bullets_list():
    return __main_widget.all_bullets


def remove_bullet(bullet):
    __main_widget.all_bullets.remove(bullet)


def get_info():
    return __main_widget.mode, __main_widget.stage


def start_explotion(position):
    __main_widget.start_explotion(pos=position)


def forbidden_cords():
    return __main_widget.forbidden_cords


def flying_portals():
    return __main_widget.flying_portals


def remove_portal(portal):
    __main_widget.flying_portals.remove(portal)


def restart_game():
    __main_widget.restart_game()


def set_score(score):
    __main_widget.set_score(score)


def set_level(level):
    __main_widget.set_level("Stages", level)


def score(score):
    __main_widget.score = score


def add_forbidden_cords(cords_list):
    for cord in cords_list:
        __main_widget.forbidden_cords.append(cord)


def track_mouse():
    __main_widget.move_barrel()


def remove_forbidden_cords(cords_list):
    for cord in cords_list:
        __main_widget.forbidden_cords.remove(cord)


def erase_forbidden_cords():
    __main_widget.forbidden_cords = list()


def main_tank(tank):
    __main_widget.tank = tank


def set_time(time_left):
    __main_widget.set_time(time_left)


def game_over_survival(score):
    __main_widget.game_over_survival(score)


def set_bombs_left(tank):
    __main_widget.set_bombs_left(tank)


def set_next_bullets(tank):
    __main_widget.set_next_bullets(tank)


def set_message(message):
    __main_widget.set_message(message)


def run(main, delay=25):
    __main_widget.show()
    __main_widget.startMain(main, delay)
    __app.exec()
