from pico2d import *
import game_framework
import server

PIXEL_PER_METER = (10.0 / 0.2)  # 10 pixel 30 cm

TIME_PER_ACTION = 0.4
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 6

RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

class BossAttackEffBack:
    image = None
    def __init__(self, x = 100, y = 200, dir = 1):
        self.x, self.y ,self.dir = x , y, dir
        self.frame = 0
        self.speed = 1

    def update(self):
        self.x += self.speed * RUN_SPEED_PPS * game_framework.frame_time * math.cos(self.dir)
        if self.speed < 4:
            self.speed += 0.05

    def draw(self):
        sx = self.x - server.stage.window_left
        sy = self.y - server.stage.window_bottom

    def get_bb(self):
        if math.cos(self.dir) < 0:
            return self.x + 20, self.y - 190, self.x + 120, self.y- 140
        else:
            return self.x- 120, self.y - 190, self.x - 20, self.y - 140

    def handle_collision(self, group, other):
        pass


