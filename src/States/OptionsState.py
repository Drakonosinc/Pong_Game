from .State import State
from Utils.States import GameState
class OptionsState(State):
    def enter(self, params=None):
        self.game.main = GameState.OPTIONS
    def exit(self): pass
    def update(self, dt): pass
    def draw(self, surface): self.game.visuals_items.draw()
    def handle_event(self, event): pass