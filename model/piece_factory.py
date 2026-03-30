from __future__ import annotations

import random
import copy

from model.block import Block
from model.tetris_piece import TetrisPiece
from data.colors import Color, BLUE, YELLOW, PINK, GREEN, ORANGE, RED


class PieceFactory:
    """Factory for creating random Tetris pieces."""

    @staticmethod
    def create_random() -> TetrisPiece:
        """Return a new random TetrisPiece."""
        items = PieceFactory._get_piece_definitions()
        selected = random.choice(list(items.values()))
        blocks: list[Block] = copy.deepcopy(selected[0])
        color: Color = copy.deepcopy(selected[1])
        return TetrisPiece(blocks, color)

    @staticmethod
    def _get_piece_definitions() -> dict[str, list[list[Block] | Color]]:
        return {
            "I": [[Block(7, 0), Block(6, 0), Block(5, 0), Block(4, 0)], BLUE],
            "Z": [[Block(5, 0), Block(6, 0), Block(6, 1), Block(7, 1)], YELLOW],
            "O": [[Block(6, 0), Block(5, 0), Block(5, 1), Block(4, 1)], PINK],
            "J": [[Block(5, 0), Block(6, 0), Block(5, 1), Block(6, 1)], GREEN],
            "L": [[Block(5, 0), Block(6, 0), Block(7, 0), Block(5, 1)], BLUE],
            "T": [[Block(5, 0), Block(6, 0), Block(7, 0), Block(6, 1)], ORANGE],
            "S": [[Block(5, 0), Block(6, 1), Block(6, 0), Block(7, 1)], RED],
        }
