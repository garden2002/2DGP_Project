from pico2d import *

import game_framework
import game_world
from flying_object import Flying_object
from grass import Grass
from knight import Knight


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            knight.handle_event(event)


def init():
    global knight

    grass = Grass()
    game_world.add_object(grass, 0)

    knight = Knight()
    game_world.add_object(knight, 1)

    fly = Flying_object()
    game_world.add_object(fly, 1)

    game_world.add_collision_pair('knight:fly', knight, fly)
    game_world.add_collision_pair('slash:fly', None, fly)

    fly = Flying_object(700, 150)
    game_world.add_object(fly, 1)

    game_world.add_collision_pair('knight:fly', knight, fly)
    game_world.add_collision_pair('slash:fly', None, fly)
    game_world.add_collision_pair('knight:grass', knight, grass)


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