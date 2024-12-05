from pico2d import *

import game_framework

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

class Hp1:
    image = None

    def __init__(self, x = 0):
        if Hp1.image is None:
            Hp1.image = load_image('./resource/Hp1.png')
        self.x = x
        self.y = 620
        self.frame = 0

    def draw(self):
        if self.frame > 0:
            self.image.clip_draw(int(self.frame) * 72, 0, 72, 72, self.x, self.y)
        else:
            self.image.clip_draw(0, 0, 72, 72, self.x, self.y)

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        if self.frame > 5:
            self.frame = - 12


    def get_bb(self):
        pass

    def handle_collision(self, group, other):
        pass