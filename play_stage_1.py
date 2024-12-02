from pico2d import *

import game_framework
import game_world
from flying_object import Flying_object
from knight import Knight
from stage2 import Stage2
from walk_object import Walk_object
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
    server.stage = Stage2()
    game_world.add_object(server.stage, 0)


    server.knight = Knight()
    game_world.add_object(server.knight, 1)
    game_world.add_collision_pair('knight:tile', server.knight, None)
    game_world.add_collision_pair('knight:fly', server.knight, None)
    game_world.add_collision_pair('knight:walk', server.knight, None)

    server.flies.append(Flying_object())
    server.flies.append(Flying_object(300, 150))
    game_world.add_objects(server.flies, 1)
    for fly in server.flies:
        game_world.add_collision_pair('slash:fly', None, fly)
        game_world.add_collision_pair('knight:fly', None, fly)

    server.walks.append(Walk_object(1000))
    game_world.add_objects(server.walks, 1)

    for walk in server.walks:
        game_world.add_collision_pair('slash:walk', None, walk)
        game_world.add_collision_pair('knight:walk', None, walk)
        game_world.add_collision_pair('walk:tile', walk, None)



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