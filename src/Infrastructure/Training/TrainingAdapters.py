import torch
from pyforgeai import (
    ITrainer,
    genetic_algorithm,
    q_learning_algorithm,
    save_genetic_model,
    save_qlearning_model,
)


class GeneticTrainer(ITrainer):
    def train(self, game):
        print("[GeneticTrainer] Iniciando algoritmo genético con PyForgeAI...")
        cfg = game.config.config_AI
        nn_cfg = cfg.get("nn", {"hidden_layers": 2, "neurons_per_layer": 6})
        arch = [nn_cfg.get("neurons_per_layer", 6)] * nn_cfg.get("hidden_layers", 2)
        type_model_str = next(k for k, v in cfg["type_model"].items() if v)
        gen_cfg = cfg["genetic"]

        def evaluate_single_model(model):
            game.model = model
            if hasattr(game, "ai_handler") and hasattr(game.ai_handler, "set_runtime_model"):
                game.ai_handler.set_runtime_model(model)
            return float(game.run_with_model())

        best_model = genetic_algorithm(
            target=evaluate_single_model,
            type_model=type_model_str,
            input_size=len(game.ai_handler.get_state()),
            output_size=2,
            generations=gen_cfg["generation_value"],
            population_size=gen_cfg["population_value"],
            num_trials=gen_cfg["try_for_ai"],
            hidden_sizes=arch,
            stop_fn=lambda: bool(getattr(game, "exit", False)),
            on_generation_fn=lambda g: setattr(game, "generation", g),
            on_best_fn=lambda m: setattr(game, "model", m),
        )
        if cfg["model_save"] and best_model is not None:
            if type_model_str == "Pytorch":
                save_genetic_model(best_model, torch.optim.Adam(best_model.parameters(), lr=0.001), game.model_path)
            else:
                save_genetic_model(best_model, optimizer=None, path=game.model_path)
        return best_model


class QLearningTrainer(ITrainer):
    def train(self, game):
        print("[QLearningTrainer] Iniciando Q-Learning con PyForgeAI...")
        cfg = game.config.config_AI
        nn_cfg = cfg.get("nn", {"hidden_layers": 2, "neurons_per_layer": 6})
        arch = [nn_cfg.get("neurons_per_layer", 6)] * nn_cfg.get("hidden_layers", 2)
        type_model_str = next(k for k, v in cfg["type_model"].items() if v)
        q_cfg = cfg["q_learning"]

        game._qlearning_state = None
        game._qlearning_prev_reward = 0

        def run_q_episode(trainer, episode_idx):
            game.qlearning_trainer = trainer
            if hasattr(trainer, "agent") and hasattr(trainer.agent, "policy_net"):
                game.model = trainer.agent.policy_net
            game.generation = episode_idx
            return float(game.run_with_model())

        try:
            best_model = q_learning_algorithm(
                target=run_q_episode,
                type_model=type_model_str,
                input_size=len(game.ai_handler.get_state()),
                output_size=2,
                episodes=q_cfg["episodes"],
                lr=q_cfg["learning_rate"],
                gamma=q_cfg["gamma"],
                epsilon_start=q_cfg["epsilon_start"],
                epsilon_end=q_cfg["epsilon_end"],
                epsilon_decay=q_cfg["epsilon_decay"],
                hidden_sizes=arch,
                stop_fn=lambda: bool(getattr(game, "exit", False)),
            )
        finally:
            for attr in ("_qlearning_state", "_qlearning_prev_reward", "qlearning_trainer"):
                if hasattr(game, attr):
                    delattr(game, attr)

        game.model = best_model
        if cfg["model_save"] and best_model is not None:
            save_qlearning_model(best_model, torch.optim.Adam(best_model.parameters(), lr=0.001), game.model_path)
        return best_model
