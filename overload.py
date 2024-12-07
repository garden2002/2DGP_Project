import game_framework
import game_world
import server
from pico2d import *

from behavior_tree import BehaviorTree, Action, Sequence, Selector, Condition
from hiteff import HitEff

PIXEL_PER_METER = (10.0 / 0.2)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION

FRAMES_PER_ACTION_RUN = 4
FRAMES_PER_ACTION_DIE = 6



class Overload:
    image = None
    damage_sound = None
    def __init__(self, x = 300, y= 400, type = 0 ):
        self.x, self.y = x, y
        self.action = 0
        self.frame = 0
        self.back_x = 0
        self.back_y = 0
        self.attack_dir = 0
        self.dir = -1
        self.hp = 4
        self.type = type
        self.hit_eff = HitEff()
        self.invincibility_time = 0
        self.die = False
        self.build_behavior_tree()
        if Overload.image is None:
            Overload.image = load_image('./resource/overload.png')
        if Overload.damage_sound is None:
            Overload.damage_sound = load_wav('./resource/enemy_damage.wav')
            Overload.damage_sound.set_volume(32)
        if self.type == 0:
            self.patrol_locations = [(self.x, self.y), (self.x + 400, self.y + 400)]
        else:
            self.patrol_locations = [(self.x, self.y), (self.x + 400, self.y - 400)]
        self.loc_no = 0

    def update(self):
        if self.action == 1:
            self.frame = (self.frame + FRAMES_PER_ACTION_RUN * ACTION_PER_TIME * game_framework.frame_time) % 4
        else:
            self.frame = (self.frame + FRAMES_PER_ACTION_DIE * ACTION_PER_TIME * game_framework.frame_time)

        if self.back_y > 0:
            self.y += RUN_SPEED_PPS * game_framework.frame_time
            self.back_y -= 1

        if self.back_x > 0:
            if self.attack_dir == -1:
                self.x += -3 * RUN_SPEED_PPS * game_framework.frame_time
            else:
                self.x += 3 * RUN_SPEED_PPS * game_framework.frame_time
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

    def get_bb(self):
        if math.cos(self.dir) > 0:
            return self.x - 20, self.y - 60, self.x + 60, self.y + 30
        else:
            return self.x - 60, self.y - 60, self.x + 20, self.y + 30

    def handle_collision(self, group, other):
        if group == 'slash:overload':
            if get_time() - self.invincibility_time > 0.6:
                 self.invincibility_time = get_time()
                 self.hp -= 1
                 self.back_x = 100
                 self.back_y = 70
                 self.attack_dir = other.face_dir
                 self.hit_eff = HitEff(self.x, self.y, self.dir)
                 game_world.add_object(self.hit_eff, 2)
                 self.damage_sound.play()
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

    def move_to(self, r=0.5):
        self.action = 1
        self.move_slightly_to(self.tx , self.ty)
        if self.distance_less_than(self.tx , self.ty , self.x , self.y ,r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def get_patrol_location(self):
        self.tx, self.ty = self.patrol_locations[self.loc_no]
        self.loc_no = (self.loc_no + 1) % len(self.patrol_locations)
        return BehaviorTree.SUCCESS

    def is_die(self):
        if self.die:
            self.action = 0
            return BehaviorTree.SUCCESS
        else:
            return  BehaviorTree.FAIL


    def die_overload(self):
        if self.frame > 6:
            game_world.remove_object(self)

    def build_behavior_tree(self):

        a1 = Action('순찰 위치 가져오기', self.get_patrol_location)
        a2 = Action('순찰', self.move_to)
        patrol = Sequence('순찰', a1, a2)

        c2 = Condition('죽었는가?',self.is_die)
        a3 = Action('죽음', self.die_overload)

        die_object = Sequence('죽음', c2 , a3)

        root =  Selector('죽음 또는 배호;',die_object,patrol)
        self.bt = BehaviorTree(root)
        pass


