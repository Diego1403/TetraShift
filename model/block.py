import math


class Block:
    def __init__(self, x, y):
        self.x = math.ceil(x)
        self.y = math.ceil(y)

    def go_down(self, speed=0.1):
        self.y = self.y + speed

    def go_left(self):
        self.x = self.x - 1

    def go_right(self):
        self.x = self.x + 1

    def get_y(self):
        return math.ceil(self.y)
