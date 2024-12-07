import game_framework
from pico2d import load_image, get_time, clear_canvas, update_canvas, get_events

import platStageStart


def init():
    global image
    global logo_start_time

    image =load_image('./resource/loading.png')
    logo_start_time = get_time()

def finish():
    global image
    del image

def update():
    global logo_start_time
    if get_time() - logo_start_time >= 2.0:
        logo_start_time =get_time()
        game_framework.change_mode(platStageStart)


def draw():
    clear_canvas()
    image.draw(640 , 360)
    update_canvas()


def handle_events():
    pass

def pause():
    pass

def resume():
    pass
