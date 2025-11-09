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
    for param1, param2, child_param1, child_param2 in zip(parent1.parameters(),parent2.parameters(),child1.parameters(),child2.parameters()):
        mask = torch.rand_like(param1) > 0.5
        child_param1.data.copy_(param1.data * mask + param2.data * (~mask))
        child_param2.data.copy_(param2.data * mask + param1.data * (~mask))
    return child1, child2

def mutate(model, mutation_rate=0.01, mutation_strength=0.1):
    with torch.no_grad():
        for param in model.parameters():
            if random.random() < mutation_rate:
                noise = torch.randn(param.size()) * mutation_strength
                param.add_(noise)
    return model

def genetic_algorithm(game, input_size, output_size, generations=100, population_size=20, mutation_rate=0.01, mutation_strength=0.1, elitism=2, num_trials=3, hidden_sizes=None):
    population = initialize_population(population_size, input_size, output_size, hidden_sizes=hidden_sizes)
    best_fitness = -float('inf')
    best_model = None
    for generation in range(generations):
        game.generation = generation  
        fitness_scores = evaluate_population(population, game, num_trials)
        current_best = max(fitness_scores)
        if current_best > best_fitness:
            best_fitness = current_best
            best_model = copy.deepcopy(population[fitness_scores.index(current_best)])
        print(f"Generación {generation}: Mejor Fitness = {current_best}")
        sorted_population = [model for _, model in sorted(zip(fitness_scores, population), key=lambda x: x[0], reverse=True)]
        new_population = [copy.deepcopy(sorted_population[i]) for i in range(elitism)]
        num_offsprings = population_size - elitism
        parents = select_parents(population, fitness_scores, num_offsprings)
        offspring = []
        for i in range(0, len(parents) - 1, 2):
            child1, child2 = crossover(parents[i], parents[i+1])
            offspring.append(mutate(child1, mutation_rate, mutation_strength))
            offspring.append(mutate(child2, mutation_rate, mutation_strength))
        while len(offspring) < num_offsprings:
            extra_parent = random.choice(population)
            offspring.append(mutate(copy.deepcopy(extra_parent), mutation_rate, mutation_strength))
        population = new_population + offspring[:num_offsprings]
    game.model = best_model
    return best_model

