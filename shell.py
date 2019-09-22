import select
import sys
import termios
import tty
from time import sleep

import core

# moves = [[0, -1], [0, -1], [0, -1], [0, -1], [0, -1], [0, -1], [0, -1], [0, -1], [0, -1], [0, -1], [1, 1], [0, -1], [0, -1], [0, -1], [0, -1], [0, -1], [0, -1], [0, -1]]
sleep_time = 0.1

core.clear_area()
core.load_map('default_map')
core.update_player()
core.draw_table()

# for element in moves:
#     # core.clear_area()
#     print(element[0])
#     core.player.edit_y_pos(0, element[0])
#     core.player.edit_x_pos(0, element[1])
#     core.update_player()
#     core.draw_table()
#     sleep(sleep_time)


# This two functions are copied from StackOverflow
def setup_term(fd, when=termios.TCSAFLUSH):
    mode = termios.tcgetattr(fd)
    mode[tty.LFLAG] = mode[tty.LFLAG] & ~(termios.ECHO | termios.ICANON)
    termios.tcsetattr(fd, when, mode)


def getch(timeout=None):
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        setup_term(fd)
        try:
            rw, wl, xl = select.select([fd], [], [], timeout)
        except select.error:
            return
        if rw:
            return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


keys_table = {
    'w': [-1, 0],  # y, x
    'a': [0, -1],
    's': [1, 0],
    'd': [0, 1]
}


def single_player():
    try:
        while True:
            # sleep(sleep_time)
            core.clear_area()
            core.draw_table()
            pressed_key = getch(timeout=0.2)
            if pressed_key in keys_table:
                core.player.edit_y_pos(0, keys_table[pressed_key][0])
                core.player.edit_x_pos(0, keys_table[pressed_key][1])
                core.update_player()
                core.clear_area()
                core.draw_table()
    except KeyboardInterrupt:
        menu('You sure you want to exit?', {'Yes': exit_from_game, 'No': single_player}, show_hint=True)()


def multi_player():
    print('Sorry, this function is unavailable now')


def exit_from_game():
    print('Okay :( Bye, my friend')
    raise Exception


def _draw_menu(text, options, active_option):
    index = 0
    print(text)
    for option in options:
        print('> ' + option if index == active_option else option)
        index += 1


def menu(text, options, show_hint=True):      # dict with codes
    core.clear_area()
    active_option = 0
    chose = False
    keys = {
        'w': -1,
        's': 1
    }
    if show_hint:
        text = 'Hint: w and s to scroll, f to choose\n' + text
    _draw_menu(text, options, active_option)
    while not chose:
        pressed_key = getch()
        if pressed_key in ['w', 's']:
            active_option += keys[pressed_key]
            try:
                list(options)[active_option]
            except IndexError:
                active_option += -keys[pressed_key]
            finally:
                if active_option < 0:
                    active_option = 0
            core.clear_area()
            _draw_menu(text, options, active_option)
        elif pressed_key == 'f':
            chose = True

    return options[list(options)[active_option]]


if __name__ == '__main__':
    try:
        chose = menu('Choose game mode:', {'Singleplayer': single_player, 'Multiplayer': multi_player}, show_hint=True)
        print('Starting the game. Please, wait...')
        chose()
    except Exception:
        pass

