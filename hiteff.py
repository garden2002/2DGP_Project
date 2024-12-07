from pico2d import *
import game_world
import game_framework
import server

TIME_PER_ACTION = 0.3
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 7


class HitEff:
    image = None

    def __init__(self, x = 100, y = 200, face_dir = 1):
        if HitEff.image == None:
            HitEff.image = load_image('./resource/hit_eff.png')
        self.x, self.y ,self.face_dir = x , y ,face_dir
        self.frame = 0

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        if self.frame > 9:
            game_world.remove_object(self)

    def draw(self):
        sx = self.x - server.stage.window_left
        sy = self.y - server.stage.window_bottom
        if math.cos(self.face_dir) > 0:
            self.image.clip_composite_draw(
                int(self.frame) * 128, 0, 128, 128,
                0, ' ',
                sx, sy, 256, 256
            )
        else:
            self.image.clip_composite_draw(
                int(self.frame) * 128, 0, 128, 128,
                0, 'h',
                sx, sy, 256, 256
            )

