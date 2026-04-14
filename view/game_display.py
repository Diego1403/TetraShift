import pygame

from data.colors import (
    BLACK, WHITE, RED, BLUE, GREEN, YELLOW, PINK, PURPLE, ORANGE,
)
from data.enums import ViewType
from data.config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, GAME_WIDTH, GAME_HEIGHT,
    BOX_WIDTH, BOX_HEIGHT, MARGIN, NBOXES_HORIZONTAL, NBOXES_VERTICAL,
    SCOREBOARD_WIDTH, SCOREBOARD_HEIGHT,
    STARTBUTTONWIDTH, STARTBUTTONHEIGHT,
    PAUSEBUTTONWIDTH, PAUSEBUTTONHEIGHT,
    CONTINUEBUTTONWIDTH, CONTINUEBUTTONHEIGHT,
    EXITBUTTONWIDTH, EXITBUTTONHEIGHT,
    TRYAGAINBUTTONWIDTH, TRYAGAINBUTTONHEIGHT,
)
from data.constants import SCREEN


class GameDisplay:
    def __init__(self, board, current_piece):
        self.board = board
        self.current_piece = current_piece
        self.score = 0
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.font = pygame.font.SysFont("comicsansms", 30)
        self.bg_img = pygame.image.load("Images/bg_light.png")
        self.pause_screen_dark_image = pygame.image.load(
            "Images/pause_screen_dark.png"
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

        self.block_images = self._load_block_images()

        self.start_button_image = pygame.transform.scale(
            self.start_button_image,
            (STARTBUTTONWIDTH, STARTBUTTONHEIGHT),
        )
        self.start_button_coords = (
            (WINDOW_WIDTH // 2) - STARTBUTTONWIDTH // 2,
            2 * WINDOW_HEIGHT // 3 + STARTBUTTONHEIGHT // 2,
        )

        self.pause_button_image = pygame.transform.scale(
            self.pause_button_image,
            (PAUSEBUTTONWIDTH, PAUSEBUTTONHEIGHT),
        )
        self.pause_button_coords = (
            (WINDOW_WIDTH // 2) - PAUSEBUTTONWIDTH // 2,
            2 * WINDOW_HEIGHT // 3 + PAUSEBUTTONHEIGHT // 2,
        )
        self.continue_button_img = pygame.transform.scale(
            self.continue_button_img,
            (CONTINUEBUTTONWIDTH, CONTINUEBUTTONHEIGHT),
        )
        self.continue_button_coords = (
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
        self.exit_button_coords = (
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
        self.try_again_button_coords = (
            (WINDOW_WIDTH // 2) - TRYAGAINBUTTONWIDTH // 2,
            2 * WINDOW_HEIGHT // 3 + TRYAGAINBUTTONHEIGHT // 2,
        )

    def draw(self, current_piece, next_pieces, lightmode=True):
        if self.viewtype == ViewType.START:
            self.draw_start_screen(lightmode)
        elif self.viewtype == ViewType.GAME:
            self.draw_game(current_piece, next_pieces, lightmode)
        elif self.viewtype == ViewType.GAMEOVER:
            self.draw_game_over_screen(lightmode)
        elif self.viewtype == ViewType.PAUSE:
            self.draw_pause_screen(lightmode)

    def set_view_type(self, viewtype, lightmode):
        self.lightmode = lightmode
        self.viewtype = viewtype
        if viewtype == ViewType.START:
            if lightmode:
                self.bg_img = pygame.image.load("Images/bg_start_light.png")
            else:
                self.bg_img = pygame.image.load("Images/bg_start_dark.png")
            self.bg_img = pygame.transform.scale(
                self.bg_img, (WINDOW_WIDTH, WINDOW_HEIGHT)
            )
        elif viewtype == ViewType.GAME:
            if lightmode:
                self.bg_img = pygame.image.load("Images/bg_light.png")
            else:
                self.bg_img = pygame.image.load("Images/bg_night.png")
            self.bg_img = pygame.transform.scale(
                self.bg_img, (WINDOW_WIDTH, WINDOW_HEIGHT)
            )
        elif viewtype == ViewType.GAMEOVER:
            self.draw_game_over_screen(lightmode)
        elif viewtype == ViewType.PAUSE:
            self.draw_pause_screen(lightmode)
        self.current_view_type = viewtype

    def draw_game(self, current_piece, next_pieces, lightmode):
        self.screen.blit(self.bg_img, (0, 0))
        self.draw_screen()
        self.draw_grid()
        self.draw_current_piece(current_piece)
        self.draw_scoreboard()
        self.draw_pause_button()
        self.draw_next_piece(next_pieces)

    def draw_next_piece(self, next_pieces):
        for i in range(len(next_pieces.queue)):
            draw_piece = next_pieces.queue[i]
            self.draw_piece(draw_piece, i)

    def draw_piece(self, piece, i):
        cell_size = 15
        for block in piece.blocks:
            pygame.draw.rect(
                self.screen,
                piece.color,
                (
                    block.x + block.x * cell_size + WINDOW_WIDTH // 2 + 150,
                    block.get_y()
                    + block.get_y() * cell_size
                    + GAME_HEIGHT // 4
                    + i * 4 * cell_size,
                    cell_size,
                    cell_size,
                ),
            )

    def draw_game_over_screen(self, lightmode=True):
        if lightmode:
            self.bg_img = pygame.image.load("Images/game_over_light.png")
        else:
            self.bg_img = pygame.image.load("Images/game_over_dark.png")
        self.bg_img = pygame.transform.scale(
            self.bg_img, (WINDOW_WIDTH, WINDOW_HEIGHT)
        )
        self.draw_exit_game(lightmode)
        self.draw_try_again(lightmode)

    def draw_try_again(self, lightmode):
        if lightmode:
            self.screen.blit(
                self.try_again_img_light,
                self.try_again_button_coords,
            )
        else:
            self.screen.blit(
                self.try_again_img_dark,
                self.try_again_button_coords,
            )

    def draw_start_screen(self, lightmode):
        self.screen.blit(self.bg_img, (0, 0))
        self.draw_start_button()

    def draw_start_button(self):
        self.start_button_coords = (
            (WINDOW_WIDTH // 2) - STARTBUTTONWIDTH // 2,
            2 * WINDOW_HEIGHT // 3 + STARTBUTTONHEIGHT // 2,
        )
        self.screen.blit(
            self.start_button_image,
            self.start_button_coords,
        )

    def draw_pause_button(self):
        self.screen.blit(
            self.pause_button_image,
            self.pause_button_coords,
        )

    def draw_pause_screen(self, lightmode=True):
        self.draw_continue_game(lightmode)

    def draw_continue_game(self, lightmode=True):
        self.screen.blit(self.continue_button_img, self.continue_button_coords)

    def draw_exit_game(self, lightmode=True):
        if lightmode:
            self.screen.blit(self.exit_button_img_light, self.exit_button_coords)
        else:
            self.screen.blit(self.exit_button_img_dark, self.exit_button_coords)

    def draw_grid(self):
        x_offset = (WINDOW_WIDTH - GAME_WIDTH) // 2
        y_offset = 0
        grid = pygame.image.load("Images/bg_grid.png")
        grid = pygame.transform.scale(grid, (GAME_WIDTH, GAME_HEIGHT))
        self.screen.blit(grid, (x_offset, y_offset))
        for x in range(NBOXES_HORIZONTAL):
            for y in range(NBOXES_VERTICAL):
                if self.board[x][y] != 0:
                    color = self.board[x][y]
                    pos = (
                        x_offset + (MARGIN + BOX_WIDTH) * x + MARGIN,
                        y_offset + (MARGIN + BOX_HEIGHT) * y + MARGIN,
                    )
                    self.draw_block(color, pos)

    def draw_current_piece(self, current_piece):
        x_offset = (WINDOW_WIDTH - GAME_WIDTH) // 2
        y_offset = 0
        for block in current_piece.blocks:
            pos = (
                x_offset + (MARGIN + BOX_WIDTH) * block.x + MARGIN,
                y_offset + (MARGIN + BOX_HEIGHT) * block.y + MARGIN,
            )
            self.draw_block(current_piece.color, pos)

    def draw_block(self, color, pos):
        image = self.block_images.get(color, self._make_fallback_surface(color))
        image = pygame.transform.scale(image, (BOX_WIDTH, BOX_HEIGHT))
        SCREEN.blit(image, pos)

    @staticmethod
    def _make_fallback_surface(color):
        surface = pygame.Surface((BOX_WIDTH, BOX_HEIGHT))
        surface.fill(color)
        return surface

    def _load_block_images(self):
        color_files = {
            RED: "Images/blocks/redblock.jpg",
            BLUE: "Images/blocks/blueblock.jpg",
            GREEN: "Images/blocks/greenblock.jpg",
            PINK: "Images/blocks/pinkblock.jpg",
            YELLOW: "Images/blocks/yellowblock.jpg",
        }
        images = {}
        for color, path in color_files.items():
            try:
                images[color] = pygame.image.load(path)
            except (pygame.error, FileNotFoundError):
                images[color] = self._make_fallback_surface(color)
        # Auto-generate fallback surfaces for colors without image files
        for color in (ORANGE, PURPLE):
            if color not in images:
                images[color] = self._make_fallback_surface(color)
        return images

    def draw_screen(self):
        pygame.draw.rect(self.screen, WHITE, [0, 0, WINDOW_WIDTH, WINDOW_HEIGHT], 5)

    def draw_scoreboard(self):
        x_offset = 120
        y_offset = 120
        pygame.draw.rect(self.screen, WHITE, [0, 0, 50, WINDOW_HEIGHT], 5)
        font = pygame.font.SysFont("comicsansms", 16)
        text = font.render("{}".format(self.score), True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (SCOREBOARD_WIDTH, SCOREBOARD_HEIGHT)
        self.screen.blit(text, (x_offset, y_offset))

    def update_score(self, score):
        self.score = score

    def get_view_type(self):
        return self.viewtype

    def get_start_button_data(self):
        return self.start_button_coords, self.start_button_image.get_size()

    def get_pause_button_data(self):
        return self.pause_button_coords, self.pause_button_image.get_size()

    def get_continue_button_data(self):
        return self.continue_button_coords, self.continue_button_img.get_size()

    def get_exit_button_data(self):
        return self.exit_button_coords, self.exit_button_img_light.get_size()

    def get_try_again_button_data(self):
        return self.try_again_button_coords, self.try_again_img_light.get_size()
