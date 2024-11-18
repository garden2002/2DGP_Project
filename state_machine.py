# event (종류 문자열 , 실제 값)
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_z, SDLK_x, SDLK_UP, SDLK_s


def start_event(e):
    return e[0] == 'START'

def time_out(e):
    return e[0] == 'TIME_OUT'

def end_motion(e):
    return e[0] == 'END_MOTION'

def landed(e):
    return e[0] == 'Landed'

def die(e):
    return e[0] == 'Die'

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT

def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT

def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT

def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

def up_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_UP

def up_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_UP

def z_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_z

def x_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_x

def s_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_s


# 상태 머신을 처리 관리해주는 클래스
class StateMachine:
    def __init__(self, o):
        self.o = o #boy self가 전달, self.o 상테 머신과 연결된 캐릭터 객체
        self.event_que = []
        pass

    def update(self):
        self.cur_state.do(self.o)
        #이벤트 발생했는지 확인하고, 거기에 따라서 상태변화
        if self.event_que: # list에 요소가 있으면, list 값은 True
            e = self.event_que.pop(0) #list에 첫번쨰 요소를 꺼냄
            for check_event , next_state in self.transitions[self.cur_state].items():
                if check_event(e):
                    self.cur_state.exit(self.o , e)
                    print(f'EXIT from {self.cur_state}')
                    self.cur_state = next_state
                    self.cur_state.enter(self.o , e)
                    print(f'ENTER into {self.cur_state}')
                    return
        pass

    def start(self, start_state):
        #현재 상태를 시작 상태로 만듬
        self.cur_state = start_state #Idle
        self.cur_state.enter(self.o ,('START' , 0))
        print(f'ENTER into {self.cur_state}')
        pass

    def draw(self):
        self.cur_state.draw(self.o)
        pass

    def set_transitions(self, transitions):
        self.transitions = transitions
        pass

    def add_event(self, e):
        self.event_que.append(e) # 상태머신용 이벤트 추가
        #print(f'    DEBUG: new event {e} is added.')
        pass

    def get_bb(self):
        return self.cur_state.get_bb(self.o)
        pass