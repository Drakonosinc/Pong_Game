from enum import Enum
class GameState(Enum):
    MENU = 0
    PLAYING = -1
    GAME_OVER = 1
    MODE_SELECT = 2
    PAUSE = 3
    OPTIONS = 4
    VISUALS = 5
    KEYS = 6