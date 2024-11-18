import game_framework
import game_world

from pico2d import *

from state_machine import StateMachine, die

PIXEL_PER_METER = (10.0 / 0.2)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 5

class Idle:
    @staticmethod
    def enter(walk , e):
        walk.action = 0
        walk.frame = 0
    @staticmethod
    def exit(walk , e):
        pass
    @staticmethod
    def do(walk):
        walk.frame = (walk.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 7
        walk.x += walk.dir * RUN_SPEED_PPS * game_framework.frame_time
        if walk.x > 1200:
            walk.dir = -1
        elif walk.x < 800:
            walk.dir = 1
    @staticmethod
    def draw(walk):
        if walk.dir == 1:
            walk.image.clip_composite_draw(
                int(walk.frame) * 140, walk.action * 140, 140, 140,
                0,'h',
                walk.x, walk.y, 140,140
            )
        else:
            walk.image.clip_draw(int(walk.frame) * 140, walk.action * 140, 140, 140, walk.x, walk.y)

class Fly_Death:
    @staticmethod
    def enter(walk , e):
        walk.action = 1
        walk.frame = 0
    @staticmethod
    def exit(walk , e):
        pass
    @staticmethod
    def do(walk):
        walk.frame = (walk.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 1

    @staticmethod
    def draw(walk):
        if walk.dir == 1:
            walk.image.clip_composite_draw(
                int(walk.frame) * 140, walk.action * 140, 140, 140,
                0,'h',
                walk.x, walk.y, 140,140
            )
        else:
            walk.image.clip_draw(int(walk.frame) * 140, walk.action * 140, 140, 140, walk.x, walk.y)


class Death:
    @staticmethod
    def enter(walk , e):
        walk.action = 2
        walk.frame = 0
    @staticmethod
    def exit(walk , e):
        pass
    @staticmethod
    def do(walk):
        walk.frame = (walk.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        if walk.frame > 8:
            game_world.remove_object(walk)
            pass
    @staticmethod
    def draw(walk):
        if walk.dir == 1:
            walk.image.clip_composite_draw(
                int(walk.frame) * 140, walk.action * 140, 140, 140,
                0,'h',
                walk.x, walk.y, 140,140
            )
        else:
            walk.image.clip_draw(int(walk.frame) * 140, walk.action * 140, 140, 140, walk.x, walk.y)


class Walk_object:
    image = None

    def __init__(self, x = 700, y= 400 ):
        self.x, self.y = x, y
        self.action = 0
        self.frame = 0
        self.dir = -1
        self.hp = 4
        self.invincibility_time = 0
        self.font = load_font('ENCR10B.TTF', 16)
        self.state_machine = StateMachine(self)  # 소년 객체를 위한 상태 머신인지 알려줄 필요
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {die:Death},
                Fly_Death:{},
                Death:{}
            }
        )
        if Walk_object.image == None:
            Walk_object.image = load_image('walk_object.png')

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        pass

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())
        self.font.draw(self.x - 10, self.y + 50, f'{self.hp:02d}', (255, 255, 0))

    def get_bb(self):
        if self.dir == 1:
            return self.x - 40, self.y - 70, self.x + 70, self.y + 70
        else:
            return self.x - 70, self.y - 70, self.x + 40, self.y + 70

    def handle_collision(self, group, other):
        if group == 'slash:walk':
            if get_time() - self.invincibility_time > 0.6:
                self.invincibility_time = get_time()
                self.hp -= 1
                if self.hp < 1:
                    self.state_machine.add_event(('Die', 0))
        pass


