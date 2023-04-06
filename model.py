import random
from enum import Enum
import pygame
from constants import *
from controller import TetrisController
from views import GameDisplay
import copy as copy


class Gamelogic:
    def __init__(self):
        self.Grid = []
        # initialize grid
        for x in range(NBOXES_HORIZONTAL):
            self.Grid.append([])
            for y in range(NBOXES_VERTICAL):
                self.Grid[x].append(0)
        newselected = random.choice(list(tetris_data.items()))[1].copy()
        newpiece = copy.copy(newselected[0])
        newcolor = copy.copy(newselected[1])
        self.currentPiece = Tetris_piece(newpiece, newcolor)
        self.currentPieceType = newpiece
        self.board = TetrisBoard(self.Grid)
        self.view = GameDisplay(self.board, self.currentPiece)
        self.controller = TetrisController(self, self.view)
        self.gameOver = False
        self.dir = Direction.DOWN
        pygame.init()
        SCREEN.fill(BLACK)

    def handle_event(self):
        self.controller.handle_event()

    def play(self):
        while not self.gameOver:
            self.handle_event()
            self.move_events()
            self.checkForFullRows()
            self.view.draw(self.board.grid, self.currentPiece)
            pygame.display.update()
            CLOCK.tick(3)
            pygame.display.flip()

    def clearLastPos(self):
        blocks = self.currentPiece.blocks
        for pos in blocks:
            if pos.y < NBOXES_VERTICAL:
                self.Grid[pos.x][pos.y] = 0

    def move_events(self):
        # We reverte past grid positions to 0
        self.clearLastPos()
        # check if you can continue down
        # If we cant go down anymore we change the current piece to a new one

        lowestY = self.currentPiece.getLowestHeight()

        blocks = self.currentPiece.blocks

        canGoDown = True
        # We check if we can go down
        if lowestY == NBOXES_VERTICAL - 1:
            canGoDown = False
            self.setNewPiece()
        else:
            for pos in blocks:
                if pos.y < NBOXES_VERTICAL - 2:
                    if self.Grid[pos.x][pos.y + 1] != 0:
                        canGoDown = False
                        self.setNewPiece()
                        break

        if canGoDown:
            self.currentPiece.move_down()

        # move piece down
        if self.dir == Direction.LEFT:

            canGoLeft = True

            for pos in blocks:
                if pos.x > 2:
                    if (
                        self.currentPiece.getMostLeft() < 1
                        and self.Grid[pos.x - 1][pos.y] != 0
                    ):
                        canGoLeft = False
            if canGoLeft:
                self.currentPiece.move_left()

        if self.dir == Direction.RIGHT:
            canGoRight = True
            for pos in blocks:
                if pos.x < NBOXES_HORIZONTAL - 1:
                    if (
                        self.currentPiece.getMostRight() < NBOXES_HORIZONTAL - 2
                        and self.Grid[pos.x][pos.y] != 0
                    ):
                        canGoRight = False
            if canGoRight:
                self.currentPiece.move_right()

        if self.dir == Direction.ROTATE:
            self.clearLastPos()
            self.currentPiece.rotate()
            self.currentPiece.move_down()

        self.dir = Direction.DOWN

    def setNewPiece(self):
        for pos in self.currentPiece.blocks:
            self.Grid[pos.x][pos.y] = self.currentPiece.color
        newselected = random.choice(list(tetris_data.items()))[1]
        newpiece = copy.copy(newselected[0])
        newcolor = copy.copy(newselected[1])
        self.currentPiece = Tetris_piece(newpiece, newcolor)
        self.currentPieceType = newpiece

    def checkForFullRows(self):
        rowsToDelete = []
        for y in range(NBOXES_VERTICAL):
            rowComplete = True
            for x in range(NBOXES_HORIZONTAL):
                if self.Grid[x][y] == 0:
                    rowComplete = False
                    break
            if rowComplete:
                rowsToDelete.append(y)

        # Delete the completed rows and shift the ones above down
        for y in rowsToDelete:
            for x in range(NBOXES_HORIZONTAL):
                for i in range(y, 0, -1):
                    self.Grid[x][i] = self.Grid[x][i - 1]
            for x in range(NBOXES_HORIZONTAL):
                self.Grid[x][0] = 0

    def checkGameOver(self):
        for x in range(NBOXES_HORIZONTAL):
            if self.Grid[x][0] == 1:
                self.gameOver = True
                return


class TetrisBoard:
    def __init__(self, grid):
        self.grid = grid

    def getGrid(self):
        return self.grid

    def setGrid(self, grid):
        self.grid = grid


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


#### Dictionarys
class Block:
    def __init__(self, x, y):
        self.x = round(x)
        self.y = round(y)

    def getPos(self):
        return Block(self.x, self.y)

    def GoRight(self):
        self.x = self.x + 1

    # converts x to int
    def getX(self):
        return int(self.x)

    def getY(self):
        return int(self.y)

    def GoLeft(self):

        self.x = self.x - 1

    def GoDown(self):
        self.y = self.y + 1

    def __str__(self):
        rep = "(" + str(self.x) + " , " + str(self.y) + ")"
        return rep


tetris_data = {
    "I": [[Block(6, 0), Block(5, 0), Block(5, 1), Block(4, 1)], BLUE],
    "Z": [[Block(5, 0), Block(6, 0), Block(6, 1), Block(7, 1)], YELLOW],
    "O": [[Block(0, 0), Block(0, 1), Block(0, 2), Block(0, 3)], PINK],
    "J": [[Block(5, 0), Block(6, 0), Block(5, 1), Block(6, 1)], GREEN],
    "L": [[Block(5, 0), Block(6, 0), Block(7, 0), Block(5, 1)], BLUE],
    "T": [[Block(5, 0), Block(6, 0), Block(7, 0), Block(6, 1)], ORANGE],
    "S": [[Block(5, 0), Block(6, 0), Block(6, 1), Block(7, 1)], RED],
}
