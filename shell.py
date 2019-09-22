import select
import sys
import termios
import tty

import core

# moves = [[0, -1], [0, -1], [0, -1], [0, -1], [0, -1], [0, -1], [0, -1], [0, -1], [0, -1], [0, -1], [1, 1], [0, -1], [0, -1], [0, -1], [0, -1], [0, -1], [0, -1], [0, -1]]

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

while True:
    pressed_key = getch(timeout=0.2)
    if pressed_key in keys_table:
        core.player.edit_y_pos(0, keys_table[pressed_key][0])
        core.player.edit_x_pos(0, keys_table[pressed_key][1])
        core.update_player()
        core.clear_area()
        core.draw_table()

