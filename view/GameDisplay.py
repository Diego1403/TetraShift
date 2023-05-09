import pygame
import queue
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
        # default is light mode
        self.bg_img = pygame.image.load("Images/bg_light.png")
        self.pause_screen_dark_image = pygame.image.load(
            "Images/pause_screen_dark.png "
        )
        self.pause_screen_light_image = pygame.image.load(
            "Images/pause_screen_light.png"
        )
        self.bg_img = pygame.transform.scale(self.bg_img, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.viewtype = ViewType.START
        self.start_button_image = pygame.image.load("Images/start_button.png")
        self.pause_button_image = pygame.image.load("Images/pause_button.png")
        self.continue_button_img = pygame.image.load("Images/continueGame_button.png")
        self.exit_button_img_dark = pygame.image.load("Images/exitGame_button_dark.png")
        self.exit_button_img_light = pygame.image.load(
            "Images/exitGame_button_light.png"
        )

        self.toogle_dark_img = pygame.image.load("Images/toogle_button_dark.png")
        self.toogle_light_img = pygame.image.load("Images/toogle_button_light.png")
        self.try_again_img_dark = pygame.image.load("Images/try_again_button_dark.png")
        self.try_again_img_light = pygame.image.load(
            "Images/try_again_button_light.png"
        )

        self.redblock = pygame.image.load("Images/blocks/redblock.jpg")
        self.blueblock = pygame.image.load("Images/blocks/blueblock.jpg")
        self.greenblock = pygame.image.load("Images/blocks/greenblock.jpg")
        self.pinkblock = pygame.image.load("Images/blocks/pinkblock.jpg")
        self.yellowblock = pygame.image.load("Images/blocks/yellowblock.jpg")

        self.start_button_image = pygame.transform.scale(
            self.start_button_image,
            (STARTBUTTONWIDTH, STARTBUTTONHEIGHT),
        )

        self.StartButtonCoords = (
            (WINDOW_WIDTH // 2) - STARTBUTTONWIDTH // 2,
            2 * WINDOW_HEIGHT // 3 + STARTBUTTONHEIGHT // 2,
        )

        self.pause_button_image = pygame.transform.scale(
            self.pause_button_image,
            (PAUSEBUTTONWIDTH, PAUSEBUTTONHEIGHT),
        )
        self.PauseButtonCoords = (
            (WINDOW_WIDTH // 2) - PAUSEBUTTONWIDTH // 2,
            2 * WINDOW_HEIGHT // 3 + PAUSEBUTTONHEIGHT // 2,
        )
        self.continue_button_img = pygame.transform.scale(
            self.continue_button_img,
            (CONTINUEBUTTONWIDTH, CONTINUEBUTTONHEIGHT),
        )
        self.ContinueButtonCoords = (
            (WINDOW_WIDTH // 2) - CONTINUEBUTTONWIDTH // 2,
            WINDOW_HEIGHT // 3 - CONTINUEBUTTONHEIGHT // 2,
        )
        self.exit_button_img_light = pygame.transform.scale(
            self.exit_button_img_light,
            (EXITBUTTONWIDTH, EXITBUTTONHEIGHT),
        )

        self.exit_button_img_dark = pygame.transform.scale(
            self.exit_button_img_dark,
            (EXITBUTTONWIDTH, EXITBUTTONHEIGHT),
        )

        self.ExitButtonCoords = (
            (WINDOW_WIDTH // 2) - EXITBUTTONWIDTH // 2,
            (WINDOW_HEIGHT // 3) - EXITBUTTONHEIGHT // 2 + 100,
        )

        self.try_again_img_light = pygame.transform.scale(
            self.try_again_img_light,
            (TRYAGAINBUTTONWIDTH, TRYAGAINBUTTONHEIGHT),
        )

        self.try_again_img_dark = pygame.transform.scale(
            self.try_again_img_dark,
            (TRYAGAINBUTTONWIDTH, TRYAGAINBUTTONHEIGHT),
        )

        self.TryAgainButtonCoords = (
            (WINDOW_WIDTH // 2) - TRYAGAINBUTTONWIDTH // 2,
            2 * WINDOW_HEIGHT // 3 + TRYAGAINBUTTONHEIGHT // 2,
        )

        # self.exitGame_button_image = pygame.transform.scale(
        #     self.continueGame_button_image,
        #     (STARTBUTTONWIDTH, STARTBUTTONHEIGHT),
        # )
        # self.exitGame_button_image = (
        #     (WINDOW_WIDTH // 2) - STARTBUTTONWIDTH // 2,
        #     2 * WINDOW_HEIGHT // 3 + STARTBUTTONHEIGHT // 2,
        # )

    def draw(self, currentPiece, nextPieces, lightmode=True):
        if self.viewtype == ViewType.START:
            self.drawStartScreen(lightmode)
        elif self.viewtype == ViewType.GAME:
            self.drawGame(currentPiece, nextPieces, lightmode)
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
            self.drawGameOverScreen(lightmode)
        elif viewtype == ViewType.PAUSE:
            self.drawPauseScreen(lightmode)
        self.currentViewType = viewtype

    def drawGame(self, currentPiece, nextPieces, lightmode):
        self.screen.blit(self.bg_img, (0, 0))
        self.drawScreen()
        self.drawGrid()
        self.drawCurrentPiece(currentPiece)
        self.drawScoreboard()
        self.drawPauseButton()
        self.drawNextPiece(nextPieces)

    def drawNextPiece(self, nextPieces):
        for i in range(len(nextPieces.queue)):
            drawPiece = nextPieces.queue[i]
            self.drawPiece(drawPiece, i)

    def drawPiece(self, piece, i):
        CELL_SIZE = 13
        for block in piece.blocks:
            pygame.draw.rect(
                self.screen,
                piece.color,
                (
                    block.getX() + block.getX() * CELL_SIZE + WINDOW_WIDTH * 3 // 4,
                    block.getY()
                    + block.getY() * CELL_SIZE
                    + GAME_HEIGHT // 3
                    + i * 4 * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE,
                ),
            )

    def drawGameOverScreen(self, lightmode=True):
        if lightmode:
            self.bg_img = pygame.image.load("Images/game_over_light.png")
            self.bg_img = pygame.transform.scale(
                self.bg_img, (WINDOW_WIDTH, WINDOW_HEIGHT)
            )

        else:
            self.bg_img = pygame.image.load("Images/game_over_dark.png")
            self.bg_img = pygame.transform.scale(
                self.bg_img, (WINDOW_WIDTH, WINDOW_HEIGHT)
            )

        self.drawExitGame(lightmode)
        self.drawTryAgain(lightmode)

    def drawTryAgain(self, lightmode):
        if lightmode:
            self.screen.blit(
                self.try_again_img_light,
                self.TryAgainButtonCoords,
            )
        else:
            self.screen.blit(
                self.try_again_img_dark,
                self.TryAgainButtonCoords,
            )

    def drawStartScreen(self, lightmode):
        self.screen.blit(self.bg_img, (0, 0))
        self.drawStartButton()

    def drawStartButton(self):
        self.StartButtonCoords = (
            (WINDOW_WIDTH // 2) - STARTBUTTONWIDTH // 2,
            2 * WINDOW_HEIGHT // 3 + STARTBUTTONHEIGHT // 2,
        )
        self.screen.blit(
            self.start_button_image,
            self.StartButtonCoords,
        )

    def drawPauseButton(self):
        self.screen.blit(
            self.pause_button_image,
            self.PauseButtonCoords,
        )

    def drawPauseScreen(self, lightmode=True):
        self.drawContinueGame(lightmode)
        # self.drawExitGame(lightmode)

    def drawContinueGame(self, lightmode=True):
        self.screen.blit(self.continue_button_img, self.ContinueButtonCoords)

    def drawExitGame(self, lightmode=True):
        if lightmode:
            self.screen.blit(self.exit_button_img_light, self.ExitButtonCoords)
        else:
            self.screen.blit(self.exit_button_img_dark, self.ExitButtonCoords)

    def drawGrid(self):
        x_offset = (WINDOW_WIDTH - GAME_WIDTH) // 2
        y_offset = 0
        grid = pygame.image.load("Images/bg_grid.png")
        grid = pygame.transform.scale(grid, (GAME_WIDTH, GAME_HEIGHT))
        self.screen.blit(grid, (x_offset, y_offset))
        for x in range(NBOXES_HORIZONTAL):
            for y in range(NBOXES_VERTICAL):
                # draw all pieces

                if self.board[x][y] != 0:
                    color = self.board[x][y]
                    pos = (
                        x_offset + (MARGIN + BOX_WIDTH) * x + MARGIN,
                        y_offset + (MARGIN + BOX_HEIGHT) * y + MARGIN,
                    )

                    self.drawBlock(color, pos)

    def drawCurrentPiece(self, currentPiece):
        x_offset = (WINDOW_WIDTH - GAME_WIDTH) // 2
        y_offset = 0

        for block in currentPiece.blocks:
            pos = (
                x_offset + (MARGIN + BOX_WIDTH) * block.x + MARGIN,
                y_offset + (MARGIN + BOX_HEIGHT) * block.y + MARGIN,
            )
            self.drawBlock(currentPiece.color, pos)

    def drawBlock(self, color, pos):
        block = self.redblock
        if color == RED:
            block = self.redblock
        elif color == BLUE:
            block = self.blueblock
        elif color == GREEN:
            block = self.greenblock
        elif color == YELLOW:
            block = self.yellowblock
        elif color == PURPLE:
            block = self.purpleblock

        image = pygame.transform.scale(block, (BOX_WIDTH, BOX_HEIGHT))
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

    def drawGameOver(self):
        text = self.font.render("Game Over", True, WHITE)
        self.screen.blit(text, (WINDOW_WIDTH / 2 - 50, WINDOW_HEIGHT / 2 - 50))

    def updateScore(self, score):
        self.score = score

    def get_StartButtonData(self):
        return self.StartButtonCoords, self.start_button_image.get_size()

    def get_PauseButtonData(self):
        return self.PauseButtonCoords, self.pause_button_image.get_size()

    def get_ContinueButtonData(self):
        return self.ContinueButtonCoords, self.continue_button_img.get_size()

    def get_ExitButtonData(self):
        return self.ExitButtonCoords, self.exit_button_img_light.get_size()
