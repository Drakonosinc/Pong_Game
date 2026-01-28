from .State import State
from Utils.States import GameState
class ModeSelectState(State):
    def enter(self, params=None):
        self.game.main = GameState.MODE_SELECT
    def exit(self): pass
    def update(self, dt): pass
    def draw(self, surface): self.game.visuals_items.draw()
    def handle_event(self, event): self.game.events_buttons(event)