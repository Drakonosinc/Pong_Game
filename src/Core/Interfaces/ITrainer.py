from abc import ABC, abstractmethod
class ITrainer(ABC):
    @abstractmethod
    def train(self, game_instance) -> object: pass