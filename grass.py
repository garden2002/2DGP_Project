from pico2d import *

class Grass:
    def __init__(self, x = 400 , y = 30):
        self.image = load_image('grass.png')
        self.x = x
        self.y = y

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y)
        self.image.draw(self.x + 800, self.y)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 400, self.y - 30, self.x + 1000, self.y + 30
        pass

    def handle_collision(self, group, other):
        pass

