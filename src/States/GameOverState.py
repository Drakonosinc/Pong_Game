from .State import State
from Utils.States import GameState
class GameOverState(State):
    def enter(self, params=None):
        self.game.main = GameState.GAME_OVER
    def exit(self): pass
    def update(self, dt): pass
    def draw(self, surface): self.game.visuals_items.draw()
    def handle_event(self, event): pass