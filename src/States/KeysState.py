from .State import State
from Utils.States import GameState
from Interface.Menus.Menu_Keys import KeysMenu
class KeysState(State):
    def __init__(self, game):
        super().__init__(game)
        self.menu = KeysMenu(self.game.ui)
