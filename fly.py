import random
import math
import game_framework
import game_world
import server
from pico2d import *
from behavior_tree import BehaviorTree, Action, Sequence, Selector, Condition
from hit_eff import Hit_eff

PIXEL_PER_METER = (10.0 / 0.2)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 15.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION

FRAMES_PER_ACTION_IDLE = 5
FRAMES_PER_ACTION_RUN = 4
FRAMES_PER_ACTION_DIE = 3



class Flying_object:
    image = None

    def __init__(self, x = 300, y= 400 ):
        self.x, self.y = x, y
        self.action = 0
        self.frame = 0
        self.back_x = 0
        self.back_y = 0
        self.dir = -1
        self.hp = 4
        self.hit_eff = Hit_eff()
        self.invincibility_time = 0
        self.font = load_font('./resource/ENCR10B.TTF', 16)
        self.die = False
        self.build_behavior_tree()
        if Flying_object.image == None:
            Flying_object.image = load_image('./resource/fly.png')

    def update(self):
        if self.action == 0:
            self.frame = (self.frame + FRAMES_PER_ACTION_IDLE * ACTION_PER_TIME * game_framework.frame_time) % 5
        elif self.action == 2:
            self.frame = (self.frame + FRAMES_PER_ACTION_RUN * ACTION_PER_TIME * game_framework.frame_time) % 4
        else:
            self.frame = (self.frame + FRAMES_PER_ACTION_DIE * ACTION_PER_TIME * game_framework.frame_time)

        if self.back_y > 0:
            self.y += RUN_SPEED_PPS * game_framework.frame_time
            self.back_y -= 1

        if self.back_x > 0:
            if math.cos(self.dir) > 0:
                self.x += -2 * RUN_SPEED_PPS * game_framework.frame_time
            else:
                self.x += 2 * RUN_SPEED_PPS * game_framework.frame_time
            self.back_x -= 1

        self.bt.run()

    def handle_event(self, event):
        pass

    def draw(self):
        sx = self.x - server.stage.window_left
        sy = self.y - server.stage.window_bottom
        if math.cos(self.dir) > 0:
            self.image.clip_composite_draw(
                int(self.frame) * 140, self.action * 140, 140, 140,
                0, 'h',
                sx, sy, 140, 140
            )
        else:
            self.image.clip_draw(int(self.frame) * 140, self.action * 140, 140, 140, sx, sy)
        if math.cos(self.dir) > 0:
            draw_rectangle(sx - 40, sy - 65, sx + 70, sy + 65)
        else:
            draw_rectangle(sx - 70, sy - 65, sx + 40, sy + 65)
        self.font.draw(sx - 10, sy + 50, f'{self.hp:02d}', (255, 255, 0))

    def get_bb(self):
        if math.cos(self.dir) > 0:
            return self.x - 40, self.y - 65, self.x + 70, self.y + 65
        else:
            return self.x - 70, self.y - 65, self.x + 40, self.y + 65

    def handle_collision(self, group, other):
        if group == 'slash:fly':
            if get_time() - self.invincibility_time > 0.6:
                self.invincibility_time = get_time()
                self.hp -= 1
                self.back_x = 100
                self.back_y = 70
                self.hit_eff = Hit_eff(self.x, self.y, self.dir)
                game_world.add_object(self.hit_eff, 2)
                if self.hp < 1:
                    self.die = True
                    self.frame = 0
            pass

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2

    def move_slightly_to(self, tx, ty):
        self.dir = math.atan2(ty -self.y ,tx - self.x)
        distance = RUN_SPEED_PPS * game_framework.frame_time
        if self.back_y <= 0:
            self.y += distance * math.sin(self.dir)
        if self.back_x <= 0:
            self.x += distance * math.cos(self.dir)

        pass

    def set_idle(self):
        self.action = 0

    def move_to(self, r=0.5):
        self.action = 2
        self.move_slightly_to(self.tx , self.ty)
        if self.distance_less_than(self.tx , self.ty , self.x , self.y ,r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING


    def is_knight_nearby(self, distance):
        if self.distance_less_than(server.knight.x , server.knight.y, self.x , self.y ,distance):
            return BehaviorTree.SUCCESS
        else:
            return  BehaviorTree.FAIL
        pass

    def move_to_knight(self, r=0.5):
        self.action = 2
        self.move_slightly_to(server.knight.x ,server.knight.y)
        if self.distance_less_than(server.knight.x , server.knight.y , self.x  , self.y , r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING
        pass

    def is_die(self):
        if self.die:
            self.action = 1
            return BehaviorTree.SUCCESS
        else:
            return  BehaviorTree.FAIL


    def die_fly(self):
        if self.frame > 3:
            game_world.remove_object(self)

    def build_behavior_tree(self):

        a1 = Action('Set Idle location', self.set_idle)
        idle = Sequence('Wander', a1)

        c1 = Condition('기사가 근처에 있는가?',self.is_knight_nearby,11)
        a2 = Action('기사에게 접근' , self.move_to_knight)
        chase_knight = Sequence('소년을 추적', c1, a2)

        c2 = Condition('죽었는가?',self.is_die)
        a3 = Action('죽음', self.die_fly)

        die_object = Sequence('죽음', c2 , a3)

        root = chase_or_idle = Selector('추적 또는 배회',die_object,chase_knight,idle)
        self.bt = BehaviorTree(root)
        pass


