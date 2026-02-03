from .State import State
from Utils.States import GameState
from Interface.Menus.Options_Menu import OptionsMenu
class OptionsState(State):
    def __init__(self, game):
        super().__init__(game)
        self.menu = OptionsMenu(self.game.ui)
    def enter(self, params=None):
        self.game.main = GameState.OPTIONS
        self.game.ui.setup_button_factories()
        self.menu.setup_buttons()
    def exit(self): pass
    def update(self, dt): pass
    def draw(self, surface):
        self.game.visuals_items.draw()
        self.menu.render()
    def handle_event(self, event):
        if self.game.main == GameState.OPTIONS: self.game.events_buttons(event)