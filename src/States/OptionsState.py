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
    def enter(self, params=None):
        self.game.main = GameState.OPTIONS
        self.game.ui.main = GameState.OPTIONS
        self.game.ui.setup_button_factories()
        self.menu.setup_buttons()
    def exit(self): pass
    def update(self, dt):
        ui_main = getattr(self.game.ui, 'main', None)
        if ui_main == GameState.VISUALS: self.game.state_manager.change(VisualsState(self.game))
        elif ui_main == GameState.KEYS: self.game.state_manager.change(KeysState(self.game))
        elif ui_main == GameState.MENU: self.game.state_manager.change(MenuState(self.game))
    def draw(self, surface):
        self.game.visuals_items.draw()
        self.menu.render()
    def handle_event(self, event):
