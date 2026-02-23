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
        type_model_str = next(k for k, v in cfg["type_model"].items() if v)
        gen_cfg = cfg["genetic"]
        best_model = genetic_algorithm(
            game,
            type_model_str,
            input_size=len(game.ai_handler.get_state()),
            output_size=2,
            generations=gen_cfg["generation_value"],
            population_size=gen_cfg["population_value"],
            num_trials=gen_cfg["try_for_ai"],
            hidden_sizes=arch)
        if cfg["model_save"]:
            if type_model_str == "Pytorch": save_genetic_model(best_model, torch.optim.Adam(best_model.parameters(), lr=0.001), game.model_path)
            else: save_genetic_model(best_model, optimizer=None, path=game.model_path)
        return best_model
class QLearningTrainer(ITrainer):
    def train(self, game):
        print("[QLearningTrainer] Iniciando protocolo Q-Learning...")
        cfg = game.config.config_AI
        nn_cfg = cfg.get("nn", {"hidden_layers": 2, "neurons_per_layer": 6})
        arch = [nn_cfg.get("neurons_per_layer", 6)] * nn_cfg.get("hidden_layers", 2)
        type_model_str = next(k for k, v in cfg["type_model"].items() if v)
        q_cfg = cfg["q_learning"]
        best_model = q_learning_algorithm(
            game, 
            type_model_str, 
            input_size=len(game.ai_handler.get_state()), 
            output_size=2, 
            episodes=q_cfg["episodes"], 
