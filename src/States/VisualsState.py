from .State import State
from Utils.States import GameState
class VisualsState(State):
    def enter(self, params=None):
        self.game.main = GameState.VISUALS
