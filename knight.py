from pico2d import get_time, load_image

from state_machine import right_down, left_up, left_down, right_up, start_event, StateMachine


class Idle:
    @staticmethod
    def enter(knight , e):
        if right_down(e) or left_up(e):
            knight.face_dir = -1
            pass
        elif left_down(e) or right_up(e) or start_event(e):
            knight.face_dir = 1
            pass
        knight.action = 1
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
        knight.frame = (knight.frame + 1) % 9
        pass
    @staticmethod
    def draw(knight):
        if knight.face_dir == 1:
            knight.image.clip_composite_draw(
                knight.frame * 128, knight.action * 128, 128, 128,
                0,'h',
                knight.x, knight.y,128,128
            )
        else:
            knight.image.clip_draw(knight.frame * 128, knight.action * 128, 128, 128, knight.x, knight.y)
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
        knight.action = 0
        knight.frame = 0
        #시작 시간을 기록
        knight.start_time = get_time()
        pass
    @staticmethod
    def exit(knight , e):
        pass
    @staticmethod
    def do(knight):
        knight.frame = (knight.frame + 1)
        if knight.frame > 12:
            knight.frame = 5
        knight.x += knight.dir * 10
        pass
    @staticmethod
    def draw(knight):
        if knight.face_dir == 1:
            knight.image.clip_composite_draw(
                knight.frame * 128, knight.action * 128, 128, 128,
                0, 'h',
                knight.x, knight.y, 128, 128
            )
        else:
            knight.image.clip_draw(knight.frame * 128, knight.action * 128, 128, 128, knight.x, knight.y)
        pass


class Knight:
    image = None
    def __init__(self):
        self.x, self.y = 100 , 300
        self.frame = 0
        self.dir = 0
        self.action = 0
        self.state_machine = StateMachine(self)  # 소년 객체를 위한 상태 머신인지 알려줄 필요
        self.state_machine.start(Idle)  # 객체를 생성한게 아닌, 직접 Idle 이라는 클래스를 사용
        self.state_machine.set_transitions(
            {
                Idle:{right_down: Run, left_down: Run, left_up: Run, right_up: Run},
                Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle}
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
