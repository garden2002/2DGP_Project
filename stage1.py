import game_world
import server

from pico2d import *

from goal import Goal
from tile import Tile

t1 = [Tile(1920, 35, 1920, 35) , Tile(350, 200, 80, 15), Tile(615, 300, 80, 15)
     , Tile(970, 400, 170, 15), Tile(1140, 200, 110, 130), Tile(1210, 370, 40, 40)
     , Tile(1790, 110, 60, 40),Tile(2000, 240, 100, 15), Tile(2215, 220, 55, 150)
     , Tile(3040, 190, 85, 15), Tile(3330, 340, 85, 15), Tile(3025, 540, 85, 15)
     , Tile(2710, 670, 85, 15), Tile(1360, 730, 1145, 35),Tile(1810, 810, 60, 45)
    ,Tile(1520, 925, 85, 15),Tile(1180, 895, 110, 130),Tile(1250, 1065, 40, 40)
    ,Tile(1110, 1105, 85, 15),Tile(945, 1435, 75, 335),Tile(1440, 1280, 85, 15)
     ,Tile(1860, 1265, 150, 35),Tile(2235, 1330, 215, 35),Tile(2595, 1400, 150, 35)
    ,Tile(2815, 1465, 70, 35),Tile(3040, 1545, 85, 15),Tile(3240, 1620, 85, 15)
    ,Tile(3640, 1280, 250, 420)]



class Stage1:
    def __init__(self):
        self.image = load_image('./resource/stage1.png')
        self.cw = get_canvas_width()
        self.ch = get_canvas_height()
        self.w = self.image.w
        self.h = self.image.h
        self.tiles = []
        self.goal = Goal(3760, 1810, 80, 110 , 1)
        self.load_tiles()
        self.window_left = clamp(0, int(server.knight.x) - self.cw // 2, self.w - self.cw - 1)
        self.window_bottom = clamp(0, int(server.knight.y) - self.ch // 2, self.h - self.ch - 1)
        self.bgm = load_music('./resource/stage1.mp3')
        self.bgm.set_volume(32)
        self.bgm.repeat_play()

    def load_tiles(self):
        for tile in t1:
            self.tiles.append(tile)
            game_world.add_collision_pair('knight:tile', None, tile)
            game_world.add_collision_pair('walk:tile', None, tile)
            game_world.add_collision_pair('roll:tile', None, tile)
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