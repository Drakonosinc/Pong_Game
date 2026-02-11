from .State import State
from Utils.States import GameState
from .GameOverState import GameOverState
class PlayingState(State):
    def __init__(self, game):
        super().__init__(game)
