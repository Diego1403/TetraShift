import pygame
from model.game_logic import GameLogic


def main():
    pygame.init()
    screen = pygame.display.set_mode(
        (pygame.display.Info().current_w, pygame.display.Info().current_h)
    )
    clock = pygame.time.Clock()

    from data.config import WINDOW_WIDTH, WINDOW_HEIGHT

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    gamelogic = GameLogic(screen, clock)
    gamelogic.play()

    pygame.quit()


if __name__ == "__main__":
    main()
