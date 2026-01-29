from .State import State
from Utils.States import GameState
class KeysState(State):
    def enter(self, params=None):
        self.game.main = GameState.KEYS
