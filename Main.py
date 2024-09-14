import sys
from Genetic_Algorithm import *
from Space_Pong import *

if __name__=="__main__":
    input_size = 6
    output_size = 2
    game=Space_pong_game()
    best_model = genetic_algorithm(game, input_size, output_size)
    game.model = best_model
    game.run_with_model()
    save_model(best_model, torch.optim.Adam(game.model.parameters(), lr=0.001),game.model_path)
pygame.quit()
sys.exit()