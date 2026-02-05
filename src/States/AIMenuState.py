from .State import State
from Utils.States import GameState
from Interface.Menus.Menu_AI import AIMenu
class AIMenuState(State):
    def __init__(self, game):
        super().__init__(game)
        self.menu = AIMenu(self.game.ui)
