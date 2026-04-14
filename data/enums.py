from enum import Enum


class ViewType(Enum):
    GAME = "0"
    PAUSE = "1"
    GAMEOVER = "2"
    START = "3"


class Direction(Enum):
    UP = "2"
    DOWN = "0"
    LEFT = "-1"
    RIGHT = "1"
    ROTATE = "3"
    NONE = "4"
