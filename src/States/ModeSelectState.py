from .State import State
from Utils.States import GameState
class ModeSelectState(State):
    def enter(self, params=None):
        self.game.main = GameState.MODE_SELECT
    def exit(self): pass
