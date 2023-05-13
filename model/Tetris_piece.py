import math
import copy as copy
from data.constants import NBOXES_HORIZONTAL, NBOXES_VERTICAL


class Tetris_piece:
    def __init__(self, blocks, color):
        self.color = copy.deepcopy(color)
        self.blocks = copy.deepcopy(blocks)

    def move_right(self):
        for block in self.blocks:
            if block.x > NBOXES_HORIZONTAL - 1:
                pass
        for block in self.blocks:
            block.GoRight()

    def move_left(self):
        for block in self.blocks:
            if block.x < 0:
                pass
        for block in self.blocks:
            block.GoLeft()

    def move_down(self, speed=0.1):
        for block in self.blocks:
            block.GoDown(speed)

    def getLowestHeight(self):
        lowest_pos = 0

        for block in self.blocks:
            if block.getY() > lowest_pos:
                lowest_pos = block.getY()
        return math.ceil(lowest_pos)

    def getMostLeft(self):
        mostLeft_pos = NBOXES_HORIZONTAL
        for block in self.blocks:
            if block.x < mostLeft_pos:
                mostLeft_pos = block.x
        return mostLeft_pos

    def getMostRight(self):
        mostRight_pos = 0
        for block in self.blocks:
            if block.x > mostRight_pos:
                mostRight_pos = block.x
        return mostRight_pos

    def getMostTop(self):
        mostTop_pos = NBOXES_VERTICAL
        for block in self.blocks:
            if block.y < mostTop_pos:
                mostTop_pos = block.y
        return mostTop_pos

    def rotate(self):
        center_x = sum([block.x for block in self.blocks]) // len(self.blocks)
        center_y = sum([block.getY() for block in self.blocks]) // len(self.blocks)

        for block in self.blocks:
            new_x = center_x + (block.getY() - center_y)
            new_y = center_y - (block.x - center_x)
            block.x = new_x
            block.y = new_y
        for block in self.blocks:
            block.y = block.y + 0.5
        
        

    def __str__(self):
        for block in self.blocks:
            print(" (" + block + " ),")
