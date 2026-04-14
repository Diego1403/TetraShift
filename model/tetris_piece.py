import math
import copy

from data.config import NBOXES_HORIZONTAL, NBOXES_VERTICAL


class TetrisPiece:
    def __init__(self, blocks, color):
        self.color = copy.deepcopy(color)
        self.blocks = copy.deepcopy(blocks)

    def move_right(self):
        for block in self.blocks:
            if block.x > NBOXES_HORIZONTAL - 1:
                return
        for block in self.blocks:
            block.go_right()

    def move_left(self):
        for block in self.blocks:
            if block.x < 0:
                return
        for block in self.blocks:
            block.go_left()

    def move_down(self, speed=0.1):
        for block in self.blocks:
            block.go_down(speed)

    def get_lowest_height(self):
        lowest_pos = 0
        for block in self.blocks:
            if block.get_y() > lowest_pos:
                lowest_pos = block.get_y()
        return math.ceil(lowest_pos)

    def get_most_left(self):
        most_left_pos = NBOXES_HORIZONTAL
        for block in self.blocks:
            if block.x < most_left_pos:
                most_left_pos = block.x
        return most_left_pos

    def get_most_right(self):
        most_right_pos = 0
        for block in self.blocks:
            if block.x > most_right_pos:
                most_right_pos = block.x
        return most_right_pos

    def get_most_top(self):
        most_top_pos = NBOXES_VERTICAL
        for block in self.blocks:
            if block.y < most_top_pos:
                most_top_pos = block.y
        return most_top_pos

    def rotate(self):
        center_x = sum([block.x for block in self.blocks]) // len(self.blocks)
        center_y = sum([block.get_y() for block in self.blocks]) // len(self.blocks)

        if center_x == 0:
            center_x = 1
        if center_y == 0:
            center_y = 1

        for block in self.blocks:
            new_x = center_x + (block.get_y() - center_y)
            new_y = center_y - (block.x - center_x)
            block.x = new_x
            block.y = new_y

        for block in self.blocks:
            block.y = block.y + 0.5

    def __str__(self):
        parts = []
        for block in self.blocks:
            parts.append(f" ({block.x}, {block.get_y()}),")
        return "\n".join(parts)
