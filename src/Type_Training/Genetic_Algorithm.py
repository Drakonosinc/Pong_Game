import random,copy,torch
from Type_Model import *
def fitness_function(model, game):
    game.model = model  
    score = game.run_with_model()
    return score

def initialize_population(size, input_size, output_size, hidden_sizes=None):
    population = []
    for _ in range(size):
        model = SimpleNN(input_size, output_size, hidden_sizes=hidden_sizes)
        population.append(model)
