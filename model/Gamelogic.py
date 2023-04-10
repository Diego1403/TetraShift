import random
import pygame
import copy as copy

from model.Block import Block
from model.TetrisBoard import TetrisBoard
from model.Tetris_piece import Tetris_piece
from view.GameDisplay import GameDisplay
from controller.TetrisController import TetrisController
from data.constants import *


class Gamelogic:
    def __init__(self):
        self.Grid = []
        # initialize grid
        for x in range(NBOXES_HORIZONTAL):
            self.Grid.append([])
            for y in range(NBOXES_VERTICAL):
                self.Grid[x].append(0)
        self.data = tetris_data().items
        newselected = random.choice(list(self.data.items()))[1]
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

    def can_go_down(self, blocks):
        lowestY = self.currentPiece.getLowestHeight()
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
        return canGoDown

    def can_go_left(self, blocks):
        mostLeft = self.currentPiece.getMostLeft()
        canGoLeft = True
        if mostLeft == 0:
            canGoLeft = False
        else:
            for pos in blocks:
                if pos.x > 0:
                    if self.Grid[pos.x - 1][pos.y] != 0:
                        canGoLeft = False
                        break
        return canGoLeft

    def can_go_right(self, blocks):
        mostRight = self.currentPiece.getMostRight()
        canGoRight = True
        if mostRight == NBOXES_HORIZONTAL - 1:
            canGoRight = False
        else:
            for pos in blocks:
                if pos.x < NBOXES_HORIZONTAL - 1:
                    if self.Grid[pos.x + 1][pos.y] != 0:
                        canGoRight = False
                        break
        return canGoRight

    def move_events(self):
        # We reverte past grid positions to 0
        self.clearLastPos()
        # check if you can continue down
        # If we cant go down anymore we change the current piece to a new one
        blocks = self.currentPiece.blocks
        if self.can_go_down(blocks):
            self.currentPiece.move_down()

        if self.dir == Direction.LEFT:
            if self.can_go_left(blocks):
                self.currentPiece.move_left()
                self.dir = Direction.DOWN

        if self.dir == Direction.RIGHT:
            if self.can_go_right(blocks):
                self.currentPiece.move_right()
                self.dir = Direction.DOWN

        if self.dir == Direction.ROTATE:
            self.clearLastPos()
            self.currentPiece.rotate()
            self.currentPiece.move_down()
            self.dir = Direction.DOWN

    def setNewPiece(self):
        for pos in self.currentPiece.blocks:
            self.Grid[pos.x][pos.y] = self.currentPiece.color
        del self.currentPiece
        data = tetris_data().items
        newselected = random.choice(list(data.items()))[1]
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


class tetris_data:
    def __init__(self):
        self.items = {
            "I": [[Block(6, 0), Block(5, 0), Block(5, 1), Block(4, 1)], BLUE],
            "Z": [[Block(5, 0), Block(6, 0), Block(6, 1), Block(7, 1)], YELLOW],
            "O": [[Block(0, 0), Block(0, 1), Block(0, 2), Block(0, 3)], PINK],
            "J": [[Block(5, 0), Block(6, 0), Block(5, 1), Block(6, 1)], GREEN],
            "L": [[Block(5, 0), Block(6, 0), Block(7, 0), Block(5, 1)], BLUE],
            "T": [[Block(5, 0), Block(6, 0), Block(7, 0), Block(6, 1)], ORANGE],
            "S": [[Block(5, 0), Block(6, 0), Block(6, 1), Block(7, 1)], RED],
        }
