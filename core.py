import textengine as txt
import physicengine as physic
import platform
import os


version = '0.0.1'

cls = 'cls' if platform.system().lower() == "windows" else 'clear'  # it's be work on mac, don't worry )))


class area:
    # def __setattr__(self, key, value):
    #     # var.last_player_move = []
    #     pass

    height = 17
    width = 33
    content = []
    info = {'name': '', 'description': ''}


class last_pos:
    def edit_y(self, y):
        if y in [1, -1]:
            last_pos.__y += y

    def edit_x(self, x):
        if x in [1, -1]:
            last_pos.__x += x

    def get_y(self):
        return last_pos.__y

    def get_x(self):
        return last_pos.__x

    __y = 10
    __x = 29


class player:
    def edit_x_pos(self, x):
        if area.content[player.__current_y][player.__current_x + x] != 0:
            return 'collision'
        if x in [1, -1]:
            last_pos.edit_x(0, player.__current_x)
            area.content[player.__current_y][player.__current_x] = 0
            player.__current_x += x
            update_player()

    def edit_y_pos(self, y):
        if area.content[player.__current_y + y][player.__current_x] != 0:
            return 'collision'
        if y in [1, -1]:
            last_pos.edit_y(0, player.__current_y)
            area.content[player.__current_y][player.__current_x] = 0
            player.__current_y += y
            update_player()

    def get_y(self):
        return player.__current_y

    def get_x(self):
        return player.__current_x

    __current_x = 29    # also used for spawn point at the game beginning
    __current_y = 10
    model = '☉'
    model_index = 7


class var:
    actions = []


class teleport:
    @staticmethod
    def player(to_pos):
        if type(to_pos) == str:
            to_pos = teleport.from_str_to_coords(to_pos)
        pass

    @staticmethod
    def player_to_map(map_name, pos):
        if type(pos) == str:
            pos = teleport.from_str_to_coords(pos)
        pass

    @staticmethod
    def object(to_pos):
        if type(to_pos) == str:
            to_pos = teleport.from_str_to_coords(to_pos)
        pass

    @staticmethod
    def object_to_map(map_name, pos):
        if type(pos) == str:
            pos = teleport.from_str_to_coords(pos)
        pass

    @staticmethod
    def from_str_to_coords(pos):
        coords = pos.split('|')
        return [coords[0], coords[1]]


class trigger:
    actions = {}
    keys = {
        'print': print,
        'input': input,
        'tp_player': teleport.player,
        'tp_object': teleport.object
    }

    @staticmethod
    def add(name, key, abs_pos):    # str, int, list
        if name not in trigger.actions:
            trigger.actions[name] = {'updates': [], 'trigger_abs_pos': abs_pos, 'map_object_before_trigger': area.content[abs_pos[0]][abs_pos[1]]}

        area.content[abs_pos[0]][abs_pos[1]] = key

    @staticmethod
    def remove(name):
        area.content[trigger.actions[name]['trigger_abs_pos'][0]][trigger.actions[name]['trigger_abs_pos'][1]] = trigger.actions[name]['map_object_before_trigger']

    @staticmethod
    def update(key, value):
        if key in trigger.actions:
            trigger.actions[key] = value

    @staticmethod
    def get_all_pos():
        result = []
        for element in trigger.actions:
            result.append(trigger.actions[element]['trigger_abs_pos'])

        return result


def return_player_to_last_coord():
    player.edit_y_pos(0, last_pos.get_y(0))
    player.edit_x_pos(0, last_pos.get_x(0))
    area.content[last_pos.get_y(0)][last_pos.get_x(0)] = 0


def update_player():
    if physic.iscollision([player.get_y(0), player.get_x(0)]):
        # return_player_to_last_coord()
        return 'collision-object'

    area.content[player.get_y(0)][player.get_x(0)] = player.model_index
    return 'successful'


def load_map(name):
    if name in os.listdir('.'):
        with open(name, 'r') as map_file:
            map_file = map_file.readlines()
            area_info = map_file[0].strip('\n').split('.')
            area_content = map_file[1:]

        index = 1
        for element in area_content:
            current_line = [index]
            for each in list(element.strip('\n')):
                current_line.append(txt.reversed_symbols_table[each])
            area.content.append(current_line)
            index += 1
    else:
        return 'map-not-found'


def get_maps():
    maps = []
    valid_maps = []
    for file in os.listdir('.'):
        if file.endswith('.map'):
            maps.append(file)

    for element in maps:
        with open(element, 'r') as map_file:
            valid = True
            for data in map_file.readlines()[0].split('.'):
                for each in ['name', 'description', 'date_created', 'size']:
                    if data.split('=')[0] != each:
                        valid = False
            if valid:
                valid_maps.append(element)

    return valid_maps

