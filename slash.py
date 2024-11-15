from pico2d import *
import game_world
import game_framework


TIME_PER_ACTION = 0.4
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 3



class Slash:
    image = None

    def __init__(self, x = 0, y = 0, action = 0):
        if Slash.image == None:
            Slash.image = load_image('slash.png')
        self.x, self.y = x, y
        self.frame = 0
        self.action = action

    def draw(self):
        self.image.clip_draw(int(self.frame) * 256, self.action * 128, 256, 128, self.x, self.y)

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        if self.frame > 3:
            game_world.remove_object(self)
