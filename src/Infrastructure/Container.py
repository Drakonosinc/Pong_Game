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
        return self.game
    def _configure_ai_strategy(self, base_model):
        if not base_model: return
        config = self.game.config.config_AI
        type_model = config.get("type_model", {})
        if type_model.get("Pytorch", False): adapter = PyTorchAdapter(base_model)
        elif type_model.get("Tensorflow", False): adapter = TensorFlowAdapter(base_model)
        else: adapter = MockAdapter(output_size=2)
