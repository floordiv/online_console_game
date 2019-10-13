import core


version = '0.0.1'


class area:
    collision_objects = [1, 2, 3, 4]
    triggers = [8, 9, 10]  # text output, text input and teleport
    triggers_collision = True


def player_abspos(player_moves):
    return [core.player.get_y(0) + player_moves[0], core.player.get_x(0) + player_moves[1]]


def iscollision(player_moves):     # list
    next_abs_player_pos = player_abspos(player_moves)   # y, x
    next_object = core.area.content[next_abs_player_pos[0]][next_abs_player_pos[1]]
    if next_object in area.collision_objects:
        return 'collision'
    elif next_object in area.triggers:
        return 'trigger'
    else:
        return 'false'


def istrigger(pos):  # list
    if core.area.content[pos[0]][pos[1]] in area.triggers:
        return True
    return False


def trigger_handler(trigger):
    player_pos = [core.player.get_y(0), core.player.get_x(0)]
    trigger_type = trigger.split('::')[1].split('|')[0]
    trigger_name = trigger.split('::')[1].split('|')[1]
    trigger_action = trigger.split('::')[1].split('|')[2]
    core.trigger.actions[trigger_name] = core.trigger.keys[trigger_type](trigger_action)

