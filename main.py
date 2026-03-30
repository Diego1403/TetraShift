from __future__ import annotations

import pygame

from data.config import WINDOW_WIDTH, WINDOW_HEIGHT
from model.game_logic import GameLogic


def main() -> None:
    """Entry point — initialise pygame, create game, and run."""
    pygame.init()
    screen: pygame.Surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock: pygame.time.Clock = pygame.time.Clock()

    gamelogic = GameLogic(screen, clock)
    gamelogic.play()

    pygame.quit()


if __name__ == "__main__":
    main()
