from .State import State
from Utils.States import GameState
from Interface.Menus.Game_Over import GameOver
class GameOverState(State):
    def __init__(self, game):
        super().__init__(game)
        self.menu = GameOver(self.game.ui)
    def enter(self, params=None):
        self.game.main = GameState.GAME_OVER
        self.game.ui.main = GameState.GAME_OVER
        self.game.ui.setup_button_factories()
        self.menu.setup_buttons()
    def exit(self): pass
    def update(self, dt):
        ui_main = getattr(self.game.ui, 'main', None)
        if ui_main == GameState.MENU: self.game.state_manager.change_state(GameState.MENU)
        elif ui_main == GameState.PLAYING: self.game.state_manager.change_state(GameState.PLAYING)
    def draw(self, surface):
        self.game.visuals_items.draw()
        self.menu.render()
    def handle_event(self, event):
        if self.game.main == GameState.GAME_OVER: self.game.events_buttons(event)