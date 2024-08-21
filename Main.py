from Genetic_Algorithm import *
from Space_Pong import *

if __name__=="__main__":
    input_size = 6  # Definir el tamaño de entrada
    output_size = 2  # Definir el tamaño de salida
    game=Space_pong_game()
    best_model = genetic_algorithm(game, input_size, output_size)
    save_model(best_model, game.model_path)
    game.model = best_model
    game.run_with_model()
pygame.quit()