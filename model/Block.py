import math as math

from data.constants import NBOXES_HORIZONTAL


class Block:
    def __init__(self, x, y):
        self.x = math.ceil(x)
        self.y = math.ceil(y)

    def getPos(self):
        return Block(self.x, self.y)

    def GoDown(self):
        self.y = self.y + 0.1

    def GoLeft(self):
        if self.x > 0:
            self.x = self.x - 1

    def GoRight(self):
        if self.x < NBOXES_HORIZONTAL - 1:
            self.x = self.x + 1

    # converts x to int
    def getX(self):
        return self.x

    def getY(self):
        return math.ceil(self.y)
