import game_world
import server

from pico2d import *

from tile import Tile

t2 = [Tile(1920, 90, 1920, 90) , Tile(2400, 360, 130, 15), Tile(2940, 520, 180, 15)
     , Tile(3510, 680, 230, 15), Tile(2300, 695, 170, 20), Tile(2600, 990, 130, 15)
     , Tile(940, 740, 1000, 90),Tile(590, 1000, 130, 15), Tile(1020, 1140, 130, 20)
     , Tile(190, 1180, 130, 20), Tile(520, 1300, 130, 20), Tile(1470, 1365, 170, 20)
     , Tile(930, 1460, 130, 15), Tile(2150, 1440, 400, 100), Tile(940, 740, 1000, 90)
     ,Tile(2730, 1660, 130, 15),Tile(2400, 1830, 130, 15),Tile(3270, 1780, 330, 80)
    ,Tile(2710, 2105, 40, 90),Tile(2950, 2125, 200, 60),Tile(3620, 2125, 225, 60)]

class Stage2:
    def __init__(self):
        self.image = load_image('./resource/stage2.png')
        self.cw = get_canvas_width()
        self.ch = get_canvas_height()
        self.w = self.image.w
        self.h = self.image.h
        self.tiles = []
        self.load_tiles()
        self.window_left = clamp(0, int(server.knight.x) - self.cw // 2, self.w - self.cw - 1)
        self.window_bottom = clamp(0, int(server.knight.y) - self.ch // 2, self.h - self.ch - 1)

    def load_tiles(self):
        for tile in t2:
            self.tiles.append(tile)
            game_world.add_collision_pair('knight:tile', None, tile)
            game_world.add_collision_pair('walk:tile', None, tile)
            game_world.add_collision_pair('roll:tile', None, tile)
        pass
    def draw(self):
        self.image.clip_draw_to_origin(self.window_left, self.window_bottom, self.cw, self.ch, 0, 0)
        for tile in self.tiles:
            sx = tile.x - self.window_left
            sy = tile.y - self.window_bottom
            draw_rectangle(sx - tile.x_size ,sy - tile.y_size ,sx + tile.x_size ,sy + tile.y_size)

    def update(self):
        self.window_left = clamp(0, int(server.knight.x) - self.cw // 2, self.w - self.cw - 1)
        self.window_bottom = clamp(0, int(server.knight.y) - self.ch // 2, self.h - self.ch - 1)

    def get_tile_below(self , knight):
        for tile in self.tiles:  # 타일 리스트를 순회
            left , bottom , right , top = tile.get_bb()
            if left < knight.x - 30 < right or left < knight.x + 30 < right:  # 캐릭터가 타일 위에 있는 경우
                if top <= knight.y - 65 <= top + 10:  # 타일 위 10픽셀 이내
                    return tile
        return None

    def handle_event(self, event):
        pass