
import json
import re
from tilegamelib import TiledMap
from tilegamelib import Vector
from monsters import MONSTERS

ACCESSIBLE = {'open_door', 'stone_stairs_down', 'stone_stairs_up'}
FLOOR = {'.', '~'}


class Level(TiledMap):

    def __init__(self, filename, tiles, player, offset):
        self.tiles = tiles
        self.player = player
        j = json.load(open(filename))
        dungeon = '\n'.join(j['map'])
        super().__init__(tiles, dungeon, offset)
        self.items = self.load_specials(j['items'])
        self.locations = self.load_specials(j['locations'])
        self.exits = self.load_specials(j['exits'])
        self.monsters = self.create_monsters(j['monsters'])

    def create_monsters(self, monsters):
        mon = []
        for name, x, y in monsters:
            mtype = MONSTERS[name]
            m = mtype(Vector(x, y), self, self.player)
            mon.append(m)
        return mon

    def load_specials(self, things):
        result = {}
        for name, x, y in things:
            pos = Vector(x, y)
            result[pos] = name
        return result

    def has_monster(self, pos):
        for m in self.monsters:
            if m.pos == pos:
                return True

    def kill(self, pos):
        for m in self.monsters:
            if m.pos == pos:
                self.monsters.remove(m)
                return

    def draw(self):
        super().draw()
        for pos, name in self.items.items():
            px = self.pos_in_pixels(pos)
            self.tiles[name].draw(px.x, px.y, 32, 32)
        for pos, name in self.locations.items():
            px = self.pos_in_pixels(pos)
            self.tiles[name].draw(px.x, px.y, 32, 32)
        for m in self.monsters:
            m.draw()

    def update(self):
        for m in self.monsters:
            m.update()

    def can_enter(self, pos):
        loc = self.locations.get(pos)
        if not loc and self.at(pos) in FLOOR:
            return True
        elif loc in ACCESSIBLE:
            return True

    def is_deadly(self, pos, plr):
        if self.at(pos) == '~':
            return True

    def interact(self, pos, player):
        loc = self.locations.get(pos)
        if loc:
            if loc == 'closed_door' and player.inv.contains('key'):
                player.inv.remove('key')
                self.locations[pos] = 'open_door'
            if loc == 'blue_fountain':
                player.life.add('heart')


    def take_item(self, pos):
        item = self.items.get(pos)
        if item:
            del self.items[pos]
            return item

    def on_exit(self, pos):
        return self.exits.get(pos)


if __name__ == '__main__':
    Level()
