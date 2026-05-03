from src.Game.Space_Pong import Space_pong_game
class Container:
    def __init__(self):
        self.game = None
    def create_app(self) -> 'Space_pong_game':
        self.game = Space_pong_game()
        return self.game
    def get_trainer(self) -> object:
        if not self.game: raise RuntimeError("El juego no ha sido inicializado por el contenedor.")
        training_config = self.game.config.config_AI["type_training"]
        if training_config.get("Genetic", False):
            from src.Infrastructure.Training.TrainingAdapters import GeneticTrainer
            return GeneticTrainer()
        elif training_config.get("Q-learning", False):
            from src.Infrastructure.Training.TrainingAdapters import QLearningTrainer
