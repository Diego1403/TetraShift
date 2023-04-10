import pygame

from data.constants import *


class GameDisplay:
    def __init__(self, board, currentPiece):
        self.board = board
        self.currentPiece = currentPiece
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.titleFont = pygame.font.SysFont("comicsansms", 50)
        self.font = pygame.font.SysFont("comicsansms", 30)
        self.gameOver = False
        self.dir = Direction.DOWN
        self.scoreFont = pygame.font.SysFont("comicsansms", 30)
        self.bg_img = pygame.image.load("Images/bg.jpg")
        self.bg_img = pygame.transform.scale(self.bg_img, (WINDOW_WIDTH, WINDOW_HEIGHT))

    def draw(self, board, currentPiece):
        # we draw the background
        self.screen.blit(self.bg_img, (0, 0))

        title = self.titleFont.render("Tetris", True, WHITE)
        self.drawScreen()
        self.drawGrid()
        self.drawCurrentPiece(currentPiece)
        self.screen.blit(title, (WINDOW_WIDTH / 2 - title.get_width() / 2, 20))
        self.drawScoreboard()
        pygame.display.update()
        pygame.display.flip()

    def drawGrid(self):
        x_offset = (WINDOW_WIDTH - GAME_WIDTH) // 2
        y_offset = 0
        for x in range(NBOXES_HORIZONTAL):
            for y in range(NBOXES_VERTICAL):
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
        font = pygame.font.SysFont("comicsansms", 32)
        text = font.render("Score: {}".format(4), True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (SCOREBOARD_WIDTH, SCOREBOARD_HEIGHT)
        SCREEN.blit(text, text_rect)

    def gameOver(self):
        self.gameOver = True
        self.screen.fill(BLACK)
        text = self.font.render("Game Over", True, WHITE)
        self.screen.blit(text, (WINDOW_WIDTH / 2 - 50, WINDOW_HEIGHT / 2 - 50))
        pygame.display.flip()

    def checkForGameOver(self):
        pass
