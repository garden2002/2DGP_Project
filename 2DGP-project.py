from pico2d import *

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
    global world
    global knight

    play = True
    knight = Knight()
    world = []
    world.append(knight)


def update_world():
    for o in world:
        o.update()
    pass


def render_world():
    clear_canvas()
    for o in world:
        o.draw()
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