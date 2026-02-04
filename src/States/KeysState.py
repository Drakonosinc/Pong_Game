from .State import State
from Utils.States import GameState
from Interface.Menus.Menu_Keys import KeysMenu
class KeysState(State):
    def __init__(self, game):
        super().__init__(game)
        self.menu = KeysMenu(self.game.ui)
    def enter(self, params=None):
        self.game.main = GameState.KEYS
        self.game.ui.setup_button_factories()
        self.menu.setup_buttons()
