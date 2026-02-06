from .State import State
from Utils.States import GameState
from Interface.Menus.Menu_AI import AIMenu
from .ModeSelectState import ModeSelectState
class AIMenuState(State):
    def __init__(self, game):
        super().__init__(game)
        self.menu = AIMenu(self.game.ui)
    def enter(self, params=None):
        self.game.main = GameState.AI_MENU
        self.game.ui.main = GameState.AI_MENU
        self.game.ui.setup_button_factories()
        self.menu.setup_buttons()
    def exit(self): pass
    def update(self, dt):
        ui_main = getattr(self.game.ui, 'main', None)
        if ui_main == GameState.MODE_SELECT: self.game.state_manager.change(ModeSelectState(self.game))
    def draw(self, surface):
        self.game.visuals_items.draw()
        self.menu.render()
    def handle_event(self, event):
        if self.game.main == GameState.AI_MENU: self.game.events_buttons(event)