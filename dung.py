
# tiles from : https://opengameart.org/content/dungeon-crawl-32x32-tiles

# try:
# https://opengameart.org/content/lpc-tile-atlas
# https://opengameart.org/content/lpc-tile-atlas2
# https://opengameart.org/content/lots-of-free-2d-tiles-and-sprites-by-hyptosis

import time
import re
import random
import arcade
from arcade.key import ESCAPE, SPACE
from tilegamelib import TiledMap, load_tiles
from tilegamelib import MapMove
from tilegamelib import PLAYER_MOVES
from tilegamelib import Vector
from player import Player
from level import Level
from monsters import Zombie


SIZEX, SIZEY = (800, 600)
LEVEL_SWITCH_TIMER = 25

SYNONYMS = [
    ('.', 'grey_dirt_0_new'),
    ('~', 'green_water'),
    ('#', 'brick_gray_0'),
    ('player', 'deep_elf_fighter_new'),
    ('s', 'slot'),
]


class DungeonCrawl(arcade.Window):

    def __init__(self):
        super().__init__(SIZEX, SIZEY, "Dungeon Crawl")
        arcade.set_background_color(arcade.color.BLACK)
        self.tiles = load_tiles('stonesoup.csv')
        self.add_tile_synonyms()
        self.player = Player(self.tiles, None)
        self.level = None
        self.level_cache = {}
        #self.enter_level('levels/dm01.json', Vector(1, 2))
        self.enter_level('levels/lv1.json', Vector(1, 2))

    def create_zombies(self):
        zombie_horde = []
        for i in range(3):
            x = random.randint(5, 12)
            y = random.randint(2, 10)
            z = Zombie('stonesoup/monster/skeletal_warrior_new.png', Vector(x, y), self.level)
            zombie_horde.append(z)
        return zombie_horde

    def enter_level(self, filename, pos):
        if filename not in self.level_cache:
            self.level = Level(filename, self.tiles, offset=Vector(50, 50))
            self.level.add_monsters(self.create_zombies())
            self.level_cache[filename] = self.level
        else:
            self.level = self.level_cache[filename]
        self.player.level = self.level
        self.player.pos = pos
        self.timer = -1

    def add_tile_synonyms(self):
        for s, t in SYNONYMS:
            self.tiles[s] = self.tiles[t]

    def on_draw(self):
        arcade.start_render()
        self.level.draw()
        self.player.draw()

    def update(self, time_delta):
        self.level.update()
        if self.timer > 0:
            self.timer -= 1
        if self.timer == 0:
            next_lv, x, y = self.level.on_exit(self.player.pos)
            self.enter_level(next_lv, Vector(x, y))

    def on_key_press(self, symbol, mod):
        """Handle player movement"""
        if self.timer > 0:
            return
        vec = PLAYER_MOVES.get(symbol)
        if vec:
            self.player.move(vec)
        elif symbol == SPACE:
            self.player.jump()
        elif symbol == ESCAPE:
            arcade.window_commands.close_window()
        if self.level.on_exit(self.player.pos):
            self.timer = LEVEL_SWITCH_TIMER


if __name__ == '__main__':
    fruit = DungeonCrawl()
    arcade.run()
