from .State import State
from Utils.States import GameState
from Interface.Menus.Menu_AI import AIMenu
class AIMenuState(State):
    def __init__(self, game):
        super().__init__(game)
        self.menu = AIMenu(self.game.ui)
    def enter(self, params=None):
        self.game.main = GameState.AI_MENU
        self.game.ui.setup_button_factories()
        self.menu.setup_buttons()
    def exit(self): pass
