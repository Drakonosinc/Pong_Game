from .State import State
from Utils.States import GameState
from Interface.Menus.Main_Menu import MainMenu
class MenuState(State):
    def __init__(self, game):
        super().__init__(game)
        self.menu = MainMenu(self.game.ui)
    def enter(self, params=None):
        self.game.main = GameState.MENU
        self.game.ui.setup_button_factories()
        self.menu.setup_buttons()
    def exit(self):pass
    def update(self, dt):pass
    def draw(self, surface):
        self.menu.render()
    def handle_event(self, event): 
        if self.game.main == GameState.MENU: self.game.events_buttons(event)