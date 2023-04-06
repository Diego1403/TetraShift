import pygame
from constants import Direction


class TetrisController:
    def __init__(self, gamelogic, view):
        self.gamelogic = gamelogic
        self.view = view

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.gamelogic.gameOver = True
                pygame.display.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.gamelogic.dir = Direction.LEFT
                if event.key == pygame.K_RIGHT:
                    self.gamelogic.dir = Direction.RIGHT
                if event.key == pygame.K_UP:
                    self.gamelogic.dir = Direction.ROTATE
                if event.key == pygame.K_DOWN:
                    # move shape down and force move events
                    self.gamelogic.dir = Direction.DOWN
