from .State import State
from Utils.States import GameState
from Interface.Menus.Options_Menu import OptionsMenu
from .VisualsState import VisualsState
from .KeysState import KeysState
from .MenuState import MenuState
class OptionsState(State):
    def __init__(self, game):
        super().__init__(game)
        self.menu = OptionsMenu(self.game.ui)
