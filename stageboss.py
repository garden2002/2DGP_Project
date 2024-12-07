import game_world
import server
from pico2d import *
from goal import Goal
from tile import Tile

t1 = [Tile(1920, 15, 1920, 15)]


class StageBoss:
    def __init__(self):
        self.image = load_image('./resource/stage_boss.png')
        self.cw = get_canvas_width()
        self.ch = get_canvas_height()
        self.w = self.image.w
        self.h = self.image.h
        self.tiles = []
        self.goal = Goal(1950, 200, 80, 170 , 3)
        self.load_tiles()
        self.window_left = clamp(0, int(server.knight.x) - self.cw // 2, self.w - self.cw - 1)
        self.window_bottom = clamp(0, int(server.knight.y) - self.ch // 2, self.h - self.ch - 1)
        self.bgm = load_music('./resource/stage_boss.mp3')
        self.bgm.set_volume(8)
        self.bgm.repeat_play()

    def load_tiles(self):
        for tile in t1:
            self.tiles.append(tile)
            game_world.add_collision_pair('knight:tile', None, tile)
            game_world.add_collision_pair('boss:tile', None, tile)
        game_world.add_collision_pair('knight:goal', None, self.goal)
        pass

    def draw(self):
        self.image.clip_draw_to_origin(self.window_left, self.window_bottom, self.cw, self.ch, 0, 0)

    def update(self):
        self.window_left = clamp(0, int(server.knight.x) - self.cw // 2, self.w - self.cw - 1)
        self.window_bottom = clamp(0, int(server.knight.y) - self.ch // 2, self.h - self.ch - 1)

    def get_tile_below(self, knight):
        for tile in self.tiles:  # 타일 리스트를 순회
            left, bottom, right, top = tile.get_bb()
            if left < knight.x - 30 < right or left < knight.x + 30 < right:  # 캐릭터가 타일 위에 있는 경우
                if top <= knight.y - 65 <= top + 10:  # 타일 위 10픽셀 이내
                    return tile
        return None

    def handle_event(self, event):
        pass