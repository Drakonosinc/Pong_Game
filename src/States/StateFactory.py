from Utils.States import GameState
from .MenuState import MenuState
from .PlayingState import PlayingState
from .GameOverState import GameOverState
from .ModeSelectState import ModeSelectState
from .PauseState import PauseState
from .OptionsState import OptionsState
from .VisualsState import VisualsState
from .KeysState import KeysState
from .AIMenuState import AIMenuState
class StateFactory:
    def __init__(self, game):
        self.game = game
        self.state_map = {
            GameState.MENU: MenuState,
            GameState.PLAYING: PlayingState,
            GameState.GAME_OVER: GameOverState,
            GameState.MODE_SELECT: ModeSelectState,
            GameState.PAUSE: PauseState,
            GameState.OPTIONS: OptionsState,
            GameState.VISUALS: VisualsState,
            GameState.KEYS: KeysState,
            GameState.AI_MENU: AIMenuState}
    def get_state(self, state_enum):
        if state_enum in self.state_map: return self.state_map[state_enum](self.game)
        return None