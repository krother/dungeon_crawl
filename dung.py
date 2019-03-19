
# tiles from : https://opengameart.org/content/dungeon-crawl-32x32-tiles

# try:
# https://opengameart.org/content/lpc-tile-atlas
# https://opengameart.org/content/lpc-tile-atlas2
# https://opengameart.org/content/lots-of-free-2d-tiles-and-sprites-by-hyptosis

import time
import re
import random
import arcade
from arcade.key import ESCAPE
from tilegamelib import TiledMap, load_tiles
from tilegamelib import MapMove
from tilegamelib import PLAYER_MOVES
from tilegamelib import Vector
from tilegamelib.vector import UP, DOWN, LEFT, RIGHT
from level import Level
from inventory import Inventory

SIZEX, SIZEY = (800, 600)
LEVEL_SWITCH_TIMER = 25

SYNONYMS = [
    ('.', 'grey_dirt_0_new'),
    ('#', 'brick_gray_0'),
    ('player', 'deep_elf_fighter_new'),
    ('s', 'slot'),
]


class Zombie:

    def __init__(self, tiles, pos, level):
        self.tiles = tiles
        self.pos = pos
        self.level = level

    def draw(self):
        px = self.level.pos_in_pixels(self.pos)
        self.tiles['skeletal_warrior_new'].draw(px.x, px.y, 32, 32)

    def move(self):
        wuerfel = random.randint(1, 6)
        if wuerfel == 6:
            vec = random.choice([UP, DOWN, LEFT, RIGHT])
            dest = self.pos + vec
            if self.level.can_enter(dest):
                self.pos = dest


class Player:

    def __init__(self, tiles, pos):
        self.tiles = tiles
        self.pos = pos
        self.level = None
        self.inv = Inventory(self.tiles, offset=Vector(500, 500))

    def draw(self):
        self.inv.draw()
        px = self.level.pos_in_pixels(self.pos)
        self.tiles['player'].draw(px.x, px.y, 32, 32)

    def move(self, vec):
        dest = self.pos + vec
        if self.level.has_monster(dest):
            if self.has_item('short_sword_3'):
                self.level.kill(dest)
        elif self.level.can_enter(dest):
            self.pos = dest
            item = self.level.take_item(self.pos)
            if item:
                self.inv.add(item)
        else:
            self.level.interact(dest, self.inv)

    def has_item(self, item):
        return item in self.inv.items



class DungeonCrawl(arcade.Window):

    def __init__(self):
        super().__init__(SIZEX, SIZEY, "Dungeon Crawl")
        arcade.set_background_color(arcade.color.BLACK)
        self.tiles = load_tiles('stonesoup.csv')
        self.add_tile_synonyms()
        self.player = Player(self.tiles, None)
        self.level = None
        self.enter_level('levels/lv1.json', Vector(1, 2))

    def create_zombies(self):
        zombie_horde = []
        for i in range(10):
            x = random.randint(5, 12)
            y = random.randint(2, 10)
            z = Zombie(self.tiles, Vector(x, y), self.level)
            zombie_horde.append(z)
        return zombie_horde

    def enter_level(self, filename, pos):
        self.level = Level(filename, self.tiles, offset=Vector(50, 50))
        self.player.level = self.level
        self.player.pos = pos
        self.level.add_monsters(self.create_zombies())
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
            if self.level.on_exit(self.player.pos):
                self.timer = LEVEL_SWITCH_TIMER
        elif symbol == ESCAPE:
            arcade.window_commands.close_window()


if __name__ == '__main__':
    fruit = DungeonCrawl()
    arcade.run()
