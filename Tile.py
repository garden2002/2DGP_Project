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

    def get_top(self):
        return self.y + 40

    def handle_collision(self, group, other):
        pass

    def is_colliding(self, other):
        # 다른 객체의 충돌 박스와 비교
        other_left, other_bottom, other_right, other_top = other.get_bb()
        tile_left, tile_bottom, tile_right, tile_top = self.get_bb()

        # 충돌 여부 판단 (AABB 방식)
        return not (
            other_right < tile_left or  # 다른 객체가 타일 왼쪽으로 벗어남
            other_left > tile_right or  # 다른 객체가 타일 오른쪽으로 벗어남
            other_top < tile_bottom or  # 다른 객체가 타일 아래로 벗어남
            other_bottom > tile_top    # 다른 객체가 타일 위로 벗어남
        )