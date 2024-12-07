from pico2d import *

import game_framework

import playStageLoading as startMode

open_canvas(1280, 720)
game_framework.run(startMode)
close_canvas()