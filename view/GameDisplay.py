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
        self.bg_img = pygame.image.load("Images/bg_light.png")
        self.bg_img = pygame.transform.scale(self.bg_img, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.viewtype = ViewType.START
        self.button_image = pygame.image.load("Images/start_button.png")
        self.redblock = pygame.image.load("Images/blocks/redblock.jpg")
        self.blueblock = pygame.image.load("Images/blocks/blueblock.jpg")
        self.greenblock = pygame.image.load("Images/blocks/greenblock.jpg")
        self.pinkblock = pygame.image.load("Images/blocks/pinkblock.jpg")
        self.yellowblock = pygame.image.load("Images/blocks/yellowblock.jpg")

        self.button_image = pygame.transform.scale(
            self.button_image,
            (STARTBUTTONWIDTH, STARTBUTTONHEIGHT),
        )
        self.StartButtonCoords = (
            (WINDOW_WIDTH // 2) - STARTBUTTONWIDTH // 2,
            2 * WINDOW_HEIGHT // 3 + STARTBUTTONHEIGHT // 2,
        )

    def draw(self, currentPiece, lightmode=True):
        if self.viewtype == ViewType.START:
            self.drawStartScreen(lightmode)
        elif self.viewtype == ViewType.GAME:
            self.drawGame(currentPiece, lightmode)
        elif self.viewtype == ViewType.GAMEOVER:
            self.drawGameOverScreen(lightmode)
        elif self.viewtype == ViewType.PAUSE:
            self.drawPauseScreen(lightmode)

    def setViewType(self, viewtype, lightmode):
        self.lightmode = lightmode
        self.viewtype = viewtype
        if viewtype == ViewType.START:
            self.viewtype = ViewType.START
            if lightmode:
                self.lightmode = True
                self.bg_img = pygame.image.load("Images/bg_start_light.png")
                self.bg_img = pygame.transform.scale(
                    self.bg_img, (WINDOW_WIDTH, WINDOW_HEIGHT)
                )
            else:
                self.lightmode = False
                self.bg_img = pygame.image.load("Images/bg_start_dark.png")
                self.bg_img = pygame.transform.scale(
                    self.bg_img, (WINDOW_WIDTH, WINDOW_HEIGHT)
                )
        elif viewtype == ViewType.GAME:
            if lightmode:
                self.lightmode = True
                self.bg_img = pygame.image.load("Images/bg_light.png")
                self.bg_img = pygame.transform.scale(
                    self.bg_img, (WINDOW_WIDTH, WINDOW_HEIGHT)
                )
            else:
                self.lightmode = False
                self.bg_img = pygame.image.load("Images/bg_dark.png")
                self.bg_img = pygame.transform.scale(
                    self.bg_img, (WINDOW_WIDTH, WINDOW_HEIGHT)
                )
        elif viewtype == ViewType.GAMEOVER:
            if lightmode:
                self.lightmode = True
                self.bg_img = pygame.image.load("Images/gameOver_light.png")
                self.bg_img = pygame.transform.scale(
                    self.bg_img, (WINDOW_WIDTH, WINDOW_HEIGHT)
                )
            else:
                self.lightmode = False
                self.bg_img = pygame.image.load("Images/gameOver_dark.png")
                self.bg_img = pygame.transform.scale(
                    self.bg_img, (WINDOW_WIDTH, WINDOW_HEIGHT)
                )
        elif viewtype == ViewType.PAUSE:
            if lightmode:
                self.lightmode = True
                self.bg_img = pygame.image.load("Images/bg_pause_light.png")
                self.bg_img = pygame.transform.scale(
                    self.bg_img, (WINDOW_WIDTH, WINDOW_HEIGHT)
                )
            else:
                self.lightmode = False
                self.bg_img = pygame.image.load("Images/bg_pause_dark.png")
                self.bg_img = pygame.transform.scale(
                    self.bg_img, (WINDOW_WIDTH, WINDOW_HEIGHT)
                )

        elif viewtype == ViewType.GAMEOVER:
            pass
        elif viewtype == ViewType.PAUSE:
            self.drawPauseScreen(lightmode)
        self.currentViewType = viewtype

    def drawGame(self, currentPiece, lightmode=True):
        self.screen.blit(self.bg_img, (0, 0))
        self.drawScreen()
        self.drawGrid()
        self.drawCurrentPiece(currentPiece)
        self.drawScoreboard()

    def drawStartScreen(self, lightmode=True):
        self.screen.blit(self.bg_img, (0, 0))
        self.drawStartButton()

    def drawStartButton(self):
        self.StartButtonCoords = (
            (WINDOW_WIDTH // 2) - STARTBUTTONWIDTH // 2,
            2 * WINDOW_HEIGHT // 3 + STARTBUTTONHEIGHT // 2,
        )
        self.screen.blit(
            self.button_image,
            self.StartButtonCoords,
        )

    def drawGameOverScreen(self, lightmode=True):
        if lightmode:
            self.bg_img = pygame.image.load("Images/gameOver_light.png")
            self.bg_img = pygame.transform.scale(
                self.bg_img, (WINDOW_WIDTH, WINDOW_HEIGHT)
            )
        else:
            self.bg_img = pygame.image.load("Images/gameOver_dark.png")
            self.bg_img = pygame.transform.scale(
                self.bg_img, (WINDOW_WIDTH, WINDOW_HEIGHT)
            )

        self.screen.blit(self.bg_img, (0, 0))

    def drawPauseScreen(self, lightmode=True):
        if lightmode:
            self.bg_img = pygame.image.load("Images/pauseScreen_light.png")
            self.bg_img = pygame.transform.scale(
                self.bg_img, (WINDOW_WIDTH, WINDOW_HEIGHT)
            )
        else:
            self.bg_img = pygame.image.load("Images/pauseScreen_dark.png")
            self.bg_img = pygame.transform.scale(
                self.bg_img, (WINDOW_WIDTH, WINDOW_HEIGHT)
            )

        self.screen.blit(self.bg_img, (0, 0))

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

        block = self.redblock

        if currentPiece.color == RED:
            block = self.redblock
        elif currentPiece.color == BLUE:
            block = self.blueblock
        elif currentPiece.color == GREEN:
            block = self.greenblock
        elif currentPiece.color == YELLOW:
            block = self.yellowblock
        elif currentPiece.color == PURPLE:
            block = self.purpleblock

        image = pygame.transform.scale(block, (BOX_WIDTH, BOX_HEIGHT))

        for block in currentPiece.blocks:
            pos = (
                x_offset + (MARGIN + BOX_WIDTH) * block.x + MARGIN,
                y_offset + (MARGIN + BOX_HEIGHT) * block.y + MARGIN,
            )
            SCREEN.blit(image, pos)

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

    def updateScore(self, score):
        self.score = score

    def checkForGameOver(self):
        pass

    def get_StartButtonData(self):
        return self.StartButtonCoords, self.button_image.get_size()
