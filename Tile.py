from pico2d import *

class Tile:
    def __init__(self, image_path, x, y, size=270):
        self.image = load_image(image_path)
        self.x = x
        self.y = y
        self.size = size

    def draw(self):
        self.image.draw(self.x, self.y)

    def get_bb(self):
        return self.x - 135, self.y - 57, self.x + 135, self.y + 40
        pass

    def handle_collision(self, group, other):
        pass