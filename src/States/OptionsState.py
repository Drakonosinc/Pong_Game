from .State import State
from Utils.States import GameState
class OptionsState(State):
    def enter(self, params=None):
        self.game.main = GameState.OPTIONS
    def exit(self): pass
