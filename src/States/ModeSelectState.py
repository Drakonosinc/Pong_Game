from .State import State
from Utils.States import GameState
from Interface.Menus.Game_Mode import GameMode
from .PlayingState import PlayingState
from .AIMenuState import AIMenuState
from .MenuState import MenuState
class ModeSelectState(State):
    def __init__(self, game):
        super().__init__(game)
        self.menu = GameMode(self.game.ui)
