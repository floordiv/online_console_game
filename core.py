import os


cls = 'clear'


class area:
    # def __setattr__(self, key, value):
    #     # var.last_player_move = []
    #     pass

    height = 17
    width = 33
    content = []
    collision_objects = [1, 2, 3, 4]


class player:
    def edit_x_pos(self, x):
        if area.content[player.__current_y][player.__current_x + x] != 0:
            return 'collision'
        if x in [1, -1]:
            var.last_player_actions['x'] = player.__current_x
            area.content[player.__current_y][player.__current_x] = 0
            player.__current_x += x
            return True
        return False

    def edit_y_pos(self, y):
        if area.content[player.__current_y + y][player.__current_x] != 0:
            return 'collision'
        if y in [1, -1]:
            var.last_player_actions['y'] = player.__current_y
            area.content[player.__current_y][player.__current_x] = 0
            player.__current_y += y
            return True
        return False

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
    last_player_actions = {'y': 0, 'x': 0}


symbols_table = {
    0: ' ',     # empty field
    1: '|',     # vertical wall
    2: '—',     # horizontal wall
    3: '#',     # water
    4: '@',     # tree
    5: '>',     # higher place
    6: '<',     # lower place
    7: '☉'      # player
}
reversed_symbols_table = dict(zip(symbols_table.values(), symbols_table.keys()))

area_height = 17
area_weight = 33
area_data = []


def clear_area():
    os.system(cls)


def return_player_to_last_coord():
    player.edit_y_pos(0, var.last_player_actions['y'])
    player.edit_x_pos(0, var.last_player_actions['x'])
    area.content[var.last_player_actions['y']][var.last_player_actions['x']] = 0


def load_map(name):
    with open(name, 'r') as map_file:
        map_file = map_file.readlines()
        area_info = map_file[0].strip('\n').split('.')
        # area_info = area_file[0].split('.')
        area_content = map_file[1:]

    index = 1
    for element in area_content:
        current_line = [index]
        for each in list(element.strip('\n')):
            current_line.append(reversed_symbols_table[each])
        area.content.append(current_line)
        index += 1


def update_player():
    if area.content[player.get_y(0)][player.get_x(0)] in area.collision_objects:
        return_player_to_last_coord()
        return 'collision-object'

    area.content[player.get_y(0)][player.get_x(0)] = player.model_index
    return 'successful'


def draw_table():
    for element in area.content:
        element = element[1:]
        current_line = ''
        for each in element:
            try:
                current_line += symbols_table[each]
            except KeyError:
                pass
        print(current_line)

# collision
