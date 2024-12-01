import pico2d
from pico2d import draw_rectangle

import game_world
from Tile import Tile

# 상수 정의
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600



class TileMap:
    def __init__(self, map_data, tile_size=250):
        self.tile_size = tile_size
        self.tiles = []
        self.load_map(map_data)

    def load_map(self, map_data):
        # 타일 번호에 따라 이미지 경로를 정의
        tile_images = {
            1: 'floor1.png',
            2: 'floor2.png'
        }

        # map_data를 읽어 타일 객체 생성
        for row_idx, row in enumerate(map_data):
            for col_idx, tile_type in enumerate(row):
                if tile_type in tile_images:
                    if tile_type == 0:
                        continue
                    x = col_idx * self.tile_size + self.tile_size // 2
                    y = (len(map_data) - row_idx - 1) * self.tile_size + self.tile_size // 2 - 80
                    tile = Tile(tile_images[tile_type], x, y, self.tile_size)
                    self.tiles.append(tile)
                    game_world.add_collision_pair('knight:map', None, tile)

    def update(self):
        pass

    def draw(self):
        for tile in self.tiles:
            tile.draw()
            draw_rectangle(*tile.get_bb())

    def get_tile_below(self , knight):
        for tile in self.tiles:  # 타일 리스트를 순회
            if tile.get_left() < knight.x < tile.get_right():  # 캐릭터가 타일 위에 있는 경우
                if tile.get_top() < knight.y <= tile.get_top() + 10:  # 타일 위 10픽셀 이내
                    return tile
        return None
