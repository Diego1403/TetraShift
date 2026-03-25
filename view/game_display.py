import pygame

from data.colors import (
    WHITE, RED, BLUE, GREEN, YELLOW, PINK, PURPLE, ORANGE,
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
from view.ui_button import UIButton


class GameDisplay:
    def __init__(self, board, current_piece, screen):
        self.board = board
        self.current_piece = current_piece
        self.score = 0
        self.screen = screen
        self.font = pygame.font.SysFont("comicsansms", 30)
        self.viewtype = ViewType.START

        # Cache backgrounds
        self._bg_cache = self._load_backgrounds()
        self.bg_img = self._bg_cache[("start", True)]

        # Cache grid image
        self._grid_img = pygame.image.load("Images/bg_grid.png")
        self._grid_img = pygame.transform.scale(self._grid_img, (GAME_WIDTH, GAME_HEIGHT))

        # Cache block images
        self.block_images = self._load_block_images()

        # Build UIButton instances
        self.start_button = self._make_button(
            "Images/start_button.png", None,
            (STARTBUTTONWIDTH, STARTBUTTONHEIGHT),
            ((WINDOW_WIDTH // 2) - STARTBUTTONWIDTH // 2,
             2 * WINDOW_HEIGHT // 3 + STARTBUTTONHEIGHT // 2),
        )
        self.pause_button = self._make_button(
            "Images/pause_button.png", None,
            (PAUSEBUTTONWIDTH, PAUSEBUTTONHEIGHT),
            ((WINDOW_WIDTH // 2) - PAUSEBUTTONWIDTH // 2,
             2 * WINDOW_HEIGHT // 3 + PAUSEBUTTONHEIGHT // 2),
        )
        self.continue_button = self._make_button(
            "Images/continueGame_button.png", None,
            (CONTINUEBUTTONWIDTH, CONTINUEBUTTONHEIGHT),
            ((WINDOW_WIDTH // 2) - CONTINUEBUTTONWIDTH // 2,
             WINDOW_HEIGHT // 3 - CONTINUEBUTTONHEIGHT // 2),
        )
        self.exit_button = self._make_button(
            "Images/exitGame_button_light.png",
            "Images/exitGame_button_dark.png",
            (EXITBUTTONWIDTH, EXITBUTTONHEIGHT),
            ((WINDOW_WIDTH // 2) - EXITBUTTONWIDTH // 2,
             (WINDOW_HEIGHT // 3) - EXITBUTTONHEIGHT // 2 + 100),
        )
        self.try_again_button = self._make_button(
            "Images/try_again_button_light.png",
            "Images/try_again_button_dark.png",
            (TRYAGAINBUTTONWIDTH, TRYAGAINBUTTONHEIGHT),
            ((WINDOW_WIDTH // 2) - TRYAGAINBUTTONWIDTH // 2,
             2 * WINDOW_HEIGHT // 3 + TRYAGAINBUTTONHEIGHT // 2),
        )

    @staticmethod
    def _make_button(light_path, dark_path, size, coords):
        light_img = pygame.transform.scale(
            pygame.image.load(light_path), size
        )
        dark_img = None
        if dark_path:
            dark_img = pygame.transform.scale(
                pygame.image.load(dark_path), size
            )
        return UIButton(
            image_light=light_img,
            image_dark=dark_img,
            coords=coords,
            size=size,
        )

    def _load_backgrounds(self):
        def _load_scaled(path):
            img = pygame.image.load(path)
            return pygame.transform.scale(img, (WINDOW_WIDTH, WINDOW_HEIGHT))

        return {
            ("start", True): _load_scaled("Images/bg_start_light.png"),
            ("start", False): _load_scaled("Images/bg_start_dark.png"),
            ("game", True): _load_scaled("Images/bg_light.png"),
            ("game", False): _load_scaled("Images/bg_night.png"),
            ("gameover", True): _load_scaled("Images/game_over_light.png"),
            ("gameover", False): _load_scaled("Images/game_over_dark.png"),
        }

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
            self.bg_img = self._bg_cache[("start", lightmode)]
        elif viewtype == ViewType.GAME:
            self.bg_img = self._bg_cache[("game", lightmode)]
        elif viewtype == ViewType.GAMEOVER:
            self.bg_img = self._bg_cache[("gameover", lightmode)]
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
        self.pause_button.draw(self.screen, lightmode)
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
        self.bg_img = self._bg_cache[("gameover", lightmode)]
        self.exit_button.draw(self.screen, lightmode)
        self.try_again_button.draw(self.screen, lightmode)

    def draw_start_screen(self, lightmode):
        self.screen.blit(self.bg_img, (0, 0))
        self.start_button.draw(self.screen, lightmode)

    def draw_pause_screen(self, lightmode=True):
        self.continue_button.draw(self.screen, lightmode)

    def draw_grid(self):
        x_offset = (WINDOW_WIDTH - GAME_WIDTH) // 2
        y_offset = 0
        self.screen.blit(self._grid_img, (x_offset, y_offset))
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
        self.screen.blit(image, pos)

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
        return self.start_button.get_data()

    def get_pause_button_data(self):
        return self.pause_button.get_data()

    def get_continue_button_data(self):
        return self.continue_button.get_data()

    def get_exit_button_data(self):
        return self.exit_button.get_data()

    def get_try_again_button_data(self):
        return self.try_again_button.get_data()
