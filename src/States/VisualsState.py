from .State import State
from Utils.States import GameState
from Interface.Menus.Visuals_Menu import VisualsMenu
class VisualsState(State):
    def __init__(self, game):
        super().__init__(game)
        self.menu = VisualsMenu(self.game.ui)
    def enter(self, params=None):
        self.game.main = GameState.VISUALS
        self.game.ui.main = GameState.VISUALS
        self.game.ui.setup_button_factories()
        self.menu.setup_buttons()
    def exit(self): pass
    def update(self, dt):
        ui_main = getattr(self.game.ui, 'main', None)
        if ui_main == GameState.OPTIONS: self.game.state_manager.change_state(GameState.OPTIONS)
    def draw(self, surface):
        self.game.visuals_items.draw()
        self.menu.render()
    def handle_event(self, event):
        if self.game.main == GameState.VISUALS:  self.game.events_buttons(event)