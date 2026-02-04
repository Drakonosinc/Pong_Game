from .State import State
from Utils.States import GameState
from Interface.Menus.Visuals_Menu import VisualsMenu
class VisualsState(State):
    def __init__(self, game):
        super().__init__(game)
        self.menu = VisualsMenu(self.game.ui)
    def enter(self, params=None):
        self.game.main = GameState.VISUALS
        self.game.ui.setup_button_factories()
        self.menu.setup_buttons()
    def exit(self): pass
