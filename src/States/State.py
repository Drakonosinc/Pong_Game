from abc import ABC, abstractmethod
class State(ABC):
    def __init__(self, game):
        self.game = game
        self.manager = game.state_manager
    @abstractmethod
    def enter(self, params=None): pass
