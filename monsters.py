from tilegamelib.vector import UP, DOWN, LEFT, RIGHT
import random
import arcade


class Monster(arcade.Sprite):

    def __init__(self, pos, level, player):
        super().__init__(self.tilename, 1.0)
        self.pos = pos
        self.level = level
        self.player = player
        self.update_px_position()

    def update_px_position(self):
        self.position = tuple(self.level.pos_in_pixels(self.pos))



class Zombie(Monster):

    tilename = 'stonesoup/monster/skeletal_warrior_new.png'

    def update(self):
        wuerfel = random.randint(1, 20)
        if wuerfel == 1:
            vec = random.choice([UP, DOWN, LEFT, RIGHT])
            dest = self.pos + vec
            if self.player.pos == dest:
                if not self.player.has_item('large_shield'):
                    self.player.wounded()
            elif self.level.can_enter(dest):
                self.pos = dest
                self.update_px_position()


class Dragon(Monster):

    tilename = 'stonesoup/monster/dragon.png'

    def update(self):
        wuerfel = random.randint(1, 5)
        if wuerfel == 1:
            vec = random.choice([UP, DOWN, LEFT, RIGHT])
            dest = self.pos + vec
            if self.player.pos == dest:
                self.player.wounded()
            elif self.level.can_enter(dest):
                self.pos = dest
                self.update_px_position()


MONSTERS = {
    'zombie': Zombie,
    'dragon': Dragon
}
