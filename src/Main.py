import sys
from Type_Training import *
from Game.Space_Pong import *
if __name__=="__main__":
    while True:
        (game:=Space_pong_game()).run()
        game.game_over=False
        match game.mode_game:
            case {"Training AI": True}:
                best_model = genetic_algorithm(game, input_size=len(game.ai_handler.get_state()), output_size=2, generations=game.config.config_AI["generation_value"], population_size=game.config.config_AI["population_value"], num_trials=game.config.config_AI["try_for_ai"])
                game.model = best_model
                if game.config.config_AI["model_save"]:save_model(game.model, torch.optim.Adam(game.model.parameters(), lr=0.001),game.model_path)
            case {"Player": True} | {"AI": True}:game.run_with_model()
        if game.exit:break
pygame.quit(),sys.exit()