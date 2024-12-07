import game_framework
import game_world

from pico2d import *
import server
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
from hiteff import HitEff

PIXEL_PER_METER = (10.0 / 0.2)  # 10 pixel 30 cm
WALK_SPEED_KMPH = 10.0
WALK_SPEED_MPM = (WALK_SPEED_KMPH * 1000.0 / 60.0)
WALK_SPEED_MPS = (WALK_SPEED_MPM / 60.0)
WALK_SPEED_PPS = (WALK_SPEED_MPS * PIXEL_PER_METER)

RUN_SPEED_KMPH = 17.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION_WALK = 7
FRAMES_PER_ACTION_RUN = 8
FRAMES_PER_ACTION_DIE = 8


class Walk_object:
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
        self.hit_eff = HitEff()
        self.invincibility_time = 0
        self.font = load_font('./resource/ENCR10B.TTF', 16)
        self.die = False
        self.build_behavior_tree()
        if Walk_object.image == None:
            Walk_object.image = load_image('./resource/walk.png')

        self.patrol_locations = [(self.x - 200 ,self.y), (self.x + 200,self.y)]
        self.loc_no = 0

    def update(self):
        if self.action == 0:
            self.frame = (self.frame + FRAMES_PER_ACTION_WALK * ACTION_PER_TIME * game_framework.frame_time) % 7
        elif self.action == 2:
            self.frame = (self.frame + FRAMES_PER_ACTION_RUN * ACTION_PER_TIME * game_framework.frame_time) % 4
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
            x , _ = self.patrol_locations[i]
            self.patrol_locations[i] = (x, self.y)


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
            draw_rectangle(sx - 40, sy - 70, sx + 70, sy + 70)
        else:
            draw_rectangle(sx - 70, sy - 70, sx + 40, sy + 70)

        self.font.draw(sx - 10, sy + 50, f'{self.hp:02d}', (255, 255, 0))

    def get_bb(self):
        if math.cos(self.dir) > 0:
            return self.x - 40, self.y - 70, self.x + 70, self.y + 70
        else:
            return self.x - 70, self.y - 70, self.x + 40, self.y + 70

    def handle_collision(self, group, other):
        if group == 'slash:walk':
            if get_time() - self.invincibility_time > 0.6:
                self.invincibility_time = get_time()
                self.hp -= 1
                self.back_x = 80
                self.hit_eff = HitEff(self.x, self.y, self.dir)
                game_world.add_object(self.hit_eff, 2)
                if self.hp < 1:
                    self.die = True
                    self.frame = 0

        elif group == 'walk:tile':
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
                        self.y = other_top + 70  # 타일 위로 위치 보정
                        self.on_ground = True
                        self.y_dir = 0
        pass

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2

    def move_slightly_to(self, tx, ty):
        self.tx, self.ty = self.patrol_locations[self.loc_no][0], self.y
        self.dir = math.atan2(ty - self.y, tx - self.x)
        if self.action == 0:
            distance = WALK_SPEED_PPS * game_framework.frame_time
        else:
            distance = RUN_SPEED_PPS * game_framework.frame_time
        if self.back_x <= 0:
            self.x += distance * math.cos(self.dir)
        pass

    def move_to(self, r=0.5):
        self.action = 0
        self.move_slightly_to(self.tx, self.ty)
        if self.distance_less_than(self.tx, self.ty, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def get_patrol_location(self):
        self.tx, self.ty = self.patrol_locations[self.loc_no][0], self.y
        self.loc_no = (self.loc_no + 1) % len(self.patrol_locations)
        return BehaviorTree.SUCCESS


    def is_knight_nearby(self, distance):
        if self.distance_less_than(server.knight.x, server.knight.y, self.x, self.y, distance):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
        pass

    def move_to_knight(self, r=0.5):
        self.action = 2
        self.move_slightly_to(server.knight.x, self.y)
        if self.distance_less_than(server.knight.x, server.knight.y, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING
        pass

    def is_die(self):
        if self.die:
            self.action = 1
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def die_walk(self):
        if self.frame > 8:
            game_world.remove_object(self)

    def build_behavior_tree(self):

        a1 = Action('순찰 위치 가져오기', self.get_patrol_location)
        a2 = Action('순찰', self.move_to)
        patrol = Sequence('순찰', a1, a2)

        c1 = Condition('기사가 근처에 있는가?', self.is_knight_nearby, 10)
        a3 = Action('기사에게 접근', self.move_to_knight)
        chase_knight = Sequence('소년을 추적', c1, a3)

        c2 = Condition('죽었는가?', self.is_die)
        a4 = Action('죽음', self.die_walk)

        die_object = Sequence('죽음', c2, a4)

        root = chase_or_patrol = Selector('추적 또는 배회', die_object, chase_knight, patrol)
        self.bt = BehaviorTree(root)
        pass


