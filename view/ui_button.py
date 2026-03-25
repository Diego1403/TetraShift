from dataclasses import dataclass

import pygame


@dataclass
class UIButton:
    image_light: pygame.Surface
    image_dark: pygame.Surface | None
    coords: tuple[int, int]
    size: tuple[int, int]

    def draw(self, screen, light_mode):
        if light_mode or self.image_dark is None:
            screen.blit(self.image_light, self.coords)
        else:
            screen.blit(self.image_dark, self.coords)

    def get_data(self):
        return self.coords, self.size
