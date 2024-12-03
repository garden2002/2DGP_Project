import game_framework
import game_world

from pico2d import *
import server
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector

PIXEL_PER_METER = (10.0 / 0.2)  # 10 pixel 30 cm

RUN_SPEED_KMPH = 30.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION_IDLE = 4
FRAMES_PER_ACTION_RUN = 6
FRAMES_PER_ACTION_DIE = 4


class Roll:
    image = None
    def __init__(self, x = 700, y= 500):
        self.x, self.y = x, y
        self.action = 0
        self.frame = 0
        self.back_x = 0
        self.back_y = 0
        self.dir = -1
        self.hp = 4
        self.y_dir = 0
        self.on_ground = False
        self.invincibility_time = 0
        self.font = load_font('./resource/ENCR10B.TTF', 16)
        self.die = False
        self.build_behavior_tree()
        if Roll.image == None:
            Roll.image = load_image('./resource/roll.png')

        self.patrol_locations = [(self.x - 200 ,self.y), (self.x + 200,self.y)]
        self.loc_no = 0

    def update(self):
        if self.action == 0:
            self.frame = (self.frame + FRAMES_PER_ACTION_IDLE * ACTION_PER_TIME * game_framework.frame_time) % 4
        elif self.action == 1:
            self.frame = (self.frame + FRAMES_PER_ACTION_RUN * ACTION_PER_TIME * game_framework.frame_time) % 3
        else:
            self.frame = (self.frame + FRAMES_PER_ACTION_DIE * ACTION_PER_TIME * game_framework.frame_time)

        if self.on_ground:  # 현재 지면에 있는 상태라면
            tile_below = server.stage.get_tile_below(self)  # 캐릭터 아래 타일 확인 (구현 필요)
            if not tile_below:  # 아래에 타일이 없으면
                self.on_ground = False  # 지면에서 떨어짐

        if not self.on_ground:
            self.y_dir = -1
        if self.back_y <= 0:
            self.y += self.y_dir * RUN_SPEED_PPS * game_framework.frame_time
        if self.y_dir > - 2.5:
            self.y_dir += -0.0098

        for i in range(len(self.patrol_locations)):
            x, y = self.patrol_locations[i]
            self.patrol_locations[i] = (x, self.y)

        if self.back_y > 0:
            self.y += 1 * RUN_SPEED_PPS * game_framework.frame_time
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
            if self.action == 1:
                draw_rectangle(sx - 20, sy - 60, sx + 60, sy + 10)
            else:
                draw_rectangle(sx - 40, sy - 60, sx + 60, sy + 10)
        else:
            if self.action == 1:
                draw_rectangle(sx - 60, sy - 60, sx + 20, sy + 10)
            else:
                draw_rectangle(sx - 60, sy - 60, sx + 40, sy + 10)

        self.font.draw(sx - 10, sy + 50, f'{self.hp:02d}', (255, 255, 0))

    def get_bb(self):
        if self.dir == 1:
            if self.action == 0:
                return self.x - 20, self.y - 60, self.x + 60, self.y + 10
            else:
                return self.x - 40, self.y - 60, self.x + 60, self.y + 10
        else:
            if self.action == 0:
                return self.x - 60, self.y - 60, self.x + 20, self.y + 10
            else:
                return self.x - 60, self.y - 60, self.x + 40, self.y + 10

    def handle_collision(self, group, other):
        if group == 'slash:roll':
            if get_time() - self.invincibility_time > 0.6:
                self.invincibility_time = get_time()
                self.hp -= 1
                self.back_x = 80
                self.back_y = 50
                if self.hp < 1:
                    self.die = True
                    self.frame = 0

        elif group == 'roll:tile':
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
                        self.x = other_right + ((right - left) *  3 / 5 )
                    else:  # 오른쪽 충돌
                        self.x = other_left - ((right - left) * 2 / 5)
                else:
                    self.y = other_top + 60  # 타일 위로 위치 보정
                    self.on_ground = True
                    self.y_dir = 0

        pass

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2

    def move_slightly_to(self, tx, ty):
        self.tx, self.ty = self.patrol_locations[self.loc_no]
        self.dir = math.atan2(ty - self.y, tx - self.x)
        distance = RUN_SPEED_PPS * game_framework.frame_time
        if self.back_x <= 0:
            self.x += distance * math.cos(self.dir)
        pass

    def move_to(self, r=0.5):
        self.move_slightly_to(self.tx, self.ty)
        if self.distance_less_than(self.tx, self.ty, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING


    def set_idle(self):
        self.action = 0


    def is_knight_nearby(self, distance):
        if self.distance_less_than(server.knight.x, server.knight.y, self.x, self.y, distance):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
        pass

    def move_to_knight(self, r=0.5):
        self.action = 1
        self.move_slightly_to(server.knight.x, server.knight.y)
        if self.distance_less_than(server.knight.x, server.knight.y, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING
        pass

    def is_die(self):
        if self.die:
            self.action = 2
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def die_roll(self):
        if self.frame > 4:
            game_world.remove_object(self)

    def build_behavior_tree(self):

        a1 = Action('Set Idle location', self.set_idle)
        idle = Sequence('Wander', a1)

        c1 = Condition('기사가 근처에 있는가?', self.is_knight_nearby, 10)
        a3 = Action('기사에게 접근', self.move_to_knight)
        chase_knight = Sequence('소년을 추적', c1, a3)

        c2 = Condition('죽었는가?', self.is_die)
        a4 = Action('죽음', self.die_roll)

        die_object = Sequence('죽음', c2, a4)

        root = chase_or_patrol = Selector('추적 또는 배회', die_object, chase_knight, idle)
        self.bt = BehaviorTree(root)
        pass


