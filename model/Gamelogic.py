import random
import pygame
import copy as copy

from model.Block import Block
from model.Tetris_piece import Tetris_piece
from view.GameDisplay import GameDisplay
from controller.TetrisController import TetrisController
from data.constants import *
import queue


class Gamelogic:
    def __init__(self):
        self.score = 0
        self.Grid = []
        self.exitGame = False
        self.pause = False
        self.dir = Direction.DOWN
        self.lightMode = True

        self.reset_game()

        self.changeViewType(ViewType.GAME, self.lightMode)
        pygame.init()
        SCREEN.fill(BLACK)

    def handle_event(self):
        self.controller.handle_event()

    def changeViewType(self, viewtype, lightmode):
        self.currentViewType = viewtype
        self.lightMode = lightmode
        self.view.setViewType(self.currentViewType, self.lightMode)

    def play(self):
        while not self.exitGame:
            self.handle_event()
            if self.currentViewType == ViewType.GAME and not self.pause:
                self.move_events()
                self.check_events()

            CLOCK.tick(60)
            self.view.draw(self.currentPiece, self.nextPieces, self.lightMode)
            pygame.display.update()
            pygame.display.flip()

    def check_events(self):
        self.checkForFullRows()
        self.view.updateScore(self.score)
        self.checkGameOver()

    def clearLastPos(self):
        blocks = self.currentPiece.blocks
        for pos in blocks:
            if pos.getY() < NBOXES_VERTICAL:
                self.Grid[pos.x][pos.getY()] = 0

    def can_go_down(self, blocks):
        lowestY = self.currentPiece.getLowestHeight()
        canGoDown = True
        # We check if we can go down
        if lowestY == NBOXES_VERTICAL - 1:
            canGoDown = False
            self.setNewPiece()
        else:
            for pos in blocks:
                if pos.getY() < NBOXES_VERTICAL - 1:
                    if self.Grid[pos.x][pos.getY() + 1] != 0:
                        canGoDown = False
                        self.setNewPiece()
                        break
        return canGoDown

    def reset_game(self):
        # initialize grid
        for x in range(NBOXES_HORIZONTAL):
            self.Grid.append([])
            for y in range(NBOXES_VERTICAL):
                self.Grid[x].append(0)

        data = tetris_data().items

        self.nextPieces = queue.Queue(5)
        for i in range(5):
            newselected = random.choice(list(data.items()))[1]
            newblocks = copy.copy(newselected[0])
            newcolor = copy.copy(newselected[1])
            self.nextPieces.put(Tetris_piece(newblocks, newcolor))
        new = self.nextPieces.get()
        self.currentPiece = Tetris_piece(new.blocks, new.color)
        self.view = GameDisplay(self.Grid, self.currentPiece)
        self.controller = TetrisController(self, self.view)
        self.dir = Direction.DOWN
        self.changeViewType(ViewType.GAME, self.lightMode)
        SCREEN.fill(BLACK)

    def can_go_left(self, blocks):
        mostLeft = self.currentPiece.getMostLeft()
        canGoLeft = True
        if mostLeft == 0:
            canGoLeft = False
        else:
            for pos in blocks:
                if pos.x > 0:
                    if self.Grid[pos.x - 1][pos.getY()] != 0:
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
                    if self.Grid[pos.x + 1][pos.getY()] != 0:
                        canGoRight = False
                        break
        return canGoRight

    def can_rotate(self, blocks):
        canRotate = True
        for pos in blocks:
            if pos.getY() < 3:  # 3 is the number of blocks from the top
                canRotate = False
                break
        return canRotate

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
            if self.can_rotate(self.currentPiece.blocks):
                self.clearLastPos()
                self.currentPiece.rotate()
                if self.can_go_down(self.currentPiece.blocks):
                    self.currentPiece.move_down()
            self.dir = Direction.DOWN

    def setNewPiece(self):
        for pos in self.currentPiece.blocks:
            self.Grid[pos.x][pos.getY()] = self.currentPiece.color
        del self.currentPiece
        data = tetris_data().items
        newselected = random.choice(list(data.items()))[1]
        newblocks = copy.copy(newselected[0])
        newcolor = copy.copy(newselected[1])
        self.nextPieces.put(Tetris_piece(newblocks, newcolor))
        self.currentPiece = self.nextPieces.get()
        # self.currentPieceType = newpiece

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
                self.score += 10

        # Delete the completed rows and shift the ones above down
        for y in rowsToDelete:
            for x in range(NBOXES_HORIZONTAL):
                for i in range(y, 0, -1):
                    self.Grid[x][i] = self.Grid[x][i - 1]
            for x in range(NBOXES_HORIZONTAL):
                self.Grid[x][0] = 0

    def checkGameOver(self):
        for x in range(NBOXES_HORIZONTAL):
            if self.Grid[x][0] != 0:
                self.pause = True
                self.changeViewType(ViewType.GAMEOVER, self.lightMode)
                return


class tetris_data:
    # Dictionary with all the pieces and their colors
    # The key is the piece type and the value is a list with the piece and the color
    # The piece is a list of blocks and the color is a tuple with the RGB values
    def __init__(self):
        self.items = {
            "I": [[Block(6, 0), Block(5, 0), Block(5, 1), Block(4, 1)], BLUE],
            "Z": [[Block(5, 0), Block(6, 0), Block(6, 1), Block(7, 1)], YELLOW],
            "O": [[Block(5, 0), Block(5, 1), Block(5, 2), Block(5, 3)], PINK],
            "J": [[Block(5, 0), Block(6, 0), Block(5, 1), Block(6, 1)], GREEN],
            "L": [[Block(5, 0), Block(6, 0), Block(7, 0), Block(5, 1)], BLUE],
            "T": [[Block(5, 0), Block(6, 0), Block(7, 0), Block(6, 1)], ORANGE],
            "S": [[Block(5, 0), Block(6, 1), Block(6, 0), Block(7, 1)], RED],
        }
