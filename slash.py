from pico2d import *
import game_world
import game_framework
import server

TIME_PER_ACTION = 0.4
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 3


class Slash_eff:
    image = None

    def __init__(self, x = 100, y = 200, action = 0 , face_dir = 1):
        if Slash_eff.image == None:
            Slash_eff.image = load_image('slash.png')
        self.x, self.y , self.action , self.face_dir = x , y , action , face_dir
        self.frame = 0

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        if self.frame > 4:
            game_world.remove_object(self)

    def draw(self):
        sx = self.x - server.stage.window_left
        sy = self.y - server.stage.window_bottom
        if self.face_dir == 1:
            if self.action == 0:
                self.image.clip_composite_draw(
                    int(self.frame) * 256, self.action * 128, 256, 128,
                    3.141592 / 2, 'h',
                    sx, sy, 256, 128
                )
            else:
                self.image.clip_composite_draw(
                    int(self.frame) * 256, self.action * 128, 256, 128,
                    0, 'h',
                    sx, sy, 256, 128
                )
        else:
            if self.action == 0:
                self.image.clip_composite_draw(
                    int(self.frame) * 256, self.action * 128, 256, 128,
                    -3.141592 / 2, ' ',
                    sx, sy, 256, 128
                )
            else:
                self.image.clip_draw(int(self.frame) * 256, self.action * 128, 256, 128, sx,
                                     sy)
        if self.face_dir == 1:
            if self.action == 0:
                draw_rectangle(sx - 40, sy, sx + 40, sy + 110)
            else:
                draw_rectangle(sx - 30, sy - 65, sx + 110, sy + 65)
        else:
            if self.action == 0:
                draw_rectangle(sx - 40, sy, sx + 40, sy + 110)
            else:
                draw_rectangle(sx - 110, sy - 65, sx + 30, sy + 65)

    def get_bb(self):
        if self.face_dir == 1:
            if self.action == 0:
                return self.x - 40, self.y, self.x + 40, self.y + 110
            else:
                return self.x - 30, self.y - 65, self.x + 110, self.y + 65
        else:
            if self.action == 0:
                return self.x - 40, self.y, self.x + 40, self.y + 110
            else:
                return self.x - 110, self.y - 65, self.x + 30, self.y + 65

    def handle_collision(self, group, other):
        pass


