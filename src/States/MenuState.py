from .State import State
from Utils.States import GameState
from Interface.Menus.Main_Menu import MainMenu
from .ModeSelectState import ModeSelectState
from .OptionsState import OptionsState
class MenuState(State):
    def __init__(self, game):
        super().__init__(game)
        self.menu = MainMenu(self.game.ui)
    def enter(self, params=None):
        self.game.main = GameState.MENU
        self.game.ui.setup_button_factories()
        self.menu.setup_buttons()
    def exit(self): pass
    def update(self, dt):
        if self.game.main == GameState.MODE_SELECT: self.game.state_manager.change(ModeSelectState(self.game))
        elif self.game.main == GameState.OPTIONS: self.game.state_manager.change(OptionsState(self.game))
    def draw(self, surface): self.menu.render()
    def handle_event(self, event): 
        if self.game.main == GameState.MENU: self.game.events_buttons(event)