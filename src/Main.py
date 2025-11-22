import sys
from Type_Training import *
from Game.Space_Pong import *
if __name__=="__main__":
    while True:
        (game:=Space_pong_game()).run()
        game.game_over=False
        match game.mode_game:
            case {"Training AI": True}:
                nn_cfg = game.config.config_AI.get("nn", {"hidden_layers": 2, "neurons_per_layer": 6})
                arch = [nn_cfg.get("neurons_per_layer", 6)] * nn_cfg.get("hidden_layers", 2)
                if game.config.config_AI["type_training"]["Genetic"]:
                    genetic_config = game.config.config_AI["genetic"]
                    best_model = genetic_algorithm(game, input_size=len(game.ai_handler.get_state()), output_size=2, generations=genetic_config["generation_value"], population_size=genetic_config["population_value"], num_trials=genetic_config["try_for_ai"], hidden_sizes=arch)
                elif game.config.config_AI["type_training"]["Q-learning"]:
                    q_config = game.config.config_AI["q_learning"]
                    nn_cfg = game.config.config_AI.get("nn", {"hidden_layers": 2, "neurons_per_layer": 6})
                    arch = [nn_cfg.get("neurons_per_layer", 6)] * nn_cfg.get("hidden_layers", 2)
                    best_model = q_learning_algorithm(game, input_size=len(game.ai_handler.get_state()), output_size=2, episodes=q_config["episodes"],lr=q_config["learning_rate"],gamma=q_config["gamma"],epsilon_start=q_config["epsilon_start"],epsilon_end=q_config["epsilon_end"],epsilon_decay=q_config["epsilon_decay"], hidden_sizes=arch)
                game.model = best_model
                if game.config.config_AI["model_save"]:save_model(game.model, torch.optim.Adam(game.model.parameters(), lr=0.001),game.model_path)
            case {"Player": True} | {"AI": True}:game.run_with_model()
        if game.exit:break
pygame.quit(),sys.exit()