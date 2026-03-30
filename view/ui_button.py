from __future__ import annotations

from dataclasses import dataclass

import pygame


@dataclass
class UIButton:
    """A UI button with optional light/dark theme images."""

    image_light: pygame.Surface
    image_dark: pygame.Surface | None
    coords: tuple[int, int]
    size: tuple[int, int]

    def draw(self, screen: pygame.Surface, light_mode: bool) -> None:
        """Blit the appropriate theme image onto *screen*."""
        if light_mode or self.image_dark is None:
            screen.blit(self.image_light, self.coords)
        else:
            screen.blit(self.image_dark, self.coords)

    def get_data(self) -> tuple[tuple[int, int], tuple[int, int]]:
        """Return (coords, size) for hit-testing."""
        return self.coords, self.size
