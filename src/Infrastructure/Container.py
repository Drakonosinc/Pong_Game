from src.Infrastructure.AI.Adapters.PyTorchAdapter import PyTorchAdapter
from src.Infrastructure.AI.Adapters.TensorFlowAdapter import TensorFlowAdapter
from src.Infrastructure.AI.Adapters.MockAdapter import MockAdapter
from src.Infrastructure.Training.TrainingAdapters import GeneticTrainer, QLearningTrainer
from src.Game.Space_Pong import Space_pong_game
class Container:
    def __init__(self):
        self.game = None
    def create_app(self) -> 'Space_pong_game':
        self.game = Space_pong_game()
        self._configure_ai_strategy(self.game.model_training)
