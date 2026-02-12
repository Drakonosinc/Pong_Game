from .State import State
from Utils.States import GameState
from Interface.Menus.Pause import Pause
class PauseState(State):
    def __init__(self, game):
        super().__init__(game)
        self.menu = Pause(self.game.ui)
    def enter(self, params=None):
        self.game.main = GameState.PAUSE
        self.game.ui.main = GameState.PAUSE
        self.game.ui.setup_button_factories()
        self.menu.setup_buttons()
    def exit(self): pass
    def update(self, dt):
        ui_main = getattr(self.game.ui, 'main', None)
        if ui_main == GameState.PLAYING: self.game.state_manager.change_state(GameState.PLAYING)
