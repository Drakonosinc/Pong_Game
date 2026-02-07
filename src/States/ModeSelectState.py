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
    def enter(self, params=None):
        self.game.main = GameState.MODE_SELECT
        self.game.ui.main = GameState.MODE_SELECT
        self.game.ui.setup_button_factories()
        self.menu.setup_buttons()
    def exit(self): pass
    def update(self, dt):
        ui_main = getattr(self.game.ui, 'main', None)
        if ui_main == GameState.PLAYING: self.game.state_manager.change(PlayingState(self.game))
        elif ui_main == GameState.AI_MENU: self.game.state_manager.change(AIMenuState(self.game))
        elif ui_main == GameState.MENU: self.game.state_manager.change(MenuState(self.game))
    def draw(self, surface):
        self.game.visuals_items.draw()
        self.menu.render()
