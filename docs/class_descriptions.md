## Class Descriptions

### TetrisController

`TetrisController` handles all user input: keyboard, mouse buttons, and optional eye-tracking via gaze and blink detection.

- `__init__(self, gamelogic, view)`: Initialise with references to `GameLogic` and `GameDisplay`. Attempts to set up eye tracking; falls back to keyboard-only on failure.
- `_init_gaze_tracking(self) -> bool`: Try to open the webcam and load the dlib model. Returns `False` if anything is unavailable.
- `cleanup(self)`: Release the camera if it was opened.
- `handle_event(self)`: Process one frame of input — gaze (with cooldown), keyboard, and mouse button clicks.
- `check_button_click(self, event, button, tipo)`: Hit-test a UI button and dispatch the appropriate action.
- `_check_gaze_direction(self) -> Direction`: Read a camera frame and return the detected gaze direction.
- `_get_gaze_ratio(self, eye_points, facial_landmarks) -> float`: Calculate the left/right white-pixel ratio for one eye.
- `_get_blinking_ratio(self, eye_points, facial_landmarks) -> float`: Calculate the horizontal/vertical line ratio to detect blinks.

### GameLogic

`GameLogic` owns all game state and orchestrates one frame of gameplay.

- `__init__(self, screen, clock)`: Receive the pygame `Surface` and `Clock` via dependency injection. Initialise audio, game state, and sub-objects.
- `play(self)`: Main game loop — handles events, processes movement, checks rows, and renders.
- `change_view_type(self, viewtype, lightmode)`: Switch the active view (START, GAME, PAUSE, GAMEOVER).
- `set_direction(self, direction)`: Set the pending movement direction (called by the controller).
- `set_paused(self, paused)`: Pause or unpause the game.
- `request_exit(self)`: Signal the game loop to stop.
- `reset_game(self)`: Reinitialise all state for a new game.
- `process_movement(self)`: Handle one frame of piece movement based on the current direction.
- `set_new_piece(self)`: Lock the current piece into the grid and spawn the next one.
- `check_for_full_rows(self)`: Clear completed rows and shift blocks down.
- `can_go_down / can_go_left / can_go_right / can_rotate`: Collision checks.

### PieceFactory

`PieceFactory` is a static factory for creating random `TetrisPiece` instances.

- `create_random() -> TetrisPiece`: Return a new random piece.

### TetrisPiece

`TetrisPiece` represents a four-block Tetris shape with a shared colour.

- `move_left / move_right / move_down(speed)`: Translate the piece.
- `rotate()`: Rotate 90 degrees clockwise around the centre.
- `get_lowest_height / get_most_left / get_most_right / get_most_top`: Boundary queries.

### Block

`Block` represents a single cell position.

- `go_down(speed) / go_left() / go_right()`: Move the cell.
- `get_y() -> int`: Return the y-coordinate rounded up.

### GameDisplay

`GameDisplay` handles all rendering of the Tetris UI.

- `__init__(self, board, current_piece, screen)`: Receive the grid, current piece, and injected `Surface`. Pre-load and cache all backgrounds, block images, and UI buttons.
- `draw(self, current_piece, next_pieces, lightmode)`: Render one frame based on the active view type.
- `set_view_type(self, viewtype, lightmode)`: Switch background and active view.
- `draw_game / draw_start_screen / draw_pause_screen / draw_game_over_screen`: View-specific rendering.
- `draw_grid()`: Render the grid background and all locked blocks.
- `draw_block(self, color, pos)`: Draw a single block using cached images with auto-generated fallbacks.
- `update_score(self, score)`: Update the displayed score.
- `get_view_type()`: Return the current `ViewType`.
- `get_*_button_data()`: Return `(coords, size)` tuples for hit-testing.

### UIButton

`UIButton` is a dataclass for themed buttons with light/dark images.

- `draw(self, screen, light_mode)`: Blit the appropriate theme image.
- `get_data()`: Return `(coords, size)` for hit-testing.
