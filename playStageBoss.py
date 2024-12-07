from pico2d import *

import game_framework
import game_world
import platStageEnd
from boss import Boss
from hp1 import Hp1
from hp2 import Hp2

from knight import Knight
from stageboss import StageBoss
from stagebossColumn import StageBossColumn
import server

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
    server.boss = None

    if not server.knight is None:
        before_state = server.knight.state_machine.cur_state
        server.knight = None
        server.knight = Knight(3,True , before_state)
    else:
        server.knight = None
        server.knight = Knight()
    game_world.add_object(server.knight, 1)
    game_world.add_collision_pair('knight:tile', server.knight, None)
    game_world.add_collision_pair('knight:boss', server.knight, None)
    game_world.add_collision_pair('knight:attack', server.knight, None)

    server.boss = Boss()
    game_world.add_object(server.boss, 1)
    game_world.add_collision_pair('boss:tile', server.boss, None)
    game_world.add_collision_pair('knight:boss', None, server.boss)
    game_world.add_collision_pair('slash:boss', None,  server.boss)

    server.stage = StageBoss()
    game_world.add_object(server.stage, 0)
    stage_column = StageBossColumn()
    game_world.add_object(stage_column, 3)

    server.hp2 = Hp2()
    game_world.add_object(server.hp2, 3)

    for hp in range(server.knight.hp):
        server.hp1.append(Hp1(130 + 100 * (hp + 1)))
    game_world.add_objects(server.hp1, 3)

def update():
    game_world.update()
    game_world.handle_collisions()
    if server.knight.die:
        finish()
        init()
    if server.boss.die:
        game_framework.change_mode(platStageEnd)
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