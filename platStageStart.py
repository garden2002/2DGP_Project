from pico2d import load_image, get_events, clear_canvas, update_canvas, load_music
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE

import game_framework
import playStage1


def init():
    global image
    global bgm
    image = load_image('./resource/start.png')
    bgm = load_music('./resource/start.mp3')
    bgm.set_volume(32)
    bgm.repeat_play()


def finish():
    global image
    global bgm
    del image
    del bgm

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.change_mode(playStage1)


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