import random

import game_world
from pico2d import get_time, load_image
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE

import game_framework
from dash_eff import Dash_eff
from slash import Slash_eff
from state_machine import right_down, left_up, left_down, right_up, start_event, StateMachine, z_down, x_down, \
    end_motion, up_down, up_up, s_down

PIXEL_PER_METER = (10.0 / 0.2)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

RUN_DASH_SPEED_KMPH = 80.0
RUN_DASH_SPEED_MPM = (RUN_DASH_SPEED_KMPH * 1000.0 / 60.0)
RUN_DASH_SPEED_MPS = (RUN_DASH_SPEED_MPM / 60.0)
RUN_DASH_SPEED_PPS = (RUN_DASH_SPEED_MPS * PIXEL_PER_METER)


TIME_PER_ACTION = 0.5
TIME_PER_DASH_ACTION = 0.3
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
DASH_ACTION_PER_TIME = 1.0 / TIME_PER_DASH_ACTION
FRAMES_PER_ACTION_IDLE = 9
FRAMES_PER_ACTION_RUN = 8
FRAMES_PER_ACTION_SLASH = 5
FRAMES_PER_ACTION_DASH = 7



class Idle:
    @staticmethod
    def enter(knight , e):
        if right_down(e) or left_up(e):
            knight.face_dir = -1
            pass
        elif left_down(e) or right_up(e) or start_event(e):
            knight.face_dir = 1
            pass
        if not up_up(e):
            knight.action = 4
            knight.frame = 0
            knight.dir = 0
    @staticmethod
    def exit(knight , e):
        pass
    @staticmethod
    def do(knight):
        knight.frame = (knight.frame + FRAMES_PER_ACTION_IDLE * ACTION_PER_TIME * game_framework.frame_time) % 9
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

class Up_Idle:
    @staticmethod
    def enter(knight , e):
        if right_down(e) or left_up(e):
            knight.face_dir = -1
            pass
        elif left_down(e) or right_up(e) or start_event(e):
            knight.face_dir = 1
            pass

        if not up_down(e):
            knight.action = 4
            knight.frame = 0
            knight.dir = 0
        pass
    @staticmethod
    def exit(knight , e):
        pass
    @staticmethod
    def do(knight):
        knight.frame = (knight.frame + FRAMES_PER_ACTION_IDLE * ACTION_PER_TIME * game_framework.frame_time) % 9
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

        if not up_up(e):
            knight.action = 3
            knight.frame = 0
    @staticmethod
    def exit(knight , e):
        pass
    @staticmethod
    def do(knight):
        knight.frame = (knight.frame + FRAMES_PER_ACTION_RUN * ACTION_PER_TIME * game_framework.frame_time)
        if knight.frame > 9:
            knight.frame = 5
        knight.x += knight.dir * RUN_SPEED_PPS * game_framework.frame_time
        knight.slash_eff.x += knight.dir * RUN_SPEED_PPS * game_framework.frame_time
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

class Up_Run:
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

        if not up_down(e):
            knight.action = 3
            knight.frame = 0
    @staticmethod
    def exit(knight , e):
        pass
    @staticmethod
    def do(knight):
        knight.frame = (knight.frame + FRAMES_PER_ACTION_RUN * ACTION_PER_TIME * game_framework.frame_time)
        if knight.frame > 9:
            knight.frame = 5
        knight.x += knight.dir * RUN_SPEED_PPS * game_framework.frame_time
        knight.slash_eff.x += knight.dir * RUN_SPEED_PPS * game_framework.frame_time
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

class Slash:
    @staticmethod
    def enter(knight , e):
        if x_down(e):
            knight.action = random.randint(1, 2)
            knight.knight_slash()
    @staticmethod
    def exit(knight , e):
        pass
    @staticmethod
    def do(knight):
        knight.slash_frame = (knight.slash_frame + FRAMES_PER_ACTION_SLASH * ACTION_PER_TIME * game_framework.frame_time)
        if knight.slash_frame > 4:
            knight.slash_frame = 0
            knight.state_machine.add_event(('ENT_MOTION', 0))
    @staticmethod
    def draw(knight):
        if knight.face_dir == 1:
            if knight.action == 0:
                knight.image.clip_composite_draw(
                    int(knight.slash_frame) * 128, knight.action * 128, 128, 128,
                    0, 'h',
                    knight.x - 16, knight.y, 128, 128
                )
            else:
                knight.image.clip_composite_draw(
                    int(knight.slash_frame) * 128, knight.action * 128, 128, 128,
                    0, 'h',
                    knight.x, knight.y, 128, 128
                )
        else:
            if knight.action == 0:
                knight.image.clip_draw(int(knight.slash_frame) * 128, knight.action * 128, 128, 128, knight.x + 16,
                                       knight.y)
            else:
                knight.image.clip_draw(int(knight.slash_frame) * 128, knight.action * 128, 128, 128, knight.x, knight.y)

class Up_Slash:
    @staticmethod
    def enter(knight , e):
        if x_down(e):
            knight.action = 0
            knight.knight_slash()
    @staticmethod
    def exit(knight , e):
        pass
    @staticmethod
    def do(knight):
        knight.slash_frame = (knight.slash_frame + FRAMES_PER_ACTION_SLASH * ACTION_PER_TIME * game_framework.frame_time)
        if knight.slash_frame > 4:
            knight.slash_frame = 0
            knight.state_machine.add_event(('ENT_MOTION', 0))
    @staticmethod
    def draw(knight):
        if knight.face_dir == 1:
            if knight.action == 0:
                knight.image.clip_composite_draw(
                    int(knight.slash_frame) * 128, knight.action * 128, 128, 128,
                    0, 'h',
                    knight.x - 16, knight.y, 128, 128
                )
            else:
                knight.image.clip_composite_draw(
                    int(knight.slash_frame) * 128, knight.action * 128, 128, 128,
                    0, 'h',
                    knight.x, knight.y, 128, 128
                )
        else:
            if knight.action == 0:
                knight.image.clip_draw(int(knight.slash_frame) * 128, knight.action * 128, 128, 128, knight.x + 16,
                                       knight.y)
            else:
                knight.image.clip_draw(int(knight.slash_frame) * 128, knight.action * 128, 128, 128, knight.x, knight.y)

class Move_Slash:
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
        elif x_down(e):
            knight.action = random.randint(1, 2)
            knight.knight_slash()
    @staticmethod
    def exit(knight , e):
        pass
    @staticmethod
    def do(knight):
        knight.slash_frame = (knight.slash_frame + FRAMES_PER_ACTION_SLASH * ACTION_PER_TIME * game_framework.frame_time)
        if knight.slash_frame > 4:
            knight.slash_frame = 0
            knight.state_machine.add_event(('ENT_MOTION', 0))
        knight.x += knight.dir * RUN_SPEED_PPS * game_framework.frame_time
        knight.slash_eff.x += knight.dir * RUN_SPEED_PPS * game_framework.frame_time
    @staticmethod
    def draw(knight):
        if knight.face_dir == 1:
            if knight.action == 0:
                knight.image.clip_composite_draw(
                    int(knight.slash_frame) * 128, knight.action * 128, 128, 128,
                    0, 'h',
                    knight.x - 16, knight.y, 128, 128
                )
            else:
                knight.image.clip_composite_draw(
                    int(knight.slash_frame) * 128, knight.action * 128, 128, 128,
                    0, 'h',
                    knight.x, knight.y, 128, 128
                )
        else:
            if knight.action == 0:
                knight.image.clip_draw(int(knight.slash_frame) * 128, knight.action * 128, 128, 128, knight.x + 16,
                                       knight.y)
            else:
                knight.image.clip_draw(int(knight.slash_frame) * 128, knight.action * 128, 128, 128, knight.x, knight.y)


class Up_Move_Slash:
    @staticmethod
    def enter(knight , e):
        if right_down(e) or left_up(e):
            knight.face_dir = 1
            knight.dir = 1
        elif left_down(e) or right_up(e):
            knight.face_dir = -1
            knight.dir = -1
        elif x_down(e):
            knight.action = 0
            knight.knight_slash()
    @staticmethod
    def exit(knight , e):
        pass
    @staticmethod
    def do(knight):
        knight.slash_frame = (knight.slash_frame + FRAMES_PER_ACTION_SLASH * ACTION_PER_TIME * game_framework.frame_time)
        if knight.slash_frame > 4:
            knight.slash_frame = 0
            knight.state_machine.add_event(('ENT_MOTION', 0))
        knight.x += knight.dir * RUN_SPEED_PPS * game_framework.frame_time
        knight.slash_eff.x += knight.dir * RUN_SPEED_PPS * game_framework.frame_time
    @staticmethod
    def draw(knight):
        if knight.face_dir == 1:
            if knight.action == 0:
                knight.image.clip_composite_draw(
                    int(knight.slash_frame) * 128, knight.action * 128, 128, 128,
                    0, 'h',
                    knight.x - 16, knight.y, 128, 128
                )
            else:
                knight.image.clip_composite_draw(
                    int(knight.slash_frame) * 128, knight.action * 128, 128, 128,
                    0, 'h',
                    knight.x, knight.y, 128, 128
                )
        else:
            if knight.action == 0:
                knight.image.clip_draw(int(knight.slash_frame) * 128, knight.action * 128, 128, 128, knight.x + 16,
                                       knight.y)
            else:
                knight.image.clip_draw(int(knight.slash_frame) * 128, knight.action * 128, 128, 128, knight.x, knight.y)

class Dash:
    @staticmethod
    def enter(knight , e):
        if s_down(e):
            knight.frame = 0
            knight.action = 5
            knight.knight_dash()
        pass
    @staticmethod
    def exit(knight , e):
        pass
    @staticmethod
    def do(knight):
        knight.frame = (knight.frame + FRAMES_PER_ACTION_DASH * DASH_ACTION_PER_TIME * game_framework.frame_time)
        if knight.frame > 7:
            knight.state_machine.add_event(('ENT_MOTION', 0))
        knight.x += knight.dir * RUN_DASH_SPEED_PPS * game_framework.frame_time
        knight.dash_eff.x += knight.dir * RUN_DASH_SPEED_PPS * game_framework.frame_time
    @staticmethod
    def draw(knight):
        if knight.face_dir == 1:
            knight.image.clip_composite_draw(
                int(knight.frame) * 256, knight.action * 128, 256, 128,
                0, 'h',
                knight.x, knight.y, 256, 128
            )
        else:
            knight.image.clip_draw(int(knight.frame) * 256, knight.action * 128, 256, 128, knight.x, knight.y)


class Up_Dash:
    @staticmethod
    def enter(knight , e):
        if s_down(e):
            knight.frame = 0
            knight.action = 5
            knight.knight_dash()
        pass
    @staticmethod
    def exit(knight , e):
        pass
    @staticmethod
    def do(knight):
        knight.frame = (knight.frame + FRAMES_PER_ACTION_DASH * DASH_ACTION_PER_TIME * game_framework.frame_time)
        if knight.frame > 7:
            knight.state_machine.add_event(('ENT_MOTION', 0))
        knight.x += knight.dir * RUN_DASH_SPEED_PPS * game_framework.frame_time
        knight.dash_eff.x += knight.dir * RUN_DASH_SPEED_PPS * game_framework.frame_time
    @staticmethod
    def draw(knight):
        if knight.face_dir == 1:
            knight.image.clip_composite_draw(
                int(knight.frame) * 256, knight.action * 128, 256, 128,
                0, 'h',
                knight.x, knight.y, 256, 128
            )
        else:
            knight.image.clip_draw(int(knight.frame) * 256, knight.action * 128, 256, 128, knight.x, knight.y)


class Knight:
    image = None
    def __init__(self):
        self.x, self.y = 100 , 300
        self.frame = 0
        self.dir = 0
        self.slash_frame = 0
        self.action = 0
        self.face_dir = 1
        self.slash_eff = Slash_eff()
        self.dash_eff = Dash_eff()
        self.state_machine = StateMachine(self)  # 소년 객체를 위한 상태 머신인지 알려줄 필요
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle:{right_down: Run, left_down: Run, left_up: Run, right_up: Run, x_down: Slash, up_down:Up_Idle},
                Up_Idle: {right_down: Up_Run, left_down: Up_Run, left_up: Up_Run, right_up: Up_Run, x_down: Up_Slash,up_up:Idle},

                Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, x_down: Move_Slash, up_down:Up_Run ,s_down:Dash},
                Up_Run: {right_down: Up_Idle, left_down: Up_Idle, right_up: Up_Idle, left_up: Up_Idle, x_down: Up_Move_Slash,up_up:Run,s_down:Up_Dash},

                Slash:{end_motion: Idle , right_down: Move_Slash, left_down: Move_Slash, right_up: Move_Slash, left_up: Move_Slash ,up_down:Up_Slash },
                Move_Slash:{end_motion: Run, right_down: Slash, left_down: Slash, right_up: Slash, left_up: Slash ,up_down:Up_Move_Slash},
                Up_Slash:{end_motion: Up_Idle , right_down: Up_Move_Slash, left_down: Up_Move_Slash, right_up: Up_Move_Slash, left_up: Up_Move_Slash ,up_up:Slash},
                Up_Move_Slash: {end_motion: Up_Run, right_down: Up_Slash, left_down: Up_Slash,right_up: Up_Slash, left_up: Up_Slash , up_up:Move_Slash},

                Dash:{end_motion: Run ,right_down: Idle, left_down: Idle, left_up: Idle, right_up: Idle,up_down:Up_Dash},
                Up_Dash: {end_motion: Up_Run,right_down: Up_Idle, left_down: Up_Idle, left_up: Up_Idle, right_up: Up_Idle, up_up:Dash },

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
        self.slash_eff = Slash_eff()
        if self.face_dir == -1:
            if self.action == 0:
                self.slash_eff.x, self.slash_eff.y, self.slash_eff.action, self.slash_eff.face_dir = self.x,self.y + 64,self.action,self.face_dir
            else:
                self.slash_eff.x, self.slash_eff.y, self.slash_eff.action, self.slash_eff.face_dir = self.x - 64, self.y, self.action, self.face_dir
        else:
            if self.action == 0:
                self.slash_eff.x, self.slash_eff.y, self.slash_eff.action, self.slash_eff.face_dir = self.x, self.y + 64,self.action,self.face_dir
            else:
                self.slash_eff.x, self.slash_eff.y, self.slash_eff.action, self.slash_eff.face_dir = self.x + 64,self.y,self.action,self.face_dir

        game_world.add_object(self.slash_eff, 2)

    def knight_dash(self):
        self.dash_eff = Dash_eff()
        if self.face_dir == -1:
            self.dash_eff.x, self.dash_eff.y, self.dash_eff.face_dir = self.x +128, self.y, self.face_dir
        else:
            self.dash_eff.x, self.dash_eff.y, self.dash_eff.face_dir = self.x -128, self.y,self.face_dir

        game_world.add_object(self.dash_eff, 2)


