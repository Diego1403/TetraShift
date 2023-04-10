from data.constants import NBOXES_HORIZONTAL


class Tetris_piece:
    def __init__(self, blocks, color):
        self.color = color
        self.orientation = 0
        self.blocks = blocks

    def move_right(self):
        for block in self.blocks:
            block.GoRight()

    def move_left(self):
        for block in self.blocks:
            block.GoLeft()

    def move_down(self):
        for block in self.blocks:
            block.GoDown()

    def getLowestHeight(self):
        lowest_pos = 0
        for block in self.blocks:
            if block.y > lowest_pos:
                lowest_pos = block.y
        return int(lowest_pos)

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

    def rotate(self):
        center_x = sum([block.x for block in self.blocks]) // len(self.blocks)
        center_y = sum([block.y for block in self.blocks]) // len(self.blocks)

        for block in self.blocks:
            new_x = center_x + (block.y - center_y)
            new_y = center_y - (block.x - center_x)
            block.x = new_x
            block.y = new_y

    def __str__(self):
        for block in self.blocks:
            print(" (" + block + " ),")
