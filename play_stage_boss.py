from pico2d import *

import game_framework
import game_world
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
    server.map = None
    before_state = server.knight.state_machine.cur_state
    server.knight = None
    server.knight = Knight(2,True , before_state)
    game_world.add_object(server.knight, 1)
    game_world.add_collision_pair('knight:tile', server.knight, None)


    server.stage = StageBoss()
    game_world.add_object(server.stage, 0)
    stage_column = StageBossColumn()
    game_world.add_object(stage_column, 2)

def update():
    game_world.update()
    game_world.handle_collisions()
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