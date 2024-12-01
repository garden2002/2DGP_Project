from pico2d import *
import server

class Tile:
    def __init__(self, x, y,x_size ,y_size):
        self.x = x
        self.y = y
        self.x_size = x_size
        self.y_size = y_size

    def draw(self):
        pass

    def get_bb(self):
        return self.x - self.x_size, self.y - self.y_size, self.x + self.x_size, self.y + self.y_size
    def get_top(self):
        return self.y + self.y_size
    def get_left(self):
        return self.x - self.x_size
    def get_right(self):
        return self.x + self.x_size

    def handle_collision(self, group, other):
        pass
