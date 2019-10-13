import os
import platform
import select
import sys
import termios
import tty


version = '0.0.1'


cls = 'cls' if platform.system().lower() == "windows" else 'clear'  # only windows uses cls. So, this code will work with windows, linux and
# macOS


class var:
    bottom_text = []


def setup_term(fd, when=termios.TCSAFLUSH):
    mode = termios.tcgetattr(fd)
    mode[tty.LFLAG] = mode[tty.LFLAG] & ~(termios.ECHO | termios.ICANON)
    termios.tcsetattr(fd, when, mode)


def text(bottom_text):    # list, list
    # overlay will be at the bottom of the play field
    var.bottom_text.append(bottom_text)


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


def clear_area():
    os.system(cls)


def _draw_menu(menu_text, options, active_option):
    index = 0
    print(menu_text)
    for option in options:
        print('> ' + option if index == active_option else option)
        index += 1


def menu(menu_text, options, show_hint=True):      # dict with codes
    clear_area()
    active_option = 0
    chose = False
    keys = {
        'w': -1,
        's': 1
    }
    if show_hint:
        menu_text = 'Hint: w and s to scroll, f to choose\n' + menu_text
    _draw_menu(menu_text, options, active_option)
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
            clear_area()
            _draw_menu(menu_text, options, active_option)
        elif pressed_key == 'f':
            chose = True

    return options[list(options)[active_option]]


def draw_table(map_content, dict_of_symbols):
    triggers = []

    for element in map_content:
        element = element[1:]
        current_line = ''
        for each in element:
            try:
                current_line += dict_of_symbols[each]
            except KeyError:
                pass
        print(current_line)
    for element in var.bottom_text:
        print(element)
    #     if element.startswith('trigger::'):
    #         triggers.append(element)
    #         continue
    #     print(element)
    # for trigger in triggers:
    #     trigger_type = trigger.split('::')[1].split('|')[0]
    #     trigger_action = trigger.split('::')[1].split('|')[1]

