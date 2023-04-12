import pygame

from data.constants import *


class GameDisplay:
    def __init__(self, board, currentPiece):
        self.board = board
        self.currentPiece = currentPiece
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.font = pygame.font.SysFont("comicsansms", 30)
        self.gameOver = False
        self.score = 0
        self.dir = Direction.DOWN
        self.scoreFont = pygame.font.SysFont("comicsansms", 30)
        self.bg_img = pygame.image.load("Images/bg.png")
        self.bg_img = pygame.transform.scale(self.bg_img, (WINDOW_WIDTH, WINDOW_HEIGHT))

    def draw(self, board, currentPiece):
        # we draw the background
        self.screen.blit(self.bg_img, (0, 0))

        self.drawScreen()
        self.drawGrid()
        self.drawCurrentPiece(currentPiece)
        self.drawScoreboard()
        pygame.display.update()
        pygame.display.flip()

    def drawGrid(self):
        x_offset = (WINDOW_WIDTH - GAME_WIDTH) // 2
        y_offset = 0
        grid = pygame.image.load("Images/bg_grid.png")
        grid = pygame.transform.scale(grid, (GAME_WIDTH, GAME_HEIGHT))
        self.screen.blit(grid, (x_offset, y_offset))
        for x in range(NBOXES_HORIZONTAL):
            for y in range(NBOXES_VERTICAL):
                # draw all pieces
                if self.board.grid[x][y] != 0:
                    color = self.board.grid[x][y]
                    rect = pygame.draw.rect(
                        SCREEN,
                        color,
                        [
                            x_offset + (MARGIN + BOX_WIDTH) * x + MARGIN,
                            y_offset + (MARGIN + BOX_HEIGHT) * y + MARGIN,
                            BOX_HEIGHT,
                            BOX_WIDTH,
                        ],
                    )

    def drawCurrentPiece(self, currentPiece):
        x_offset = (WINDOW_WIDTH - GAME_WIDTH) // 2
        y_offset = 0
        for pos in currentPiece.blocks:
            pygame.draw.rect(
                SCREEN,
                currentPiece.color,
                [
                    x_offset + (MARGIN + BOX_WIDTH) * pos.x + MARGIN,
                    y_offset + (MARGIN + BOX_HEIGHT) * pos.y + MARGIN,
                    BOX_HEIGHT,
                    BOX_WIDTH,
                ],
            )

    def drawScreen(self):
        pygame.draw.rect(self.screen, WHITE, [0, 0, WINDOW_WIDTH, WINDOW_HEIGHT], 5)

    def drawScoreboard(self):
        x_offset = 120
        y_offset = 120
        pygame.draw.rect(self.screen, WHITE, [0, 0, 50, WINDOW_HEIGHT], 5)
        font = pygame.font.SysFont("comicsansms", 16)
        text = font.render("{}".format(self.score), True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (SCOREBOARD_WIDTH, SCOREBOARD_HEIGHT)
        self.screen.blit(text, (x_offset, y_offset))

    def gameOver(self):
        self.gameOver = True
        self.screen.fill(BLACK)
        text = self.font.render("Game Over", True, WHITE)
        self.screen.blit(text, (WINDOW_WIDTH / 2 - 50, WINDOW_HEIGHT / 2 - 50))
        pygame.display.flip()

    def updateScore(self, score):
        self.score = score

    def checkForGameOver(self):
        pass
