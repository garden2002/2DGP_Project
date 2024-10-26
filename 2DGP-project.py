from pico2d import *



class Knight:
    image = None
    def __init__(self):
        self.x, self.y = 100 , 300
        self.frame = 0
        self.dir = 0
        self.action = 7
        if Knight.image == None:
            Knight.image = load_image('knight.png')

    def update(self):
        self.frame = (self.frame + 1) % 7
        self.x += self.dir * 5

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                self.dir += 1
                self.action = 15
            elif event.key == SDLK_LEFT:
                self.dir -= 1
                self.action = 15
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                self.dir -= 1
                self.action = 7
            elif event.key == SDLK_LEFT:
                self.dir += 1
                self.action = 7

    def draw(self):
        self.image.clip_draw(self.frame * 128, self.action * 128, 128, 128, self.x, self.y)

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