from .State import State
from Utils.States import GameState
class MenuState(State):
    def __init__(self, game):
        super().__init__(game)
    def enter(self, params=None): self.game.main = GameState.MENU
    def exit(self): pass
    def update(self, dt): pass
    def draw(self, surface): self.game.visuals_items.draw()
    def handle_event(self, event): 
