from .State import State
from Utils.States import GameState
from .GameOverState import GameOverState
class PlayingState(State):
    def __init__(self, game):
        super().__init__(game)
    def enter(self, params=None):
        self.game.main = GameState.PLAYING
        self.game.ui.main = GameState.PLAYING
        self.game.game_over = False
        if params and params.get("reset"): self.game.reset()
    def exit(self): pass
    def update(self, dt):
        if self.game.mode_game["Training AI"] or self.game.mode_game["AI"]:  self.game.type_game()
