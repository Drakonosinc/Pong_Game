from .State import State
from Utils.States import GameState
class AIMenuState(State):
    def enter(self, params=None):
        self.game.main = GameState.AI_MENU
