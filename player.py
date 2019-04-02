from inventory import Inventory
from tilegamelib import Vector


class Player:

    def __init__(self, tiles, pos):
        self.tiles = tiles
        self.pos = pos
        self.level = None
        self.inv = Inventory(self.tiles, offset=Vector(500, 500))
        self._lastvec = Vector(0, 0)

    def draw(self):
        self.inv.draw()
        px = self.level.pos_in_pixels(self.pos)
        self.tiles['player'].draw(px.x, px.y, 32, 32)

    def move(self, vec):
        dest = self.pos + vec
        if self.level.has_monster(dest):
            if self.has_item('short_sword_3'):
                self.level.kill(dest)
        elif self.level.is_deadly(dest, self):
            self.die()
        elif self.level.can_enter(dest):
            self.pos = dest
            item = self.level.take_item(self.pos)
            if item:
                self.inv.add(item)
        else:
            self.level.interact(dest, self.inv)
        self._lastvec = vec

    def jump(self):
        p1 = self.pos + self._lastvec
        if self.level.can_enter(p1):
            self.pos = p1
            self.move(self._lastvec)

    def has_item(self, item):
        return item in self.inv.items
