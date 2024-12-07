from pico2d import load_image, get_events, clear_canvas, update_canvas, load_music
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE

import game_framework


def init():
    global image
    image = load_image('./resource/end.png')
    global bgm
    bgm = load_music('./resource/end.mp3')
    bgm.set_volume(32)
    bgm.repeat_play()


def finish():
    global image
    del image
    global bgm
    del bgm

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()


def draw():
    clear_canvas()
    image.draw(640 , 360)
    update_canvas()

def update():
    pass

def pause():
    pass

def resume():
    pass