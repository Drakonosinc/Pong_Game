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
    return population

def evaluate_population(population, game, num_trials=3):
    fitness_scores = []
    for model in population:
        score = [fitness_function(model, game) for _ in range(num_trials)]
        fitness_scores.append(sum(score) / num_trials)
    min_score = abs(min(fitness_scores)) if min(fitness_scores) < 0 else 0
    fitness_scores = [score + min_score + 1 for score in fitness_scores]  # Asegúrate de que todos los fitness sean positivos
    return fitness_scores

def select_parents(population, fitness_scores, num_parents):
    sorted_pop_fitness = sorted(zip(population, fitness_scores), key=lambda x: x[1], reverse=True)
    top_count = max(2, len(sorted_pop_fitness) // 2)
    top_population = [ind for ind, fit in sorted_pop_fitness[:top_count]]
    top_fitness = [fit for ind, fit in sorted_pop_fitness[:top_count]]
    parents = random.choices(top_population, weights=top_fitness, k=num_parents)
    return parents

def crossover(parent1, parent2):
    child1 = copy.deepcopy(parent1)
    child2 = copy.deepcopy(parent2)
