import sys
from src.Infrastructure.AI.Adapters.PyTorchAdapter import PyTorchAdapter
from src.Infrastructure.AI.Adapters.MockAdapter import MockAdapter
from src.Infrastructure.Training.TrainingAdapters import GeneticTrainer, QLearningTrainer
from src.Game.Space_Pong import Space_pong_game
class Container:
    def __init__(self):
        self.game = None
    def create_app(self) -> 'Space_pong_game':
        self.game = Space_pong_game()
        self._configure_ai_strategy()
        return self.game
    def _configure_ai_strategy(self):
        config = self.game.config.config_AI
        type_model = config.get("type_model", {})
        if type_model.get("Pytorch", False): pass 
    def get_trainer(self) -> object:
        if not self.game: raise Exception("Game not initialized")
        training_config = self.game.config.config_AI["type_training"]
        if training_config.get("Genetic", False): return GeneticTrainer()
