from pico2d import *

from state_machine import StateMachine, right_down, left_up, right_up, start_event, left_down


class Idle:
    @staticmethod
    def enter(knight , e):
        if right_down(e) or left_up(e):
            pass
        elif left_down(e) or right_up(e) or start_event(e):
            pass
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
        knight.frame = (knight.frame + 1) % 7
        pass
    @staticmethod
    def draw(knight):
        knight.image.clip_draw(knight.frame * 128, knight.action * 128, 128, 128, knight.x, knight.y)
        pass

class Knight:
    image = None
    def __init__(self):
        self.x, self.y = 100 , 300
        self.frame = 0
        self.dir = 0
        self.action = 7
        self.state_machine = StateMachine(self)  # 소년 객체를 위한 상태 머신인지 알려줄 필요
        self.state_machine.start(Idle)  # 객체를 생성한게 아닌, 직접 Idle 이라는 클래스를 사용
        self.state_machine.set_transitions(
            {
                Idle:{}
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

def handle_events():
    global play

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            play = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            play = False
        else:
            knight.handle_event(event)


def reset_world():
    global play
    global world
    global knight

    play = True
    knight = Knight()
    world = []
    world.append(knight)


def update_world():
    for o in world:
        o.update()
    pass


def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()

open_canvas()
reset_world()
# game loop
while play:
    handle_events()
    update_world()
    render_world()
    delay(0.05)
# finalization code
close_canvas()