import pygame

from data.colors import *  # noqa: F401,F403
from data.enums import *  # noqa: F401,F403
from data.config import *  # noqa: F401,F403

# TODO: SCREEN and CLOCK will be injected via DI in Commit 5.
# Kept here temporarily so the game runs between commits.
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  # type: ignore[name-defined]
GRID_SURFACE = pygame.Surface((GAME_HEIGHT, GAME_WIDTH))  # type: ignore[name-defined]
CLOCK = pygame.time.Clock()
pygame.font.init()
