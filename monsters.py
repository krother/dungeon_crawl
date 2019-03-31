from tilegamelib.vector import UP, DOWN, LEFT, RIGHT
import random
import arcade

class Zombie(arcade.Sprite):

    def __init__(self, tilename, pos, level):
        super().__init__(tilename, 1.0)
        self.pos = pos
        self.level = level
        self.update_px_position()

    def update_px_position(self):
        self.position = tuple(self.level.pos_in_pixels(self.pos))

    def update(self):
        wuerfel = random.randint(1, 6)
        if wuerfel == 6:
            vec = random.choice([UP, DOWN, LEFT, RIGHT])
            dest = self.pos + vec
            if self.level.can_enter(dest):
                self.pos = dest
                self.update_px_position()
