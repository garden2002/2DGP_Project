import random

import game_world
import slash
from pico2d import get_time, load_image
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE

import game_framework
from state_machine import right_down, left_up, left_down, right_up, start_event, StateMachine, z_down, x_down, \
    end_motion

PIXEL_PER_METER = (10.0 / 0.2)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


TIME_PER_ACTION = 0.4
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION_IDLE = 9
FRAMES_PER_ACTION_RUN = 8
FRAMES_PER_ACTION_SLASH = 5



class Idle:
    @staticmethod
    def enter(knight , e):
        if right_down(e) or left_up(e):
            knight.face_dir = -1
            pass
        elif left_down(e) or right_up(e) or start_event(e):
            knight.face_dir = 1
            pass
        knight.action = 3
        knight.frame = 0
        knight.dir = 0
        #시작 시간을 기록
        knight.start_time = get_time()
        pass
    @staticmethod
    def exit(knight , e):
        pass
    @staticmethod
    def do(knight):
        knight.frame = (knight.frame + FRAMES_PER_ACTION_IDLE * ACTION_PER_TIME * game_framework.frame_time) % 9
        pass
    @staticmethod
    def draw(knight):
        if knight.face_dir == 1:
            knight.image.clip_composite_draw(
                int(knight.frame) * 128, knight.action * 128, 128, 128,
                0,'h',
                knight.x, knight.y,128,128
            )
        else:
            knight.image.clip_draw(int(knight.frame) * 128, knight.action * 128, 128, 128, knight.x, knight.y)
        pass


class Run:
    @staticmethod
    def enter(knight , e):
        if right_down(e) or left_up(e):
            knight.face_dir = 1
            knight.dir = 1
            pass
        elif left_down(e) or right_up(e):
            knight.face_dir = -1
            knight.dir = -1
            pass
        knight.action = 2
        knight.frame = 0
        #시작 시간을 기록
        knight.start_time = get_time()
        pass
    @staticmethod
    def exit(knight , e):
        pass
    @staticmethod
    def do(knight):
        knight.frame = (knight.frame + FRAMES_PER_ACTION_RUN * ACTION_PER_TIME * game_framework.frame_time)
        if knight.frame > 9:
            knight.frame = 5
        knight.x += knight.dir * RUN_SPEED_PPS * game_framework.frame_time
        pass
    @staticmethod
    def draw(knight):
        if knight.face_dir == 1:
            knight.image.clip_composite_draw(
                int(knight.frame) * 128, knight.action * 128, 128, 128,
                0, 'h',
                knight.x, knight.y, 128, 128
            )
        else:
            knight.image.clip_draw(int(knight.frame) * 128, knight.action * 128, 128, 128, knight.x, knight.y)
        pass

class Slash:
    @staticmethod
    def enter(knight , e):
        knight.action = random.randint(0, 1)
        knight.frame = 0
        knight.knight_slash()
        #시작 시간을 기록
        pass
    @staticmethod
    def exit(knight , e):
        pass
    @staticmethod
    def do(knight):
        knight.frame = (knight.frame + FRAMES_PER_ACTION_SLASH * ACTION_PER_TIME * game_framework.frame_time)
        if knight.frame > 5:
            knight.state_machine.add_event(('ENT_MOTION', 0))
        pass
    @staticmethod
    def draw(knight):
        if knight.face_dir == 1:
            knight.image.clip_composite_draw(
                int(knight.frame) * 128, knight.action * 128, 128, 128,
                0, 'h',
                knight.x, knight.y, 128, 128
            )
        else:
            knight.image.clip_draw(int(knight.frame) * 128, knight.action * 128, 128, 128, knight.x, knight.y)
        pass

class Move_Slash:
    @staticmethod
    def enter(knight , e):
        knight.action = random.randint(0, 1)
        knight.frame = 0
        knight.knight_slash()
        #시작 시간을 기록
        pass
    @staticmethod
    def exit(knight , e):
        pass
    @staticmethod
    def do(knight):
        knight.frame = (knight.frame + FRAMES_PER_ACTION_SLASH * ACTION_PER_TIME * game_framework.frame_time)
        if knight.frame > 5:
            knight.state_machine.add_event(('ENT_MOTION', 0))
        knight.x += knight.dir * RUN_SPEED_PPS * game_framework.frame_time
        pass
    @staticmethod
    def draw(knight):
        if knight.face_dir == 1:
            knight.image.clip_composite_draw(
                int(knight.frame) * 128, knight.action * 128, 128, 128,
                0, 'h',
                knight.x, knight.y, 128, 128
            )
        else:
            knight.image.clip_draw(int(knight.frame) * 128, knight.action * 128, 128, 128, knight.x, knight.y)
        pass


class Knight:
    image = None
    def __init__(self):
        self.x, self.y = 100 , 300
        self.frame = 0
        self.dir = 0
        self.action = 0
        self.state_machine = StateMachine(self)  # 소년 객체를 위한 상태 머신인지 알려줄 필요
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle:{right_down: Run, left_down: Run, left_up: Run, right_up: Run, x_down: Slash},
                Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, x_down: Move_Slash},
                Slash:{end_motion: Idle , right_down: Run, left_down: Run, right_up: Run, left_up: Run},
                Move_Slash:{end_motion: Run,right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle}
            }
        )
        if Knight.image == None:
            Knight.image = load_image('knight.png')

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.add_event(
            ('INPUT', event)
        )
    def draw(self):
        self.state_machine.draw()

    def knight_slash(self):
        slash = Slash(self.x , self.y , self.action)
        game_world.add_object(slash, 2)

