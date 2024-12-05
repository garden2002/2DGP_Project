from pico2d import *

class Hp2:
    image = None

    def __init__(self):
        if Hp2.image is None:
            Hp2.image = load_image('./resource/Hp2.png')
        self.x = 140
        self.y = 620

    def draw(self):
        self.image.clip_composite_draw(
            0, 0, 240, 240, 0, 'h', self.x, self.y, 240, 240)

    def update(self):
        pass

    def get_bb(self):
        pass

    def handle_collision(self, group, other):
        pass