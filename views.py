from constants import *
import pygame


class GameDisplay:
    def __init__(self, board, currentPiece):
        self.board = board
        self.currentPiece = currentPiece
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.font = pygame.font.SysFont("comicsansms", 30)
        self.gameOver = False
        self.dir = Direction.DOWN

    def draw(self, board, currentPiece):
        self.screen.fill(BLACK)
        self.drawGrid()
        self.drawCurrentPiece(currentPiece)
        # self.drawBoard(board)
        # self.drawScore()
        pygame.display.flip()

    def drawGrid(self):
        for x in range(NBOXES_HORIZONTAL):
            for y in range(NBOXES_VERTICAL):

                if self.board.grid[x][y] == 0:
                    color = WHITE
                    pygame.draw.rect(
                        SCREEN,
                        color,
                        [
                            (MARGIN + BOX_WIDTH) * x + MARGIN,
                            (MARGIN + BOX_HEIGHT) * y + MARGIN,
                            BOX_HEIGHT,
                            BOX_WIDTH,
                        ],
                    )
                else:
                    color = self.board.grid[x][y]
                    pygame.draw.rect(
                        SCREEN,
                        color,
                        [
                            (MARGIN + BOX_WIDTH) * x + MARGIN,
                            (MARGIN + BOX_HEIGHT) * y + MARGIN,
                            BOX_HEIGHT,
                            BOX_WIDTH,
                        ],
                    )

    def drawCurrentPiece(self, currentPiece):
        for pos in currentPiece.blocks:
            pygame.draw.rect(
                SCREEN,
                currentPiece.color,
                [
                    (MARGIN + BOX_WIDTH) * pos.x + MARGIN,
                    (MARGIN + BOX_HEIGHT) * pos.y + MARGIN,
                    BOX_HEIGHT,
                    BOX_WIDTH,
                ],
            )

    def drawScore(self):
        pass
        # score = self.font.render("Score: " + str(self.board.score), True, WHITE)
        # self.screen.blit(score, (WINDOW_WIDTH - 150, 10))

    def gameOver(self):
        self.gameOver = True
        self.screen.fill(BLACK)
        text = self.font.render("Game Over", True, WHITE)
        self.screen.blit(text, (WINDOW_WIDTH / 2 - 50, WINDOW_HEIGHT / 2 - 50))
        pygame.display.flip()

    def checkForGameOver(self):
        pass
