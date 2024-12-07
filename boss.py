
import game_framework
import game_world

from pico2d import *
import server
from bossattackeff import BossAttackEff
from bossattackeffback import BossAttackEffBack
from hiteff import HitEff
from state_machine import StateMachine, end_motion, landed, jump_time_out, attack_time_out

PIXEL_PER_METER = (10.0 / 0.2)  # 10 pixel 30 cm

RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

JUMP_SPEED_KMPH = 50.0
JUMP_SPEED_MPM = (JUMP_SPEED_KMPH * 1000.0 / 60.0)
JUMP_SPEED_MPS = (JUMP_SPEED_MPM / 60.0)
JUMP_SPEED_PPS = (JUMP_SPEED_MPS * PIXEL_PER_METER)


TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION_IDLE = 5
FRAMES_PER_ACTION_JUMP = 4
FRAMES_PER_ACTION_ATTACK = 6
FRAMES_PER_ACTION_DIE = 9

class Die:
    @staticmethod
    def enter(knight, e):
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

        draw_rectangle(sx - 30, sy - 65, sx + 30, sy + 40)

    @staticmethod
    def get_bb(knight):
        return knight.x - 30, knight.y - 65, knight.x + 30, knight.y + 40

class Idle:
    @staticmethod
    def enter(boss, e):
        boss.dir = math.atan2(server.knight.y - boss.y, server.knight.x - boss.x)
        boss.action = 3  # 낙하 동작의 인덱스를 8로 설정
        boss.frame = 0
        boss.jump_time = get_time()
    @staticmethod
    def exit(boss, e):
        pass
    @staticmethod
    def do(boss):
        boss.frame = (boss.frame + FRAMES_PER_ACTION_IDLE * ACTION_PER_TIME * game_framework.frame_time) % 5
        if boss.distance_less_than(server.knight.x, server.knight.y, boss.x, boss.y, 15):
            if get_time() - boss.attack_time > 13:
                boss.attack_time = get_time()
                boss.state_machine.add_event(('ATTACK_TIME_OUT', 0))
            elif get_time() - boss.jump_time > 3:
                boss.jump_time = get_time()
                boss.tx = server.knight.x
                boss.ty = boss.y
                boss.state_machine.add_event(('JUMP_TIME_OUT', 0))

        boss.y += boss.y_dir * RUN_SPEED_PPS * game_framework.frame_time

    @staticmethod
    def draw(boss):
        sx = boss.x - server.stage.window_left
        sy = boss.y - server.stage.window_bottom
        if math.cos(boss.dir) < 0:
            boss.image.clip_composite_draw(
                int(boss.frame) * 842, boss.action * 624, 842, 624,
                0, 'h',
                sx, sy, 842, 624
            )
        else:
            boss.image.clip_draw(int(boss.frame) * 842, boss.action * 624, 842, 624, sx, sy)

        if math.cos(boss.dir) < 0:
            draw_rectangle(sx - 85, sy - 300, sx + 190, sy- 30)
        else:
            draw_rectangle(sx - 190, sy - 300, sx + 85, sy- 30)

        boss.font.draw(sx - 10, sy + 50, f'{boss.hp:02d}', (255, 255, 0))

    @staticmethod
    def get_bb(boss):
        if math.cos(boss.dir) < 0:
            return boss.x - 85, boss.y - 300, boss.x + 190, boss.y - 30
        else:
            return boss.x - 190, boss.y - 300, boss.x + 85, boss.y - 30

class MoveReady:
    @staticmethod
    def enter(boss, e):
        boss.action = 2  # 낙하 동작의 인덱스를 8로 설정
        boss.frame = 0
    @staticmethod
    def exit(boss, e):
        pass
    @staticmethod
    def do(boss):
        boss.frame = (boss.frame + FRAMES_PER_ACTION_IDLE * ACTION_PER_TIME * game_framework.frame_time)
        if boss.frame > 3:
            boss.state_machine.add_event(('END_MOTION', 0))

    @staticmethod
    def draw(boss):
        sx = boss.x - server.stage.window_left
        sy = boss.y - server.stage.window_bottom
        if math.cos(boss.dir) < 0:
            boss.image.clip_composite_draw(
                int(boss.frame) * 842, boss.action * 624, 842, 624,
                0, 'h',
                sx, sy, 842, 624
            )
        else:
            boss.image.clip_draw(int(boss.frame) * 842, boss.action * 624, 842, 624, sx, sy)

        if math.cos(boss.dir) < 0:
            draw_rectangle(sx - 85, sy - 300, sx + 190, sy- 30)
        else:
            draw_rectangle(sx - 190, sy - 300, sx + 85, sy- 30)

        boss.font.draw(sx - 10, sy + 50, f'{boss.hp:02d}', (255, 255, 0))

    @staticmethod
    def get_bb(boss):
        if math.cos(boss.dir) < 0:
            return boss.x - 85, boss.y - 300, boss.x + 190, boss.y - 30
        else:
            return boss.x - 190, boss.y - 300, boss.x + 85, boss.y - 30

class Move:
    @staticmethod
    def enter(boss, e):
        boss.action = 1  # 낙하 동작의 인덱스를 8로 설정
        boss.frame = 0
        boss.jump = True
        boss.jump_count = 0
        boss.y_dir = 1
        boss.tx = server.knight.x
        boss.ty = boss.y

    @staticmethod
    def exit(boss, e):
        pass

    @staticmethod
    def do(boss):
        boss.frame = (boss.frame + FRAMES_PER_ACTION_IDLE * ACTION_PER_TIME * game_framework.frame_time)
        boss.jump_count = (boss.jump_count + FRAMES_PER_ACTION_IDLE * ACTION_PER_TIME * game_framework.frame_time)
        if boss.frame > 3:
            boss.frame = 2

        if boss.y_dir > 0:
            boss.y += boss.y_dir * JUMP_SPEED_PPS * game_framework.frame_time
        else:
            boss.y += boss.y_dir * RUN_SPEED_PPS * game_framework.frame_time
            if boss.y_dir > -4.5:
                boss.y_dir += -0.049

        if boss.jump_count > 7 and boss.jump == True:
            boss.y_dir = -1
            boss.jump = False

        boss.move_slightly_to(boss.tx, boss.ty)
        if boss.distance_less_than(boss.tx, boss.ty, boss.x, boss.y, 0.5):
            boss.state_machine.add_event(('landed', 0))


    @staticmethod
    def draw(boss):
        sx = boss.x - server.stage.window_left
        sy = boss.y - server.stage.window_bottom
        if math.cos(boss.dir) < 0:
            boss.image.clip_composite_draw(
                int(boss.frame) * 842, boss.action * 624, 842, 624,
                0, 'h',
                sx, sy, 842, 624
            )
        else:
            boss.image.clip_draw(int(boss.frame) * 842, boss.action * 624, 842, 624, sx, sy)

        if math.cos(boss.dir) < 0:
            draw_rectangle(sx - 120, sy - 300, sx + 120, sy - 30)
        else:
            draw_rectangle(sx - 120, sy - 300, sx + 120, sy - 30)

        boss.font.draw(sx - 10, sy + 50, f'{boss.hp:02d}', (255, 255, 0))

    @staticmethod
    def get_bb(boss):
        if math.cos(boss.dir) < 0:
            return boss.x - 120, boss.y - 300, boss.x + 120, boss.y - 60
        else:
            return boss.x - 120, boss.y - 300, boss.x + 120, boss.y - 60

class Land:
    @staticmethod
    def enter(boss, e):
        boss.action = 0  # 낙하 동작의 인덱스를 8로 설정
        boss.frame = 0

    @staticmethod
    def exit(boss, e):
        pass

    @staticmethod
    def do(boss):
        boss.frame = (boss.frame + FRAMES_PER_ACTION_IDLE * ACTION_PER_TIME * game_framework.frame_time)
        if boss.frame > 3:
            boss.state_machine.add_event(('END_MOTION', 0))

    @staticmethod
    def draw(boss):
        sx = boss.x - server.stage.window_left
        sy = boss.y - server.stage.window_bottom
        if math.cos(boss.dir) < 0:
            boss.image.clip_composite_draw(
                int(boss.frame) * 842, boss.action * 624, 842, 624,
                0, 'h',
                sx - 20, sy, 842, 624
            )
        else:
            boss.image.clip_draw(int(boss.frame) * 842, boss.action * 624, 842, 624, sx + 20, sy)

        if math.cos(boss.dir) < 0:
            draw_rectangle(sx - 85- 20, sy - 300, sx + 190 - 20, sy - 30)
        else:
            draw_rectangle(sx - 190 + 20, sy - 300, sx + 85+ 20, sy - 30)

        boss.font.draw(sx - 10, sy + 50, f'{boss.hp:02d}', (255, 255, 0))

    @staticmethod
    def get_bb(boss):
        if math.cos(boss.dir) < 0:
            return boss.x - 85- 20, boss.y - 300, boss.x + 190- 20, boss.y - 30
        else:
            return boss.x - 190+ 20, boss.y - 300, boss.x + 85+ 20, boss.y - 30

class AttackReady:
    @staticmethod
    def enter(boss, e):
        boss.action = 4  # 낙하 동작의 인덱스를 8로 설정
        boss.frame = 0
        boss.ready = 0

    @staticmethod
    def exit(boss, e):
        pass

    @staticmethod
    def do(boss):
        if boss.ready >= 3:
            boss.state_machine.add_event(('END_MOTION', 0))
        boss.frame = (boss.frame + FRAMES_PER_ACTION_ATTACK * ACTION_PER_TIME * game_framework.frame_time)
        if boss.frame > 6:
            boss.ready += 1
            boss.frame = 0


    @staticmethod
    def draw(boss):
        sx = boss.x - server.stage.window_left
        sy = boss.y - server.stage.window_bottom
        if math.cos(boss.dir) < 0:
            boss.image.clip_composite_draw(
                int(boss.frame) * 842, boss.action * 624, 842, 624,
                0, 'h',
                sx, sy, 842, 624
            )
        else:
            boss.image.clip_draw(int(boss.frame) * 842, boss.action * 624, 842, 624, sx, sy)

        if math.cos(boss.dir) < 0:
            draw_rectangle(sx - 110, sy - 300, sx + 150, sy - 30)
        else:
            draw_rectangle(sx - 150, sy - 300, sx + 110, sy - 30)

        boss.font.draw(sx - 10, sy + 50, f'{boss.hp:02d}', (255, 255, 0))

    @staticmethod
    def get_bb(boss):
        if math.cos(boss.dir) < 0:
            return boss.x - 85, boss.y - 300, boss.x + 190, boss.y - 30
        else:
            return boss.x - 190, boss.y - 300, boss.x + 85, boss.y - 30

class Attack:
    @staticmethod
    def enter(boss, e):
        boss.action = 5  # 낙하 동작의 인덱스를 8로 설정
        boss.frame = 0

    @staticmethod
    def exit(boss, e):
        boss.boss_attack()
        pass

    @staticmethod
    def do(boss):
        boss.frame = (boss.frame + FRAMES_PER_ACTION_ATTACK * ACTION_PER_TIME * game_framework.frame_time)
        if boss.frame > 3:
            boss.state_machine.add_event(('END_MOTION', 0))

    @staticmethod
    def draw(boss):
        sx = boss.x - server.stage.window_left
        sy = boss.y - server.stage.window_bottom
        if math.cos(boss.dir) < 0:
            boss.image.clip_composite_draw(
                int(boss.frame) * 842, boss.action * 624, 842, 624,
                0, 'h',
                sx, sy, 842, 624
            )
        else:
            boss.image.clip_draw(int(boss.frame) * 842, boss.action * 624, 842, 624, sx, sy)

        if math.cos(boss.dir) < 0:
            draw_rectangle(sx, sy - 300, sx + 260, sy - 30)
        else:
            draw_rectangle(sx - 260, sy - 300, sx, sy - 30)

        boss.font.draw(sx - 10, sy + 50, f'{boss.hp:02d}', (255, 255, 0))

    @staticmethod
    def get_bb(boss):
        if math.cos(boss.dir) < 0:
            return boss.x, boss.y - 300, boss.x + 260, boss.y - 30
        else:
            return boss.x - 260, boss.y - 300, boss.x, boss.y - 30

class AttackEnd:
    @staticmethod
    def enter(boss, e):
        boss.action = 6  # 낙하 동작의 인덱스를 8로 설정
        boss.frame = 0

    @staticmethod
    def exit(boss, e):
        pass

    @staticmethod
    def do(boss):
        boss.frame = (boss.frame + FRAMES_PER_ACTION_ATTACK * ACTION_PER_TIME * game_framework.frame_time)
        if boss.frame > 5:
            boss.state_machine.add_event(('END_MOTION', 0))

    @staticmethod
    def draw(boss):
        sx = boss.x - server.stage.window_left
        sy = boss.y - server.stage.window_bottom
        if math.cos(boss.dir) < 0:
            boss.image.clip_composite_draw(
                int(boss.frame) * 842, boss.action * 624, 842, 624,
                0, 'h',
                sx, sy, 842, 624
            )
        else:
            boss.image.clip_draw(int(boss.frame) * 842, boss.action * 624, 842, 624, sx, sy)

        if math.cos(boss.dir) < 0:
            draw_rectangle(sx - 85, sy - 300, sx + 190, sy - 30)
        else:
            draw_rectangle(sx - 190, sy - 300, sx + 85, sy - 30)

        boss.font.draw(sx - 10, sy + 50, f'{boss.hp:02d}', (255, 255, 0))

    @staticmethod
    def get_bb(boss):
        if math.cos(boss.dir) < 0:
            return boss.x - 85, boss.y - 300, boss.x + 190, boss.y - 30
        else:
            return boss.x - 190, boss.y - 300, boss.x + 85, boss.y - 30

class Boss:
    image = None
    def __init__(self, x = 1500, y= 400):
        self.x, self.y = x, y
        self.action = 0
        self.frame = 0
        self.dir = math.atan2(0 , 1)
        self.hp = 20
        self.y_dir = -1
        self.on_ground = False
        self.ready = 0
        self.jump_count = 0
        self.jump = False
        self.hit_eff = HitEff()
        self.attack_eff = BossAttackEff()
        self.attack_eff_back = BossAttackEff()
        self.invincibility_time = 0
        self.jump_time = 1
        self.attack_time = 1
        self.font = load_font('./resource/ENCR10B.TTF', 16)
        self.die = False
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle : {jump_time_out : MoveReady,attack_time_out : AttackReady},
                MoveReady : {end_motion: Move},
                Move : {landed: Land , end_motion:Idle},
                Land : {end_motion:Idle},
                AttackReady : {end_motion: Attack},
                Attack: {end_motion: AttackEnd},
                AttackEnd:{end_motion: Idle}
            }
        )
        if Boss.image == None:
            Boss.image = load_image('./resource/boss.png')


    def update(self):
        self.state_machine.update()


    def handle_event(self, event):
        pass

    def draw(self):
        self.state_machine.draw()

    def get_bb(self):
        return self.state_machine.get_bb()

    def handle_collision(self, group, other):
        if group == 'slash:boss':
            if get_time() - self.invincibility_time > 0.6:
                self.invincibility_time = get_time()
                self.hp -= 1
                self.hit_eff = HitEff(self.x, self.y - 200, self.dir)
                game_world.add_object(self.hit_eff, 2)
                if self.hp < 1:
                    self.die = True
                    self.frame = 0

        elif group == 'boss:tile':
            left, bottom, right, top = self.get_bb()
            other_left, other_bottom, other_right, other_top = other.get_bb()
            dx_left = other_right - left
            dx_right = right - other_left
            dy_bottom = top - other_bottom
            dy_top = other_top - bottom
            if dx_left > 0 and dx_right > 0 and dy_bottom > 0 and dy_top > 0:
                min_dx = min(dx_left, dx_right)
                min_dy = min(dy_bottom, dy_top)
                if min_dx < min_dy:  # 좌우 충돌
                    if dx_left < dx_right:  # 왼쪽 충돌
                        self.x = other_right + ((right - left) *  7 / 11)
                    else:  # 오른쪽 충돌
                        self.x = other_left - ((right - left) * 4 / 11)
                else:
                    if not dy_bottom < dy_top:  # 아래에서 위로 충돌
                        if not self.jump:
                            self.state_machine.add_event(('LANDED', 0))
                            self.y = other_top + 300  # 타일 위로 위치 보정
                            self.on_ground = True
                            self.y_dir = 0
        pass

    def boss_attack(self):
        self.attack_eff = BossAttackEff()
        x_offset = -140 if math.cos(self.dir) < 0 else 140
        self.attack_eff.x = self.x + x_offset
        self.attack_eff.y = self.y - 110
        self.attack_eff.dir = self.dir

        self.attack_eff_back = BossAttackEffBack()
        x_offset = -120 if math.cos(self.dir) < 0 else 120
        self.attack_eff_back.x = self.x + x_offset
        self.attack_eff_back.y = self.y - 110
        self.attack_eff_back.dir = self.dir

        game_world.add_object(self.attack_eff, 2)
        game_world.add_object( self.attack_eff_back, 2)
        game_world.add_collision_pair('knight:attack', None,  self.attack_eff)
        game_world.add_collision_pair('knight:attack', None, self.attack_eff_back)

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2

    def move_slightly_to(self, tx, ty, r=0.5):
        distance = RUN_SPEED_PPS * game_framework.frame_time
        self.x += distance * math.cos(self.dir)
        pass


