from inventory import Inventory
from tilegamelib import Vector
import arcade


class Player:

    def __init__(self, tiles, pos):
        self.tiles = tiles
        self.pos = pos
        self.level = None
        self.inv = Inventory(self.tiles, offset=Vector(550, 500))
        self.life = Inventory(self.tiles, offset=Vector(550, 400), rows=1, cols=5)
        self._lastvec = Vector(0, 0)
        for i in range(5):
            self.life.add('heart')

    def die(self):
        arcade.window_commands.close_window()

    def draw(self):
        self.inv.draw()
        self.life.draw()
        px = self.level.pos_in_pixels(self.pos)
        self.tiles['player'].draw(px.x, px.y, 32, 32)

    def wounded(self):
        self.life.remove('heart')
        if not 'heart' in self.life.items:
            self.die()

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
            self.level.interact(dest, self)
        if self.level.is_deadly(self.pos, self):
            self.wounded()
        self._lastvec = vec

    def jump(self):
        p1 = self.pos + self._lastvec
        if self.level.can_enter(p1):
            self.pos = p1
            self.move(self._lastvec)

    def has_item(self, item):
        return item in self.inv.items
