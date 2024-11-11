from pico2d import *

import game_world
import knight
from knight import Knight


def handle_events():
    global play

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            play = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            play = False
        else:
            knight.handle_event(event)


def reset_world():
    global play
    global knight

    play = True
    knight = Knight()
    game_world.add_object(knight, 1)


def update_world():
    game_world.update()
    pass


def render_world():
    clear_canvas()
    game_world.render()
    update_canvas()

open_canvas()
reset_world()
# game loop
while play:
    handle_events()
    update_world()
    render_world()
    delay(0.05)
# finalization code
close_canvas()