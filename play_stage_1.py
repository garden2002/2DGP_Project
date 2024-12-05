from pico2d import *

import game_framework
import game_world
import play_stage_2
from fly import Flying_object
from hp1 import Hp1
from hp2 import Hp2

from knight import Knight
from overload import Overload
from stage1 import Stage1
import server


loc_fly = [(1440 , 2160 -1640) ,(1900 , 2160 -1000) ,(2440 , 2160 -400)]
loc_overload = [(350 , 2160 -1800 , 0) , (3030 , 2160 - 1470 , 1) ,(1280, 2160 - 970 , 1)]

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            server.knight.handle_event(event)


def init():
    server.stage = None
    server.flies = []
    server.walks = []
    server.overloads = []
    server.rolls = []
    server.map = None
    server.hp1 = []
    server.hp2 = None
    if not server.knight is None:
        before_state = server.knight.state_machine.cur_state
        server.knight = None
        server.knight = Knight(1, False, before_state)
    else:
        server.knight = None
        server.knight = Knight()
    game_world.add_object(server.knight, 2)
    game_world.add_collision_pair('knight:tile', server.knight, None)
    game_world.add_collision_pair('knight:fly', server.knight, None)
    game_world.add_collision_pair('knight:overload', server.knight, None)
    game_world.add_collision_pair('knight:goal', server.knight,None)

    for loc in loc_fly:
        server.flies.append(Flying_object(loc[0],loc[1]))
    game_world.add_objects(server.flies, 1)
    for fly in server.flies:
        game_world.add_collision_pair('slash:fly', None, fly)
        game_world.add_collision_pair('knight:fly', None, fly)

    for loc in loc_overload:
        server.overloads.append(Overload(loc[0],loc[1],loc[2]))
    game_world.add_objects(server.overloads, 1)
    for overload in server.overloads:
        game_world.add_collision_pair('slash:overload', None, overload)
        game_world.add_collision_pair('knight:overload', None, overload)

    server.stage = Stage1()
    game_world.add_object(server.stage, 0)

    server.hp2 = Hp2()
    game_world.add_object(server.hp2, 3)

    for hp in range(server.knight.hp):
        server.hp1.append(Hp1(130 + 100 * (hp + 1)))
    game_world.add_objects(server.hp1, 3)


def update():
    game_world.update()
    game_world.handle_collisions()
    if server.knight.stage == 2:
        game_framework.change_mode(play_stage_2)
    if server.knight.die:
        finish()
        init()
    pass


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass

def finish():
    game_world.clear()
    pass