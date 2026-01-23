from abc import ABC, abstractmethod
class State(ABC):
    def __init__(self, game):
        self.game = game
        self.manager = game.state_manager
    @abstractmethod
    def enter(self, params=None): pass
    @abstractmethod
    def exit(self): pass
    @abstractmethod
    def update(self, dt): pass
    @abstractmethod
    def draw(self, surface): pass
    @abstractmethod
    def handle_event(self, event): pass