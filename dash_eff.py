from pico2d import *
import game_world
import game_framework
import server

TIME_PER_ACTION = 0.3
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 7


class Dash_eff:
    image = None

    def __init__(self, x = 100, y = 200, action = 0 , face_dir = 1):
        if Dash_eff.image == None:
            Dash_eff.image = load_image('dash_eff.png')
        self.x, self.y ,self.face_dir = x , y ,face_dir
        self.frame = 0

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        if self.frame > 7:
            game_world.remove_object(self)

    def draw(self):
        sx = self.x - server.stage.window_left
        sy = self.y - server.stage.window_bottom
        if self.face_dir == 1:
            self.image.clip_draw(int(self.frame) * 402, 0, 402, 188, sx,
                                 sy)
        else:
            self.image.clip_composite_draw(
                int(self.frame) * 402, 0, 402, 188,
                0, 'h',
                sx, sy, 402, 188
            )

