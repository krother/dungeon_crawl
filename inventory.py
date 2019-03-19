
from tilegamelib import TiledMap
from tilegamelib import Vector


class Inventory(TiledMap):

    def __init__(self, tiles, offset):
        slots = """ssss\nssss\nssss"""
        super().__init__(tiles, slots, offset=offset)
        self.items = []

    @property
    def full(self):
        return len(self.items) >= 12

    def add(self, item):
        self.items.append(item)

    def remove(self, item):
        self.items.remove(item)

    def contains(self, item):
        return item in self.items

    def draw(self):
        super().draw()
        for i, item in enumerate(self.items):
            x = i % 4
            y = i // 4
            pos = self.pos_in_pixels(Vector(x, y))
            self.tiles[item].draw(pos.x, pos.y, 32, 32)
