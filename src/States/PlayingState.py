from .State import State
from Utils.States import GameState
class PlayingState(State):
    def __init__(self, game):
        super().__init__(game)
    def enter(self, params=None):
        self.game.main = GameState.PLAYING
        self.game.game_over = False
        if params and params.get("reset"): self.game.reset()
