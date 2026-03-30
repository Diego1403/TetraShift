from __future__ import annotations

import math


class Block:
    """Represents a single cell in a Tetris piece."""

    def __init__(self, x: int | float, y: int | float) -> None:
        self.x: int = math.ceil(x)
        self.y: int | float = math.ceil(y)

    def go_down(self, speed: float = 0.1) -> None:
        """Move the block down by *speed* rows."""
        self.y = self.y + speed

    def go_left(self) -> None:
        self.x = self.x - 1

    def go_right(self) -> None:
        self.x = self.x + 1

    def get_y(self) -> int:
        """Return the y-coordinate rounded up to the nearest integer."""
        return math.ceil(self.y)
