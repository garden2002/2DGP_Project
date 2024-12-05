from pico2d import *

import game_framework
import game_world
import play_stage_boss
from hp1 import Hp1
from hp2 import Hp2

from knight import Knight
from roll import Roll
from stage2 import Stage2
from walk import Walk_object
import server
import math

loc_walk = [(1400 , 2160 -1860) ,(1440 , 2160 -1190) ,(2170 , 2160 -480)]
loc_roll = [(1980 , 2160 -1860 , math.atan2(0 , -1)) , (500 , 2160 - 1040 ,  math.atan2(0, 1)) ,(1570, 2160 - 1180 , math.atan2(0, 1))]

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
    server.hp1 = []
    server.hp2 = None
    server.map = None
    if not server.knight is None:
        before_state = server.knight.state_machine.cur_state
        server.knight = None
        server.knight = Knight(2,True ,before_state)
    else:
        server.knight = None
        server.knight = Knight(2,True)
    game_world.add_object(server.knight, 2)
    game_world.add_collision_pair('knight:tile', server.knight, None)
    game_world.add_collision_pair('knight:walk', server.knight, None)
    game_world.add_collision_pair('knight:roll', server.knight, None)
    game_world.add_collision_pair('knight:goal', server.knight, None)

    for loc in loc_walk:
        server.walks.append(Walk_object(loc[0],loc[1]))
    game_world.add_objects(server.walks, 1)
    for walk in server.walks:
        game_world.add_collision_pair('slash:walk', None, walk)
        game_world.add_collision_pair('knight:walk', None, walk)
        game_world.add_collision_pair('walk:tile', walk, None)

    for loc in loc_roll:
        server.rolls.append(Roll(loc[0],loc[1],loc[2]))
    game_world.add_objects(server.rolls, 1)
    for roll in server.rolls:
        game_world.add_collision_pair('slash:roll', None, roll)
        game_world.add_collision_pair('knight:roll', None, roll)
        game_world.add_collision_pair('roll:tile', roll, None)

    server.stage = Stage2()
    game_world.add_object(server.stage, 0)

    server.hp2 = Hp2()
    game_world.add_object(server.hp2, 3)

    for hp in range(server.knight.hp):
        server.hp1.append(Hp1(130 + 100 * (hp + 1)))
    game_world.add_objects(server.hp1, 3)

def update():
    game_world.update()
    game_world.handle_collisions()
    if server.knight.stage == 3:
        game_framework.change_mode(play_stage_boss)
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