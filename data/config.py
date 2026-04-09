# ---------------------------------------------------------------------------
# Grid & window
# ---------------------------------------------------------------------------
NBOXES_VERTICAL = 15
NBOXES_HORIZONTAL = 10
MARGIN = 0
BOX_HEIGHT = 25
BOX_WIDTH = 25
BOX_SIZE = BOX_HEIGHT

GAME_HEIGHT = (BOX_HEIGHT + MARGIN) * NBOXES_VERTICAL
GAME_WIDTH = (BOX_WIDTH + MARGIN) * NBOXES_HORIZONTAL
WINDOW_HEIGHT = GAME_HEIGHT + 100
WINDOW_WIDTH = GAME_WIDTH * 3
SCOREBOARD_WIDTH = GAME_WIDTH / 5
SCOREBOARD_HEIGHT = GAME_HEIGHT / 2

# ---------------------------------------------------------------------------
# Button sizes
# ---------------------------------------------------------------------------
STARTBUTTONWIDTH = 200
STARTBUTTONHEIGHT = 100
PAUSEBUTTONWIDTH = 100
PAUSEBUTTONHEIGHT = 100
CONTINUEBUTTONHEIGHT = 200
CONTINUEBUTTONWIDTH = 300
EXITBUTTONWIDTH = 200
EXITBUTTONHEIGHT = 100
TRYAGAINBUTTONWIDTH = 200
TRYAGAINBUTTONHEIGHT = 100

# ---------------------------------------------------------------------------
# Eye tracking thresholds
# ---------------------------------------------------------------------------
DEFAULT_BLINK_THRESHOLD = 6.0
DEFAULT_BLINK_DURATION = 1.0
DEFAULT_LEFT_GAZE_THRESHOLD = 3.0
DEFAULT_RIGHT_GAZE_THRESHOLD = 0.4
GAZE_COOLDOWN_FRAMES = 6      # replaces time.sleep(0.2) at 30 fps
BLINK_COOLDOWN_FRAMES = 30    # replaces time.sleep(1) at 30 fps

# ---------------------------------------------------------------------------
# Game timing
# ---------------------------------------------------------------------------
GAME_FPS = 30
PIECE_DROP_SPEED = 0.1
FAST_DROP_SPEED = 1.0
SCORE_PER_ROW = 10

# ---------------------------------------------------------------------------
# Display
# ---------------------------------------------------------------------------
NEXT_PIECE_CELL_SIZE = 15
FONT_NAME = "arial"
