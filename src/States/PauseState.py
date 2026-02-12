from .State import State
from Utils.States import GameState
from Interface.Menus.Pause import Pause
class PauseState(State):
    def __init__(self, game):
        super().__init__(game)
        self.menu = Pause(self.game.ui)
