import math as math

from data.constants import NBOXES_HORIZONTAL


class Block:
    def __init__(self, x, y):
        self.x = math.ceil(x)
        self.y = math.ceil(y)

    def getPos(self):
        return Block(self.x, self.y)

    # default speed is 1
    def GoDown(self, speed=0.1):
        self.y = self.y + speed

    def GoLeft(self):
        self.x = self.x - 1

    def GoRight(self):
        self.x = self.x + 1

    # converts x to int
    def getX(self):
        return self.x

    def getY(self):
        return math.ceil(self.y)
