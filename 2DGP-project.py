from pico2d import *

import game_framework

import loading_mode as start_mode


open_canvas(1280, 720)
game_framework.run(start_mode)
close_canvas()