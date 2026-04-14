# TetraShift

**A Tetris game with eye-tracking controls** built with Pygame, OpenCV, and dlib.

Move pieces with your gaze, rotate them with a blink, or fall back to the keyboard — your choice.

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)


## Features

- **Gaze detection** — look left or right to move the active piece
- **Blink detection** — close both eyes to rotate
- **Keyboard controls** — arrow keys work as a traditional fallback
- **Light / dark theme** — toggle at the start screen
- **Graceful fallback** — if no webcam or model file is found, the game runs keyboard-only
- **Next-piece queue** — see the upcoming 5 pieces

## Architecture

TetraShift follows an **MVC** pattern:

| Layer | Module | Responsibility |
|-------|--------|----------------|
| **Model** | `model/block.py` | Single grid cell |
| | `model/tetris_piece.py` | Four-block piece with movement & rotation |
| | `model/piece_factory.py` | Random piece generation |
| | `model/game_logic.py` | Game state, collision detection, row clearing |
| **View** | `view/game_display.py` | All rendering (grid, pieces, screens, buttons) |
| | `view/ui_button.py` | Reusable themed button dataclass |
| **Controller** | `controller/tetris_controller.py` | Keyboard, mouse, and eye-tracking input |
| **Data** | `data/colors.py` | Typed color constants |
| | `data/enums.py` | `ViewType` and `Direction` enums |
| | `data/config.py` | All game configuration (no pygame calls) |

## Prerequisites

- Python 3.10+
- A webcam (optional — for eye tracking)
- `shape_predictor_68_face_landmarks.dat` (optional — for eye tracking)

## Installation

```bash
# Clone the repository
git clone https://github.com/Diego1403/TetraShift.git
cd TetraShift

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
```

### Eye-tracking setup (optional)

Download the dlib facial landmark model:

1. Get `shape_predictor_68_face_landmarks.dat.bz2` from
   <http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2>
2. Extract and place `shape_predictor_68_face_landmarks.dat` in the project root

If the file is missing or the webcam is unavailable, the game will automatically
run in keyboard-only mode.

## Usage

```bash
python main.py
```

### Controls

| Input | Action |
|-------|--------|
| Left arrow / look left | Move piece left |
| Right arrow / look right | Move piece right |
| Up arrow / blink (hold) | Rotate piece |
| Down arrow | Fast drop |

### Game states

**START** → click Start → **GAME** → click Pause → **PAUSE** → Continue or Exit
**GAME** → top out → **GAMEOVER** → Try Again or Exit

## Configuration

All tunable values live in `data/config.py`:

- Grid dimensions, box sizes, window layout
- Eye-tracking thresholds (`DEFAULT_BLINK_THRESHOLD`, gaze ratios)
- Game timing (`GAME_FPS`, `PIECE_DROP_SPEED`, `SCORE_PER_ROW`)
- Cooldown frames for gaze and blink actions

## Project Structure

```
TetraShift/
├── main.py                    # Entry point with DI
├── pyproject.toml             # Modern Python packaging config
├── requirements.txt           # Pip dependencies
├── data/
│   ├── colors.py              # Color constants
│   ├── enums.py               # ViewType, Direction
│   └── config.py              # All configuration
├── model/
│   ├── block.py               # Block class
│   ├── tetris_piece.py        # TetrisPiece class
│   ├── piece_factory.py       # PieceFactory
│   └── game_logic.py          # GameLogic (core state)
├── view/
│   ├── game_display.py        # GameDisplay (rendering)
│   └── ui_button.py           # UIButton dataclass
├── controller/
│   └── tetris_controller.py   # TetrisController (input)
├── Images/                    # UI and block images
├── audio/                     # Sound effects and music
├── docs/                      # Additional documentation
└── LICENSE                    # Apache 2.0
```

## License

This project is licensed under the [Apache License 2.0](LICENSE).

## Acknowledgments

- Inspired by [Pawan Jain's eye tracking lectures](https://www.youtube.com/playlist?list=PL6Yc5OUgcoTlvHb5OfFLUJ90ofBuoU5g8)
- Built with [Pygame](https://www.pygame.org/), [OpenCV](https://opencv.org/), and [dlib](http://dlib.net/)
