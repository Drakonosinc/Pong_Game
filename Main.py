import sys
from Genetic_Algorithm import *
from Space_Pong import *
if __name__=="__main__":
    best_model = genetic_algorithm((game:=Space_pong_game()), input_size=len(game.get_state()), output_size=2, generations=game.config_AI["generation_value"], population_size=game.config_AI["population_value"], num_trials=game.config_AI["try_for_ai"])
    game.model = best_model
    if game.config_AI["model_save"]:save_model(best_model, torch.optim.Adam(game.model.parameters(), lr=0.001),game.model_path)
pygame.quit(),sys.exit()