from __future__ import annotations

import queue
from typing import Literal

import pygame

from model.block import Block
from model.tetris_piece import TetrisPiece
from model.piece_factory import PieceFactory
from view.game_display import GameDisplay
from controller.tetris_controller import TetrisController
from data.colors import Color, BLACK
from data.enums import ViewType, Direction
from data.config import (
    NBOXES_HORIZONTAL, NBOXES_VERTICAL, GAME_FPS,
    PIECE_DROP_SPEED, FAST_DROP_SPEED, SCORE_PER_ROW,
)

CellValue = Color | Literal[0]
Grid = list[list[CellValue]]


class GameLogic:
    """Core game state and logic for Tetris."""

    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock) -> None:
        self.screen: pygame.Surface = screen
        self.clock: pygame.time.Clock = clock

        pygame.mixer.init()

        self.score: int = 0
        self.grid: Grid = []
        self.exit_game: bool = False
        self.pause: bool = False
        self.dir: Direction = Direction.NONE
        self.light_mode: bool = True
        self.current_view_type: ViewType = ViewType.START

        self.reset_game()
        self.full_row_sound: pygame.mixer.Sound = pygame.mixer.Sound("audio/full_row.mp3")
        self.gameover_sound: pygame.mixer.Sound = pygame.mixer.Sound("audio/game_over.mp3")
        pygame.mixer.music.load("audio/music.mp3")
        self.change_view_type(ViewType.START, self.light_mode)

        self.screen.fill(BLACK)

    def handle_event(self) -> None:
        self.controller.handle_event()

    def change_view_type(self, viewtype: ViewType, lightmode: bool) -> None:
        self.current_view_type = viewtype
        self.light_mode = lightmode
        self.view.set_view_type(self.current_view_type, self.light_mode)

    def set_direction(self, direction: Direction) -> None:
        """Set the current movement direction."""
        self.dir = direction

    def set_paused(self, paused: bool) -> None:
        """Pause or unpause the game."""
        self.pause = paused

    def request_exit(self) -> None:
        """Request the game loop to exit."""
        self.exit_game = True

    def play(self) -> None:
        """Run the main game loop."""
        pygame.mixer.music.play(-1)
        while not self.exit_game:
            self.handle_event()
            if self.current_view_type == ViewType.GAME and not self.pause:
                pygame.mixer.music.unpause()
                self.process_movement()
                self.check_game_events()
            else:
                pygame.mixer.music.pause()
            self.clock.tick(GAME_FPS)
            self.view.draw(self.current_piece, self.next_pieces, self.light_mode)
            pygame.display.update()
            pygame.display.flip()

    def check_game_events(self) -> None:
        self.check_for_full_rows()
        self.view.update_score(self.score)

    def clear_last_pos(self) -> None:
        """Erase the current piece from the grid."""
        blocks = self.current_piece.blocks
        for pos in blocks:
            if pos.get_y() < NBOXES_VERTICAL:
                self.grid[pos.x][pos.get_y()] = 0

    def can_go_down(self, blocks: list[Block]) -> bool:
        lowest_y = self.current_piece.get_lowest_height()
        can_go = True
        if lowest_y >= NBOXES_VERTICAL - 1:
            can_go = False
            self.set_new_piece()
        else:
            for pos in blocks:
                if pos.get_y() < NBOXES_VERTICAL - 1:
                    if self.grid[pos.x][pos.get_y() + 1] != 0:
                        can_go = False
                        self.set_new_piece()
                        break
        return can_go

    def reset_game(self) -> None:
        """Reset all game state for a new game."""
        self.score = 0
        self.grid = []
        self.exit_game = False
        self.pause = False
        self.dir = Direction.NONE
        self.light_mode = True

        for x in range(NBOXES_HORIZONTAL):
            self.grid.append([])
            for y in range(NBOXES_VERTICAL):
                self.grid[x].append(0)

        self.next_pieces: queue.Queue[TetrisPiece] = queue.Queue(5)
        for _ in range(5):
            self.next_pieces.put(PieceFactory.create_random())

        new = self.next_pieces.get()
        self.current_piece: TetrisPiece = TetrisPiece(new.blocks, new.color)
        self.view: GameDisplay = GameDisplay(self.grid, self.current_piece, self.screen)
        self.controller: TetrisController = TetrisController(self, self.view)
        self.dir = Direction.NONE
        self.change_view_type(ViewType.GAME, self.light_mode)
        self.screen.fill(BLACK)

    def can_go_left(self, blocks: list[Block]) -> bool:
        most_left = self.current_piece.get_most_left()
        can_go = True
        if most_left <= 0:
            return False
        else:
            for pos in blocks:
                if pos.x > 0:
                    if self.grid[pos.x - 1][pos.get_y()] != 0:
                        can_go = False
                        break
        return can_go

    def can_go_right(self, blocks: list[Block]) -> bool:
        most_right = self.current_piece.get_most_right()
        can_go = True
        if most_right >= NBOXES_HORIZONTAL - 1:
            return False
        else:
            for pos in blocks:
                if pos.x < NBOXES_HORIZONTAL - 1:
                    if self.grid[pos.x + 1][pos.get_y()] != 0:
                        can_go = False
                        break
        return can_go

    def can_rotate(self, blocks: list[Block]) -> bool:
        can_rot = True
        for pos in blocks:
            if pos.x < 0 or pos.x > NBOXES_HORIZONTAL - 1:
                can_rot = False
                break
            if pos.get_y() > NBOXES_VERTICAL - 1:
                can_rot = False
                break
            if self.grid[pos.x][pos.get_y()] != 0:
                can_rot = False
                break
            if pos.get_y() < 4:
                can_rot = False
                break
        return can_rot

    def process_movement(self) -> None:
        """Handle one frame of piece movement based on the current direction."""
        self.clear_last_pos()
        blocks = self.current_piece.blocks
        if self.can_go_down(blocks):
            self.current_piece.move_down(PIECE_DROP_SPEED)
        if self.dir == Direction.DOWN:
            if self.can_go_down(blocks):
                self.current_piece.move_down(FAST_DROP_SPEED)
                self.dir = Direction.NONE
            else:
                self.set_new_piece()
        if self.dir == Direction.LEFT:
            if self.can_go_left(blocks):
                self.current_piece.move_left()
                self.dir = Direction.NONE

        if self.dir == Direction.RIGHT:
            if self.can_go_right(blocks):
                self.current_piece.move_right()
                self.dir = Direction.NONE

        if self.dir == Direction.ROTATE:
            if self.can_rotate(self.current_piece.blocks):
                self.clear_last_pos()
                if self.can_go_down(self.current_piece.blocks):
                    self.current_piece.rotate()
                    self.current_piece.move_down()
            self.dir = Direction.NONE

    def set_new_piece(self) -> None:
        """Lock the current piece and spawn a new one."""
        if self.current_piece.get_most_top() == 0:
            self.pause = True
            self.change_view_type(ViewType.GAMEOVER, self.light_mode)
            self.gameover_sound.play()

        for pos in self.current_piece.blocks:
            self.grid[pos.x][pos.get_y()] = self.current_piece.color
        del self.current_piece

        self.next_pieces.put(PieceFactory.create_random())
        new_piece = self.next_pieces.get()
        self.current_piece = TetrisPiece(new_piece.blocks, new_piece.color)

    def check_for_full_rows(self) -> None:
        """Clear completed rows and shift blocks down."""
        rows_to_delete: list[int] = []
        for y in range(NBOXES_VERTICAL):
            row_complete = True
            for x in range(NBOXES_HORIZONTAL):
                if self.grid[x][y] == 0:
                    row_complete = False
                    break
            if row_complete:
                self.full_row_sound.play()
                rows_to_delete.append(y)
                self.score += SCORE_PER_ROW

        for y in rows_to_delete:
            for x in range(NBOXES_HORIZONTAL):
                for i in range(y, 0, -1):
                    self.grid[x][i] = self.grid[x][i - 1]
            for x in range(NBOXES_HORIZONTAL):
                self.grid[x][0] = 0
