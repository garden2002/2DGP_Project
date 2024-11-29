from pico2d import *

import game_framework
import game_world
from Map import TileMap
from flying_object import Flying_object
from knight import Knight
from walk_object import Walk_object

map_data = [
    [1,1,1,1,1,1,1,1,1,1],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [1,1,1,0,0,0,0,0,0,0],
    [1,1,1,1,1,1,1,1,1,1],
]



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

    map = TileMap(map_data)
    game_world.add_object(map, 0)

    knight = Knight()
    game_world.add_object(knight, 1)

    game_world.add_collision_pair('knight:map', knight, None)

    fly = Flying_object()
    game_world.add_object(fly, 1)

    game_world.add_collision_pair('knight:fly', knight, fly)
    game_world.add_collision_pair('slash:fly', None, fly)

    fly = Flying_object(300, 150)
    game_world.add_object(fly, 1)
    game_world.add_collision_pair('knight:fly', knight, fly)
    game_world.add_collision_pair('slash:fly', None, fly)

    walk = Walk_object(1000 , 130)
    game_world.add_object(walk, 1)
    game_world.add_collision_pair('slash:walk', None, walk)
    game_world.add_collision_pair('knight:walk', knight, walk)





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