import random

from sdl2 import SDL_KEYDOWN, SDLK_s

import game_world
from pico2d import load_image, get_time, clamp, load_wav

import game_framework
import server
from boss import DieEnd, DieStart
from dasheff import DashEff
from hiteff import HitEff
from slasheff import SlashEff
from state_machine import (right_down, left_up, left_down, right_up, start_event, StateMachine, z_down, x_down,
                           end_motion, up_down, up_up, s_down, landed, fall, die)

PIXEL_PER_METER = (10.0 / 0.2)

RUN_SPEED_KMPH = 30.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

DASH_SPEED_KMPH = 80.0
DASH_SPEED_MPM = (DASH_SPEED_KMPH * 1000.0 / 60.0)
DASH_SPEED_MPS = (DASH_SPEED_MPM / 60.0)
DASH_SPEED_PPS = (DASH_SPEED_MPS * PIXEL_PER_METER)


JUMP_SPEED_KMPH = 40.0
JUMP_SPEED_MPM = (JUMP_SPEED_KMPH * 1000.0 / 60.0)
JUMP_SPEED_MPS = (JUMP_SPEED_MPM / 60.0)
JUMP_SPEED_PPS = (JUMP_SPEED_MPS * PIXEL_PER_METER)


TIME_PER_ACTION = 0.5
TIME_PER_DASH_ACTION = 0.3
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
DASH_ACTION_PER_TIME = 1.0 / TIME_PER_DASH_ACTION
FRAMES_PER_ACTION_IDLE = 9
FRAMES_PER_ACTION_RUN = 8
FRAMES_PER_ACTION_SLASH = 5
FRAMES_PER_ACTION_DASH = 7
FRAMES_PER_ACTION_JUMP = 12
FRAMES_PER_ACTION_FALL = 6
FRAMES_PER_ACTION_DIE = 3


class Die:
    @staticmethod
    def enter(knight, e):
        if die(e):
            knight.action = 8  # 낙하 동작의 인덱스를 8로 설정
            knight.frame = 0
    @staticmethod
    def exit(knight, e):
        if knight.frame > 12:
            knight.die = True
        pass
    @staticmethod
    def do(knight):
        knight.frame = (knight.frame + FRAMES_PER_ACTION_DIE * ACTION_PER_TIME * game_framework.frame_time)
        if knight.frame > 12:
            knight.state_machine.add_event(('END_MOTION', 0))

    @staticmethod
    def draw(knight):
        sx = knight.x - server.stage.window_left
        sy = knight.y - server.stage.window_bottom
        if knight.face_dir == 1:
            knight.image.clip_composite_draw(
                int(knight.frame) * 128, knight.action * 128, 128, 128, 0, 'h', sx, sy, 128, 128)
        else:
            knight.image.clip_draw(int(knight.frame) * 128, knight.action * 128, 128, 128, sx, sy)

    @staticmethod
    def get_bb(knight):
        return knight.x - 30, knight.y - 65, knight.x + 30, knight.y + 40

class UpDie:
    @staticmethod
    def enter(knight, e):
        if die(e):
            knight.action = 8  # 낙하 동작의 인덱스를 8로 설정
            knight.frame = 0

    @staticmethod
    def exit(knight, e):
        if knight.frame > 12:
            knight.die = True
        pass

    @staticmethod
    def do(knight):
        knight.frame = (knight.frame + FRAMES_PER_ACTION_DIE * ACTION_PER_TIME * game_framework.frame_time)
        if knight.frame > 12:
            knight.state_machine.add_event(('END_MOTION', 0))

    @staticmethod
    def draw(knight):
        sx = knight.x - server.stage.window_left
        sy = knight.y - server.stage.window_bottom
        if knight.face_dir == 1:
            knight.image.clip_composite_draw(
                int(knight.frame) * 128, knight.action * 128, 128, 128, 0, 'h', sx, sy, 128, 128)
        else:
            knight.image.clip_draw(int(knight.frame) * 128, knight.action * 128, 128, 128, sx, sy)

    @staticmethod
    def get_bb(knight):
        return knight.x - 30, knight.y - 65, knight.x + 30, knight.y + 40

class MoveDie:
    @staticmethod
    def enter(knight, e):
        if die(e):
            knight.action = 8  # 낙하 동작의 인덱스를 8로 설정
            knight.frame = 0

    @staticmethod
    def exit(knight, e):
        if knight.frame > 12:
            knight.die = True
        pass

    @staticmethod
    def do(knight):
        knight.frame = (knight.frame + FRAMES_PER_ACTION_DIE * ACTION_PER_TIME * game_framework.frame_time)
        if knight.frame > 12:
            knight.state_machine.add_event(('END_MOTION', 0))

    @staticmethod
    def draw(knight):
        sx = knight.x - server.stage.window_left
        sy = knight.y - server.stage.window_bottom
        if knight.face_dir == 1:
            knight.image.clip_composite_draw(
                int(knight.frame) * 128, knight.action * 128, 128, 128, 0, 'h', sx, sy, 128, 128)
        else:
            knight.image.clip_draw(int(knight.frame) * 128, knight.action * 128, 128, 128, sx, sy)

    @staticmethod
    def get_bb(knight):
        return knight.x - 30, knight.y - 65, knight.x + 30, knight.y + 40

class UpMoveDie:
    @staticmethod
    def enter(knight, e):
        if die(e):
            knight.action = 8  # 낙하 동작의 인덱스를 8로 설정
            knight.frame = 0
    @staticmethod
    def exit(knight, e):
        if knight.frame > 12:
            knight.die = True
        pass
    @staticmethod
    def do(knight):
        knight.frame = (knight.frame + FRAMES_PER_ACTION_DIE * ACTION_PER_TIME * game_framework.frame_time)
        if knight.frame > 12:
            knight.state_machine.add_event(('END_MOTION', 0))

    @staticmethod
    def draw(knight):
        sx = knight.x - server.stage.window_left
        sy = knight.y - server.stage.window_bottom
        if knight.face_dir == 1:
            knight.image.clip_composite_draw(
                int(knight.frame) * 128, knight.action * 128, 128, 128, 0, 'h', sx, sy, 128, 128)
        else:
            knight.image.clip_draw(int(knight.frame) * 128, knight.action * 128, 128, 128, sx, sy)

    @staticmethod
    def get_bb(knight):
        return knight.x - 30, knight.y - 65, knight.x + 30, knight.y + 40

class Fall:
    @staticmethod
    def enter(knight, e):
        knight.action = 7  # 낙하 동작의 인덱스를 8로 설정
        knight.frame = 0
        knight.y_dir = -1  # 기사가 아래로 이동하도록 설정
    @staticmethod
    def exit(knight, e):
        pass

    @staticmethod
    def do(knight):
        knight.y += knight.y_dir * RUN_SPEED_PPS * game_framework.frame_time
        if knight.y_dir > - 2.5:
            knight.y_dir += -0.0098
        knight.frame = (knight.frame + FRAMES_PER_ACTION_FALL * ACTION_PER_TIME * game_framework.frame_time)
        if knight.frame > 5:
            knight.frame = 3

    @staticmethod
    def draw(knight):
        sx = knight.x - server.stage.window_left
        sy = knight.y - server.stage.window_bottom
        if knight.face_dir == 1:
            knight.image.clip_composite_draw(
                int(knight.frame) * 128, knight.action * 128, 128, 128, 0, 'h', sx, sy, 128, 128)
        else:
            knight.image.clip_draw(int(knight.frame) * 128, knight.action * 128, 128, 128, sx, sy)
    @staticmethod
    def get_bb(knight):
        return knight.x - 30, knight.y - 65, knight.x + 30, knight.y + 40

class UpFall:
    @staticmethod
    def enter(knight, e):
        knight.action = 7  # 낙하 동작의 인덱스를 8로 설정
        knight.frame = 0
        knight.y_dir = -1  # 기사가 아래로 이동하도록 설정
    @staticmethod
    def exit(knight, e):
        pass

    @staticmethod
    def do(knight):
        knight.y += knight.y_dir * RUN_SPEED_PPS * game_framework.frame_time
        if knight.y_dir > -2.5:
            knight.y_dir += -0.0098
        knight.frame = (knight.frame + FRAMES_PER_ACTION_FALL * ACTION_PER_TIME * game_framework.frame_time)
        if knight.frame > 5:
            knight.frame = 3

    @staticmethod
    def draw(knight):
        sx = knight.x - server.stage.window_left
        sy = knight.y - server.stage.window_bottom
        if knight.face_dir == 1:
            knight.image.clip_composite_draw(
                int(knight.frame) * 128, knight.action * 128, 128, 128, 0, 'h', sx, sy, 128, 128)
        else:
            knight.image.clip_draw(int(knight.frame) * 128, knight.action * 128, 128, 128, sx, sy)
    @staticmethod
    def get_bb(knight):
        return knight.x - 30, knight.y - 65, knight.x + 30, knight.y + 40

class MoveFall:
    @staticmethod
    def enter(knight, e):
        if right_down(e) or left_up(e):
            knight.face_dir = 1
            knight.x_dir = 1
            pass
        elif left_down(e) or right_up(e):
            knight.face_dir = -1
            knight.x_dir = -1
        knight.action = 7  # 낙하 동작의 인덱스를 8로 설정
        knight.frame = 0
        knight.y_dir = -1  # 기사가 아래로 이동하도록 설정
    @staticmethod
    def exit(knight, e):
        pass

    @staticmethod
    def do(knight):
        knight.y += knight.y_dir * RUN_SPEED_PPS * game_framework.frame_time
        if knight.y_dir > -2.5:
            knight.y_dir += -0.0098
        knight.x += knight.x_dir * RUN_SPEED_PPS * game_framework.frame_time

        knight.x = clamp(30.0, knight.x, server.stage.w - 30.0)
        knight.frame = (knight.frame + FRAMES_PER_ACTION_FALL * ACTION_PER_TIME * game_framework.frame_time)
        if knight.frame > 5:
            knight.frame = 3

    @staticmethod
    def draw(knight):
        sx = knight.x - server.stage.window_left
        sy = knight.y - server.stage.window_bottom
        if knight.face_dir == 1:
            knight.image.clip_composite_draw(
                int(knight.frame) * 128, knight.action * 128, 128, 128, 0, 'h', sx, sy, 128, 128)
        else:
            knight.image.clip_draw(int(knight.frame) * 128, knight.action * 128, 128, 128, sx, sy)
    @staticmethod
    def get_bb(knight):
        return knight.x - 30, knight.y - 65, knight.x + 30, knight.y + 40

class UpMoveFall:
    @staticmethod
    def enter(knight, e):
        if right_down(e) or left_up(e):
            knight.face_dir = 1
            knight.x_dir = 1
            pass
        elif left_down(e) or right_up(e):
            knight.face_dir = -1
            knight.x_dir = -1
        knight.action = 7  # 낙하 동작의 인덱스를 8로 설정
        knight.frame = 0
        knight.y_dir = -1  # 기사가 아래로 이동하도록 설정
    @staticmethod
    def exit(knight, e):
        pass

    @staticmethod
    def do(knight):
        knight.x += knight.x_dir * RUN_SPEED_PPS * game_framework.frame_time
        knight.x = clamp(30.0, knight.x, server.stage.w - 30.0)
        knight.y += knight.y_dir * RUN_SPEED_PPS * game_framework.frame_time
        if knight.y_dir > -2.5:
            knight.y_dir += -0.0098
        knight.frame = (knight.frame + FRAMES_PER_ACTION_FALL * ACTION_PER_TIME * game_framework.frame_time)
        if knight.frame > 5:
            knight.frame = 3

    @staticmethod
    def draw(knight):
        sx = knight.x - server.stage.window_left
        sy = knight.y - server.stage.window_bottom
        if knight.face_dir == 1:
            knight.image.clip_composite_draw(
                int(knight.frame) * 128, knight.action * 128, 128, 128, 0, 'h', sx, sy, 128, 128)
        else:
            knight.image.clip_draw(int(knight.frame) * 128, knight.action * 128, 128, 128, sx, sy)

    @staticmethod
    def get_bb(knight):
        return knight.x - 30, knight.y - 65, knight.x + 30, knight.y + 40

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
            knight.x_dir = 0
    @staticmethod
    def exit(knight , e):
        pass
    @staticmethod
    def do(knight):
        if not knight.on_ground:  # 지면에 없을 경우 낙하 시작
            knight.state_machine.add_event(('FALLING', 0))
        knight.frame = (knight.frame + FRAMES_PER_ACTION_IDLE * ACTION_PER_TIME * game_framework.frame_time) % 9
    @staticmethod
    def draw(knight):
        sx = knight.x - server.stage.window_left
        sy = knight.y - server.stage.window_bottom
        if knight.face_dir == 1:
            knight.image.clip_composite_draw(
                int(knight.frame) * 128, knight.action * 128, 128, 128, 0, 'h', sx, sy, 128, 128)
        else:
            knight.image.clip_draw(int(knight.frame) * 128, knight.action * 128, 128, 128, sx, sy)
    @staticmethod
    def get_bb(knight):
        return knight.x - 30, knight.y - 65, knight.x + 30, knight.y + 40

class UpIdle:
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
            knight.x_dir = 0
        pass
    @staticmethod
    def exit(knight , e):
        pass
    @staticmethod
    def do(knight):
        if not knight.on_ground:  # 지면에 없을 경우 낙하 시작
            knight.state_machine.add_event(('FALLING', 0))
        knight.frame = (knight.frame + FRAMES_PER_ACTION_IDLE * ACTION_PER_TIME * game_framework.frame_time) % 9
    @staticmethod
    def draw(knight):
        sx = knight.x - server.stage.window_left
        sy = knight.y - server.stage.window_bottom
        if knight.face_dir == 1:
            knight.image.clip_composite_draw(
                int(knight.frame) * 128, knight.action * 128, 128, 128, 0, 'h', sx, sy, 128, 128)
        else:
            knight.image.clip_draw(int(knight.frame) * 128, knight.action * 128, 128, 128, sx, sy)

    @staticmethod
    def get_bb(knight):
        return knight.x - 30, knight.y - 65, knight.x + 30, knight.y + 40

class Run:
    @staticmethod
    def enter(knight , e):
        if right_down(e) or left_up(e):
            knight.face_dir = 1
            knight.x_dir = 1
            pass
        elif left_down(e) or right_up(e):
            knight.face_dir = -1
            knight.x_dir = -1
            pass
        if not up_up(e):
            knight.action = 3
            knight.frame = 0
    @staticmethod
    def exit(knight , e):
        pass
    @staticmethod
    def do(knight):
        if not knight.on_ground:  # 지면에 없을 경우 낙하 시작
            knight.state_machine.add_event(('FALLING', 0))
        knight.frame = (knight.frame + FRAMES_PER_ACTION_RUN * ACTION_PER_TIME * game_framework.frame_time)
        if knight.frame > 9:
            knight.frame = 5

        knight.x += knight.x_dir * RUN_SPEED_PPS * game_framework.frame_time
        knight.x = clamp(30.0, knight.x, server.stage.w - 30.0)
        knight.slash_eff.x += knight.x_dir * RUN_SPEED_PPS * game_framework.frame_time
    @staticmethod
    def draw(knight):
        sx = knight.x - server.stage.window_left
        sy = knight.y - server.stage.window_bottom
        if knight.face_dir == 1:
            knight.image.clip_composite_draw(
                int(knight.frame) * 128, knight.action * 128, 128, 128, 0, 'h', sx, sy, 128, 128)
        else:
            knight.image.clip_draw(int(knight.frame) * 128, knight.action * 128, 128, 128, sx, sy)

    @staticmethod
    def get_bb(knight):
        return knight.x - 30, knight.y - 65, knight.x + 30, knight.y + 40

class UpRun:
    @staticmethod
    def enter(knight , e):
        if right_down(e) or left_up(e):
            knight.face_dir = 1
            knight.x_dir = 1
            pass
        elif left_down(e) or right_up(e):
            knight.face_dir = -1
            knight.x_dir = -1
            pass

        if not up_down(e):
            knight.action = 3
            knight.frame = 0
    @staticmethod
    def exit(knight , e):
        pass
    @staticmethod
    def do(knight):
        if not knight.on_ground:  # 지면에 없을 경우 낙하 시작
            knight.state_machine.add_event(('FALLING', 0))
        knight.frame = (knight.frame + FRAMES_PER_ACTION_RUN * ACTION_PER_TIME * game_framework.frame_time)
        if knight.frame > 9:
            knight.frame = 5

        knight.x += knight.x_dir * RUN_SPEED_PPS * game_framework.frame_time
        knight.slash_eff.x += knight.x_dir * RUN_SPEED_PPS * game_framework.frame_time
        knight.x = clamp(30.0, knight.x, server.stage.w - 30.0)
    @staticmethod
    def draw(knight):
        sx = knight.x - server.stage.window_left
        sy = knight.y - server.stage.window_bottom
        if knight.face_dir == 1:
            knight.image.clip_composite_draw(
                int(knight.frame) * 128, knight.action * 128, 128, 128, 0, 'h', sx, sy, 128, 128)
        else:
            knight.image.clip_draw(int(knight.frame) * 128, knight.action * 128, 128, 128, sx, sy)


    @staticmethod
    def get_bb(knight):
        return knight.x - 30, knight.y - 65, knight.x + 30, knight.y + 40

class Slash:
    @staticmethod
    def enter(knight , e):
        if x_down(e):
            knight.sword_sound.play(1)
            knight.frame = 0
            knight.action = random.randint(1, 2)
            knight.knight_slash()
    @staticmethod
    def exit(knight , e):
        pass
    @staticmethod
    def do(knight):
        knight.frame = (knight.frame + FRAMES_PER_ACTION_SLASH * ACTION_PER_TIME * game_framework.frame_time)
        if knight.frame > 4:
            knight.state_machine.add_event(('END_MOTION', 0))

        knight.y += knight.y_dir * RUN_SPEED_PPS * game_framework.frame_time
        knight.slash_eff.y += knight.y_dir * RUN_SPEED_PPS * game_framework.frame_time
    @staticmethod
    def draw(knight):
        sx = knight.x - server.stage.window_left
        sy = knight.y - server.stage.window_bottom
        if knight.face_dir == 1:
            knight.image.clip_composite_draw(
                int(knight.frame) * 128, knight.action * 128, 128, 128,
                0, 'h',
                sx, sy, 128, 128
            )
        else:
            knight.image.clip_draw(int(knight.frame) * 128, knight.action * 128, 128, 128, sx, sy)
    @staticmethod
    def get_bb(knight):
        return knight.x - 30, knight.y - 65, knight.x + 30, knight.y + 40

class UpSlash:
    @staticmethod
    def enter(knight , e):
        if x_down(e):
            knight.sword_sound.play(1)
            knight.frame = 0
            knight.action = 0
            knight.knight_slash()
    @staticmethod
    def exit(knight , e):
        pass
    @staticmethod
    def do(knight):
        knight.frame = (knight.frame + FRAMES_PER_ACTION_SLASH * ACTION_PER_TIME * game_framework.frame_time)
        if knight.frame > 4:
            knight.state_machine.add_event(('END_MOTION', 0))

        knight.y += knight.y_dir * RUN_SPEED_PPS * game_framework.frame_time
        knight.slash_eff.y += knight.y_dir * RUN_SPEED_PPS * game_framework.frame_time
    @staticmethod
    def draw(knight):
        sx = knight.x - server.stage.window_left
        sy = knight.y - server.stage.window_bottom
        if knight.face_dir == 1:
            knight.image.clip_composite_draw(
                int(knight.frame) * 128, knight.action * 128, 128, 128,
                0, 'h',
                sx - 16, sy, 128, 128)
        else:
            knight.image.clip_draw(int(knight.frame) * 128, knight.action * 128, 128, 128, sx + 16,
                                       sy)

    @staticmethod
    def get_bb(knight):
        return knight.x - 30, knight.y - 65, knight.x + 30, knight.y + 40

class MoveSlash:
    @staticmethod
    def enter(knight , e):
        if right_down(e) or left_up(e):
            knight.face_dir = 1
            knight.x_dir = 1
            pass
        elif left_down(e) or right_up(e):
            knight.face_dir = -1
            knight.x_dir = -1
            pass
        elif x_down(e):
            knight.sword_sound.play()
            knight.frame = 0
            knight.action = random.randint(1, 2)
            knight.knight_slash()
    @staticmethod
    def exit(knight , e):
        pass
    @staticmethod
    def do(knight):
        knight.frame = (knight.frame + FRAMES_PER_ACTION_SLASH * ACTION_PER_TIME * game_framework.frame_time)
        if knight.frame > 4:
            knight.state_machine.add_event(('END_MOTION', 0))

        knight.x += knight.x_dir * RUN_SPEED_PPS * game_framework.frame_time
        knight.x = clamp(30.0, knight.x, server.stage.w - 30.0)
        knight.slash_eff.x += knight.x_dir * RUN_SPEED_PPS * game_framework.frame_time
        knight.y += knight.y_dir * RUN_SPEED_PPS * game_framework.frame_time
        knight.slash_eff.y += knight.y_dir * RUN_SPEED_PPS * game_framework.frame_time
    @staticmethod
    def draw(knight):
        sx = knight.x - server.stage.window_left
        sy = knight.y - server.stage.window_bottom
        if knight.face_dir == 1:
            knight.image.clip_composite_draw(
                int(knight.frame) * 128, knight.action * 128, 128, 128,
                0, 'h',
                sx, sy, 128, 128
            )
        else:
            knight.image.clip_draw(int(knight.frame) * 128, knight.action * 128, 128, 128, sx, sy)

    @staticmethod
    def get_bb(knight):
        return knight.x - 30, knight.y - 65, knight.x + 30, knight.y + 40

class UpMoveSlash:
    @staticmethod
    def enter(knight , e):
        if right_down(e) or left_up(e):
            knight.face_dir = 1
            knight.x_dir = 1
        elif left_down(e) or right_up(e):
            knight.face_dir = -1
            knight.x_dir = -1
        elif x_down(e):
            knight.sword_sound.play(1)
            knight.frame = 0
            knight.action = 0
            knight.knight_slash()
    @staticmethod
    def exit(knight , e):
        pass
    @staticmethod
    def do(knight):
        knight.frame = (knight.frame + FRAMES_PER_ACTION_SLASH * ACTION_PER_TIME * game_framework.frame_time)
        if knight.frame > 4:
            knight.state_machine.add_event(('END_MOTION', 0))

        knight.x += knight.x_dir * RUN_SPEED_PPS * game_framework.frame_time
        knight.x = clamp(30.0, knight.x, server.stage.w - 30.0)
        knight.slash_eff.x += knight.x_dir * RUN_SPEED_PPS * game_framework.frame_time
        knight.y += knight.y_dir * RUN_SPEED_PPS * game_framework.frame_time
        knight.slash_eff.y += knight.y_dir * RUN_SPEED_PPS * game_framework.frame_time
    @staticmethod
    def draw(knight):
        sx = knight.x - server.stage.window_left
        sy = knight.y - server.stage.window_bottom
        if knight.face_dir == 1:
            knight.image.clip_composite_draw(
                 int(knight.frame) * 128, knight.action * 128, 128, 128,
                0, 'h',
                sx - 16, sy, 128, 128
            )
        else:
            knight.image.clip_draw(int(knight.frame) * 128, knight.action * 128, 128, 128, sx + 16,
                                       sy)

    @staticmethod
    def get_bb(knight):
        return knight.x - 30, knight.y - 65, knight.x + 30, knight.y + 40

class Dash:
    @staticmethod
    def enter(knight , e):
        if s_down(e):
            knight.dash_sound.play()
            knight.frame = 0
            knight.action = 5
            knight.jump_frame = 12
            knight.knight_dash()
        pass
    @staticmethod
    def exit(knight , e):
        pass
    @staticmethod
    def do(knight):
        knight.frame = (knight.frame + FRAMES_PER_ACTION_DASH * DASH_ACTION_PER_TIME * game_framework.frame_time)
        if knight.frame > 6:
            knight.state_machine.add_event(('END_MOTION', 0))

        knight.x += knight.x_dir * DASH_SPEED_PPS * game_framework.frame_time
        knight.x = clamp(30.0, knight.x, server.stage.w - 30.0)
        knight.dash_eff.x += knight.x_dir * DASH_SPEED_PPS * game_framework.frame_time
    @staticmethod
    def draw(knight):
        sx = knight.x - server.stage.window_left
        sy = knight.y - server.stage.window_bottom
        if knight.face_dir == 1:
            knight.image.clip_composite_draw(
                int(knight.frame) * 256, knight.action * 128, 256, 128, 0, 'h', sx - 60, sy, 256, 128)
        else:
            knight.image.clip_draw(int(knight.frame) * 256, knight.action * 128, 256, 128, sx + 60, sy)
    @staticmethod
    def get_bb(knight):
        if knight.face_dir == 1:
            return knight.x , knight.y - 65, knight.x + 60, knight.y + 40
        else:
            return knight.x - 60, knight.y - 65, knight.x, knight.y + 40

class UpDash:
    @staticmethod
    def enter(knight , e):
        if s_down(e):
            knight.dash_sound.play()
            knight.frame = 0
            knight.action = 5
            knight.jump_frame = 12
            knight.knight_dash()
        pass
    @staticmethod
    def exit(knight , e):
        pass
    @staticmethod
    def do(knight):
        knight.frame = (knight.frame + FRAMES_PER_ACTION_DASH * DASH_ACTION_PER_TIME * game_framework.frame_time)
        if knight.frame > 6:
            knight.state_machine.add_event(('END_MOTION', 0))

        knight.x += knight.x_dir * DASH_SPEED_PPS * game_framework.frame_time
        knight.x = clamp(30.0, knight.x, server.stage.w - 30.0)
        knight.dash_eff.x += knight.x_dir * DASH_SPEED_PPS * game_framework.frame_time
    @staticmethod
    def draw(knight):
        sx = knight.x - server.stage.window_left
        sy = knight.y - server.stage.window_bottom
        if knight.face_dir == 1:
            knight.image.clip_composite_draw(
                int(knight.frame) * 256, knight.action * 128, 256, 128, 0, 'h', sx - 60, sy, 256, 128)
        else:
            knight.image.clip_draw(int(knight.frame) * 256, knight.action * 128, 256, 128, sx + 60, sy)

    @staticmethod
    def get_bb(knight):
        if knight.face_dir == 1:
            return knight.x, knight.y - 65, knight.x + 60, knight.y + 40
        else:
            return knight.x - 60, knight.y - 65, knight.x, knight.y + 40

class Jump:
    @staticmethod
    def enter(knight , e):
        if z_down(e):
            knight.jump_sound.play()
            knight.jump_frame = 0
            knight.action = 6
            knight.y_dir = 1
            knight.jump = True
        pass
    @staticmethod
    def exit(knight , e):
        pass
    @staticmethod
    def do(knight):
        if knight.y_dir > 0:
            knight.y += knight.y_dir * JUMP_SPEED_PPS * game_framework.frame_time
        else:
            knight.y += knight.y_dir * RUN_SPEED_PPS * game_framework.frame_time
            if knight.y_dir > -2.5:
                knight.y_dir += -0.0098
    @staticmethod
    def draw(knight):
        sx = knight.x - server.stage.window_left
        sy = knight.y - server.stage.window_bottom
        if knight.face_dir == 1:
            knight.image.clip_composite_draw(
                int(knight.jump_frame) * 128, knight.action * 128, 128, 128, 0, 'h', sx - 15, sy, 128, 128)
        else:
            knight.image.clip_draw(int(knight.jump_frame) * 128, knight.action * 128, 128, 128, sx + 15, sy)

    @staticmethod
    def get_bb(knight):
        if knight.face_dir == 1:
            return knight.x - 30, knight.y - 65, knight.x + 30, knight.y + 40
        else:
            return knight.x - 30, knight.y - 65, knight.x + 30, knight.y + 40

class MoveJump:
    @staticmethod
    def enter(knight , e):
        if right_down(e) or left_up(e):
            knight.face_dir = 1
            knight.x_dir = 1
            pass
        elif left_down(e) or right_up(e):
            knight.face_dir = -1
            knight.x_dir = -1
            pass
        elif z_down(e):
            knight.jump_sound.play()
            knight.jump_frame = 0
            knight.action = 6
            knight.y_dir = 1
            knight.jump = True
        pass
    @staticmethod
    def exit(knight , e):
        pass
    @staticmethod
    def do(knight):
        if knight.y_dir > 0:
            knight.y += knight.y_dir * JUMP_SPEED_PPS * game_framework.frame_time
        else:
            knight.y += knight.y_dir * RUN_SPEED_PPS * game_framework.frame_time
            if knight.y_dir > -2.5:
                knight.y_dir += -0.0098
        knight.x += knight.x_dir * RUN_SPEED_PPS * game_framework.frame_time
        knight.x = clamp(30.0, knight.x, server.stage.w - 30.0)
    @staticmethod
    def draw(knight):
        sx = knight.x - server.stage.window_left
        sy = knight.y - server.stage.window_bottom
        if knight.face_dir == 1:
            knight.image.clip_composite_draw(
                int(knight.jump_frame) * 128, knight.action * 128, 128, 128, 0, 'h', sx - 15, sy, 128, 128)
        else:
            knight.image.clip_draw(int(knight.jump_frame) * 128, knight.action * 128, 128, 128, sx + 15, sy)

    @staticmethod
    def get_bb(knight):
        if knight.face_dir == 1:
            return knight.x - 30, knight.y - 65, knight.x + 30, knight.y + 40
        else:
            return knight.x - 30, knight.y - 65, knight.x + 30, knight.y + 40

class UpJump:
    @staticmethod
    def enter(knight , e):
        if z_down(e):
            knight.jump_sound.play()
            knight.jump_frame = 0
            knight.action = 6
            knight.y_dir = 1
            knight.jump = True
        pass
    @staticmethod
    def exit(knight , e):
        pass
    @staticmethod
    def do(knight):
        if knight.y_dir > 0:
            knight.y += knight.y_dir * JUMP_SPEED_PPS * game_framework.frame_time
        else:
            knight.y += knight.y_dir * RUN_SPEED_PPS * game_framework.frame_time
            if knight.y_dir > -2.5:
                knight.y_dir += -0.0098
    @staticmethod
    def draw(knight):
        sx = knight.x - server.stage.window_left
        sy = knight.y - server.stage.window_bottom
        if knight.face_dir == 1:
            knight.image.clip_composite_draw(
                int(knight.jump_frame) * 128, knight.action * 128, 128, 128, 0, 'h', sx - 15, sy, 128, 128)
        else:
            knight.image.clip_draw(int(knight.jump_frame) * 128, knight.action * 128, 128, 128, sx + 15, sy)

    @staticmethod
    def get_bb(knight):
        if knight.face_dir == 1:
            return knight.x - 30, knight.y - 65, knight.x + 30, knight.y + 40
        else:
            return knight.x - 30, knight.y - 65, knight.x + 30, knight.y + 40

class UpMoveJump:
    @staticmethod
    def enter(knight , e):
        if right_down(e) or left_up(e):
            knight.face_dir = 1
            knight.x_dir = 1
            pass
        elif left_down(e) or right_up(e):
            knight.face_dir = -1
            knight.x_dir = -1
            pass
        elif z_down(e):
            knight.jump_sound.play()
            knight.jump_frame = 0
            knight.action = 6
            knight.y_dir = 1
            knight.jump = True
        pass
    @staticmethod
    def exit(knight , e):
        pass
    @staticmethod
    def do(knight):
        if knight.y_dir > 0:
            knight.y += knight.y_dir * JUMP_SPEED_PPS * game_framework.frame_time
        else:
            knight.y += knight.y_dir * RUN_SPEED_PPS * game_framework.frame_time
            if knight.y_dir > -2.5:
                knight.y_dir += -0.0098
        knight.x += knight.x_dir * RUN_SPEED_PPS * game_framework.frame_time
        knight.x = clamp(30.0, knight.x, server.stage.w - 30.0)
    @staticmethod
    def draw(knight):
        sx = knight.x - server.stage.window_left
        sy = knight.y - server.stage.window_bottom
        if knight.face_dir == 1:
            knight.image.clip_composite_draw(
                int(knight.jump_frame) * 128, knight.action * 128, 128, 128, 0, 'h', sx - 15, sy, 128, 128)
        else:
            knight.image.clip_draw(int(knight.jump_frame) * 128, knight.action * 128, 128, 128, sx + 15, sy)

    @staticmethod
    def get_bb(knight):
        if knight.face_dir == 1:
            return knight.x - 30, knight.y - 65, knight.x + 30, knight.y + 40
        else:
            return knight.x - 30, knight.y - 65, knight.x + 30, knight.y + 40

class Knight:
    image = None
    damage_sound = None
    dash_sound = None
    land_sound = None
    jump_sound = None
    sword_sound = None
    die_sound = None
    def __init__(self,stage = 1 , dash = False , state = Idle):
        self.x, self.y = 100 ,200
        self.frame = 0
        self.back_x = 0
        self.jump_frame = 0
        self.jump = False
        self.on_ground = False
        self.die = False
        self.dash = dash
        self.attack_dir = 1
        self.invincibility_time = 0
        self.x_dir = 1
        self.y_dir = -1
        self.action = 0
        self.face_dir = 1
        self.stage = stage
        self.hit_eff = HitEff()
        self.hp = 4
        self.slash_eff = SlashEff()
        self.dash_eff = DashEff()
        self.state_machine = StateMachine(self)
        self.state_machine.start(state)
        self.state_machine.set_transitions(
            {
                Die: {end_motion: Idle ,right_down: MoveDie, left_down: MoveDie, left_up: MoveDie, right_up: MoveDie, up_down:UpDie},
                UpDie: {end_motion: UpIdle, right_down: UpMoveDie, left_down: UpMoveDie, left_up: UpMoveDie,right_up: UpMoveDie, up_up: Die},

                MoveDie: {end_motion: Run, right_down: Die, left_down: Die, right_up: Die, left_up: Die,up_down: UpMoveDie},
                UpMoveDie: {end_motion: UpRun ,right_down: UpDie, left_down: UpDie, right_up: UpDie, left_up: UpDie, up_up:MoveDie},

                Idle:{die: Die ,fall: Fall, right_down: Run, left_down: Run, left_up: Run, right_up: Run, x_down: Slash, z_down: Jump, up_down:UpIdle},
                UpIdle: {die: UpDie ,fall: UpFall, right_down: UpRun, left_down: UpRun, left_up: UpRun, right_up: UpRun, x_down: UpSlash, z_down: UpJump, up_up:Idle},

                Run: {die: MoveDie ,fall: MoveFall, right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, x_down: MoveSlash , s_down:Dash, z_down: MoveJump, up_down:UpRun},
                UpRun: {die: UpMoveDie, fall: UpMoveFall , right_down: UpIdle, left_down: UpIdle, right_up: UpIdle, left_up: UpIdle, x_down: UpMoveSlash, s_down:UpDash, z_down: UpMoveJump, up_up:Run},

                Slash:{die: Die ,end_motion: Idle , right_down: MoveSlash, left_down: MoveSlash, right_up: MoveSlash, left_up: MoveSlash , up_down:UpSlash},
                UpSlash: {die: UpDie, end_motion: UpIdle, right_down: UpMoveSlash, left_down: UpMoveSlash,right_up: UpMoveSlash, left_up: UpMoveSlash, up_up: Slash},

                MoveSlash:{die: MoveDie ,end_motion: Run, right_down: Slash, left_down: Slash, right_up: Slash, left_up: Slash , up_down:UpMoveSlash},
                UpMoveSlash: {die: UpMoveDie,end_motion: UpRun, right_down: UpSlash, left_down: UpSlash, right_up: UpSlash, left_up: UpSlash , up_up:MoveSlash},

                Dash:{die: MoveDie,end_motion: Run , right_down: Idle, left_down: Idle, left_up: Idle, right_up: Idle, up_down:UpDash},
                UpDash: {die: UpMoveDie,end_motion: UpRun, right_down: UpIdle, left_down: UpIdle, left_up: UpIdle, right_up: UpIdle, up_up:Dash},

                Jump:{die: Die,landed: Idle , right_down: MoveJump, left_down: MoveJump, right_up: MoveJump, left_up: MoveJump, x_down:Slash,up_down:UpJump},
                UpJump: {die: UpDie,landed: UpIdle, right_down: UpMoveJump, left_down: UpMoveJump, right_up: UpMoveJump,left_up: UpMoveJump, x_down: UpSlash, up_up: Jump},

                MoveJump:{die: MoveDie,landed: Run, right_down: Jump, left_down: Jump, right_up: Jump, left_up: Jump, x_down:MoveSlash, s_down:Dash, up_down:UpMoveJump},
                UpMoveJump: {die: UpMoveDie,landed: UpRun, right_down: UpJump, left_down: UpJump, right_up: UpJump, left_up: UpJump, x_down:UpMoveSlash, s_down:UpDash,up_up:MoveJump},

                Fall:{die: Die,landed: Idle, right_down: MoveFall, left_down: MoveFall, right_up: MoveFall, left_up: MoveFall, x_down: Slash,up_down:UpFall},
                UpFall: {die: UpDie,landed: UpIdle, right_down: UpMoveFall, left_down: UpMoveFall, right_up: UpMoveFall,left_up: UpMoveFall, x_down: UpSlash, up_up: Fall},

                MoveFall: {die: MoveDie,landed: Run, right_down: Fall, left_down: Fall, right_up: Fall, left_up: Fall, x_down: MoveSlash, s_down:Dash,up_down:UpMoveFall},
                UpMoveFall: {die: UpMoveDie,landed: UpRun, right_down: UpFall, left_down: UpFall, right_up: UpFall, left_up: UpFall, x_down: UpMoveSlash, s_down:UpDash  , up_up:MoveFall},
            }
        )
        if Knight.image is None:
            Knight.image = load_image('./resource/knight.png')
        if Knight.damage_sound is None:
            Knight.damage_sound = load_wav('./resource/damage.wav')
            Knight.dash_sound = load_wav('./resource/dash.wav')
            Knight.land_sound = load_wav('./resource/land.wav')
            Knight.sword_sound = load_wav('./resource/sword.wav')
            Knight.jump_sound = load_wav('./resource/jump.wav')
            Knight.die_sound = load_wav('./resource/die.wav')
            Knight.damage_sound.set_volume(32)
            Knight.dash_sound.set_volume(32)
            Knight.land_sound.set_volume(32)
            Knight.sword_sound.set_volume(32)
            Knight.jump_sound.set_volume(32)
            Knight.die_sound.set_volume(32)

    def update(self):
        self.state_machine.update()

        if self.back_x > 0:
            if self.attack_dir < 0:
                self.x += -2 * RUN_SPEED_PPS * game_framework.frame_time
                self.slash_eff.x += -2 * RUN_SPEED_PPS * game_framework.frame_time
                self.dash_eff.x += -2 * RUN_SPEED_PPS * game_framework.frame_time
            else:
                self.x += 2 * RUN_SPEED_PPS * game_framework.frame_time
                self.slash_eff.x += 2 * RUN_SPEED_PPS * game_framework.frame_time
                self.dash_eff.x += 2 * RUN_SPEED_PPS * game_framework.frame_time
            self.back_x -= 1
            self.x = clamp(30.0, self.x, server.stage.w - 30.0)

        if self.on_ground:  # 현재 지면에 있는 상태라면
            tile_below = server.stage.get_tile_below(self)  # 캐릭터 아래 타일 확인 (구현 필요)
            if not tile_below:  # 아래에 타일이 없으면
                self.on_ground = False  # 지면에서 떨어짐
                if self.state_machine.cur_state not in (Fall, MoveFall, UpFall, UpMoveFall):
                    if self.state_machine.cur_state in (Slash, UpSlash, MoveSlash, UpMoveSlash):
                        self.y_dir = -1
                    self.state_machine.add_event(('FALLING', 0))  # 낙하 상태로 전환

        if self.jump_frame < 11:
            if self.y_dir == -1:
                self.jump_frame = (
                        self.jump_frame + FRAMES_PER_ACTION_FALL * ACTION_PER_TIME * game_framework.frame_time)
            else:
                self.jump_frame = (
                            self.jump_frame + FRAMES_PER_ACTION_JUMP * ACTION_PER_TIME * game_framework.frame_time)

        if self.jump_frame > 11 and self.jump == True:
            self.y_dir = -1
            self.jump = False

        if self.jump_frame > 11:
            self.jump_frame = 9

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN and event.key == SDLK_s and not self.dash:
            return
        self.state_machine.add_event(
            ('INPUT', event)
        )
    def draw(self):
        self.state_machine.draw()

    def knight_slash(self):
        self.slash_eff = SlashEff()
        x_offset = 64 if self.action != 0 else 0
        y_offset = 64 if self.action == 0 else 0
        self.slash_eff.x = self.x + (x_offset if self.face_dir == 1 else -x_offset)
        self.slash_eff.y = self.y + y_offset
        self.slash_eff.action = self.action
        self.slash_eff.face_dir = self.face_dir

        game_world.add_object(self.slash_eff, 2)
        game_world.add_collision_pair('slash:fly', self.slash_eff, None)
        game_world.add_collision_pair('slash:walk', self.slash_eff, None)
        game_world.add_collision_pair('slash:overload', self.slash_eff, None)
        game_world.add_collision_pair('slash:roll', self.slash_eff, None)
        game_world.add_collision_pair('slash:boss', self.slash_eff, None)

    def knight_dash(self):
        self.dash_eff = DashEff()
        dash_offset = 128
        self.dash_eff.x = self.x + (dash_offset if self.face_dir == -1 else -dash_offset)
        self.dash_eff.y = self.y
        self.dash_eff.face_dir = self.face_dir

        game_world.add_object(self.dash_eff, 2)


    def get_bb(self):
        return self.state_machine.get_bb()


    def handle_collision(self, group, other):
        # fill here
        if group == 'knight:tile':
            left , bottom , right, top = self.get_bb()
            if self.state_machine.cur_state in (Dash, UpDash):
                top -= 30
                bottom += 30
            other_left, other_bottom, other_right, other_top = other.get_bb()
            dx_left = other_right - left
            dx_right = right - other_left
            dy_bottom = top - other_bottom
            dy_top = other_top - bottom
            if dx_left > 0 and dx_right > 0 and dy_bottom > 0 and dy_top > 0:
                min_dx = min(dx_left, dx_right)
                min_dy = min(dy_bottom, dy_top)
                if self.state_machine.cur_state in (Dash, UpDash):
                    dash_offset = 128
                    if dx_left < dx_right:  # 왼쪽 충돌
                        self.x = other_right + ((right - left) / 2)
                        self.dash_eff.x = other_right + ((right - left) / 2) + (dash_offset if self.face_dir == -1 else -dash_offset)
                    else:  # 오른쪽 충돌
                        self.x = other_left - ((right - left) / 2)
                        self.dash_eff.x = other_left - ((right - left) / 2)+ (dash_offset if self.face_dir == -1 else -dash_offset)
                elif min_dx < min_dy:  # 좌우 충돌
                    x_offset = 64 if self.action != 0 else 0
                    if dx_left < dx_right:  # 왼쪽 충돌
                        self.x = other_right + ((right - left) / 2)
                        self.slash_eff.x = other_right + ((right - left) / 2) + (x_offset if self.face_dir == 1 else -x_offset)
                    else:  # 오른쪽 충돌
                        self.x = other_left - ((right - left) / 2)
                        self.slash_eff.x = other_left - ((right - left) / 2) + (x_offset if self.face_dir == 1 else -x_offset)
                else:  # 상하 충돌
                    if dy_bottom < dy_top:  # 아래에서 위로 충돌
                        self.y_dir = -1
                        self.jump = False
                        self.jump_frame = 12
                    else:
                        if self.state_machine.cur_state in (Jump, MoveJump, UpJump, UpMoveJump,
                                                            Fall, MoveFall, UpFall, UpMoveFall):
                            if not self.jump:
                                self.land_sound.play()
                                self.state_machine.add_event(('LANDED', 0))
                                self.y = other_top + 65  # 타일 위로 위치 보정
                                self.slash_eff.y = other_top + 65
                                self.on_ground = True
                                self.y_dir = 0
                        elif self.state_machine.cur_state in (Slash, UpSlash, MoveSlash, UpMoveSlash):
                            y_offset = 64 if self.action == 0 else 0
                            self.y = other_top + 65  # 타일 위로 위치 보정
                            self.slash_eff.y = other_top + 65 + y_offset
                            self.on_ground = True
                            self.y_dir = 0

        elif (group == 'knight:fly' or group == 'knight:walk'or group == 'knight:roll'
              or group == 'knight:overload') :
            if get_time() - self.invincibility_time > 1 and other.die == False and self.hp > 0:
                self.invincibility_time = get_time()
                game_world.remove_object(server.hp1[self.hp - 1])
                self.hp -= 1
                self.hit_eff = HitEff(self.x, self.y, self.face_dir)
                self.back_x = 80
                game_world.add_object(self.hit_eff, 2)
                self.attack_dir = self.x - other.x
                self.damage_sound.play()
                if self.hp < 1:
                    Knight.die_sound.play()
                    self.state_machine.add_event(('DIE', 0))

        elif  group == 'knight:boss':
            if get_time() - self.invincibility_time > 1 and other.die == False and self.hp > 0 and not other.state_machine.cur_state in (DieStart, DieEnd):
                self.invincibility_time = get_time()
                game_world.remove_object(server.hp1[self.hp - 1])
                self.hp -= 1
                self.hit_eff = HitEff(self.x, self.y, self.face_dir)
                self.back_x = 80
                game_world.add_object(self.hit_eff, 2)
                self.attack_dir = self.x - other.x
                self.damage_sound.play()
                if self.hp < 1:
                    self.state_machine.add_event(('DIE', 0))
        elif  group == 'knight:attack':
            if get_time() - self.invincibility_time > 1 and self.hp > 0:
                self.invincibility_time = get_time()
                game_world.remove_object(server.hp1[self.hp - 1])
                self.hp -= 1
                self.hit_eff = HitEff(self.x, self.y, self.face_dir)
                self.back_x = 80
                game_world.add_object(self.hit_eff, 2)
                self.attack_dir = self.x - other.x
                self.damage_sound.play()
                if self.hp < 1:
                    self.state_machine.add_event(('DIE', 0))
        elif group == 'knight:goal':
            if other.stage == 1:
                self.stage = 2
            elif other.stage == 2:
                self.stage = 3
            elif other.stage == 3:
                if server.boss and server.boss.die == True:
                    self.stage = 4
            pass





