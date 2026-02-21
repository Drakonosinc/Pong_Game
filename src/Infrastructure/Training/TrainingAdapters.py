import torch
from src.Core.Interfaces.ITrainer import ITrainer
from src.Type_Training.Genetic_Algorithm import genetic_algorithm, save_genetic_model
from src.Type_Training.Q_learning import q_learning_algorithm, save_qlearning_model
class GeneticTrainer(ITrainer):
    def train(self, game):
        print("[GeneticTrainer] Iniciando protocolo genético...")
        cfg = game.config.config_AI
        nn_cfg = cfg.get("nn", {"hidden_layers": 2, "neurons_per_layer": 6})
        arch = [nn_cfg.get("neurons_per_layer", 6)] * nn_cfg.get("hidden_layers", 2)
