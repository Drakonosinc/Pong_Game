from enum import Enum
class GameState(Enum):
    MENU = 0
    PLAYING = -1
    GAME_OVER = 1
    MODE_SELECT = 2
    