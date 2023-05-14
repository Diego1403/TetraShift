## Class Descriptions

### TetrisController

`TetrisController` is the main class responsible for handling input from the user, both from the keyboard and through gaze and blink detection. It includes the following methods:

- `__init__(self, gamelogic, view)`: Initializes the TetrisController with the given gamelogic and view objects. Also sets up gaze tracking and blink detection.
- `init_gaze_tracking(self)`: Initializes gaze tracking by setting up the necessary objects and models.
- `handle_event(self)`: Handles user input events, such as gaze direction, blinks, and keyboard inputs.
- `check_button(self, event, Button, tipo)`: Checks if a button in the game's user interface has been clicked and performs the corresponding action.
- `check_gaze_direction(self)`: Determines the user's gaze direction and returns the corresponding movement direction.
- `get_gaze_ratio(self, eye_points, facial_landmarks)`: Calculates the gaze ratio for the specified eye points.
- `midpoint(self, p1, p2)`: Calculates the midpoint between two points.
- `hypot(self, x, y)`: Calculates the distance between two points.
- `get_blinking_ratio(self, eye_points, facial_landmarks)`: Calculates the blinking ratio for the specified eye points.

### Gamelogic

The `Gamelogic` class is the centerpiece of the TetraShift game. It is responsible for handling the logic and state of the game, including moving pieces, checking for game events like completed lines, and managing the game state such as the score and the grid. Here's a breakdown of the main functions and their roles:

- `__init__(self)`: The constructor of the class, which initializes and sets up the game. It sets up the pygame mixer for sound effects and music, calls `reset_game()` to initialize the game state, and then sets up the display and controller for the game.
- `handle_event(self)`: This function delegates the handling of events to the controller.
- `changeViewType(self, viewtype, lightmode)`: Changes the view type based on the provided `viewtype` and `lightmode` parameters. It also updates the game's current view type and light mode.
- `play(self)`: The main game loop. It handles events, checks for game events, and updates the display, while the game is not set to exit.
- `check_events(self)`: Checks for game events, such as completed lines, and updates the score.
- `clearLastPos(self)`: This method clears the last position of the current piece on the grid.
- `can_go_down(self, blocks)`, `can_go_left(self, blocks)`, `can_go_right(self, blocks)`, `can_rotate(self, blocks)`: These functions check if the current piece can move down, left, right or be rotated, respectively, based on the current state of the grid and the blocks of the piece.
- `reset_game(self)`: Resets the game state. This includes the score, the game grid, and the state variables like `exitGame` and `pause`. It also initializes the queue of next pieces and sets the current piece.
- `move_events(self)`: Handles the movement of the current piece based on the user's input and the game state. It clears the last position of the piece
- `setNewPiece(self)`: Replaces the current piece with a new one from the queue of next pieces. If the new piece cannot be placed on the grid (because it overlaps with existing blocks), the game is set to pause and the game over view is displayed.
- `checkForFullRows(self)`: Checks for completed rows on the grid. If a row is complete, it is removed from the grid, and the rows above it are moved down. The score is also updated.

### GameDisplay

The `GameDisplay` class defines the game display or user interface of the game. Here's an overview of the various components:

- \***\*init**(self, board, currentPiece):\*\* The constructor for the `GameDisplay` class. The `board` and `currentPiece` parameters are the game board and the current game piece being manipulated by the player. It also initializes various other attributes such as the game's display, score, and images to be used in the display.-
- **draw(self, currentPiece, nextPieces, lightmode=True):** This method draws the game on the screen depending on the current state of the game (e.g. start, during the game, game over, pause). It calls appropriate draw methods based on the `viewtype`.-
- **setViewType(self, viewtype, lightmode):** This method is used to set the current state of the game view.-
- **drawGame(self, currentPiece, nextPieces, lightmode):** This method draws the game screen when the game is in progress. It includes the game screen, grid, current piece, scoreboard, pause button, and the next piece.-
- **drawGameOverScreen(self, lightmode=True):** This method is called when the game is over. It loads and displays the game over screen, the 'try again' button, and the 'exit game' button.-
- **drawStartScreen(self, lightmode):** This method is used to draw the start screen when the game is first opened.-
- **drawPauseScreen(self, lightmode=True):** This method is used to draw the pause screen when the game is paused.-
- **drawBlock(self, color, pos):** This method is used to draw a block of a particular color at a particular position on the game board.-
- **drawScoreboard(self):** This method is used to draw the scoreboard on the screen.-
- **updateScore(self, score):** This method is used to update the score of the game.-
- **get_ViewType(self):** This method returns the current view type of the game.-
- The remaining `get_` methods are used to get the positions and sizes of the various buttons used in the game.

In addition, this class also loads images and transforms them to the appropriate sizes for use in the game. These images are used for different blocks, buttons, and backgrounds in the game.
