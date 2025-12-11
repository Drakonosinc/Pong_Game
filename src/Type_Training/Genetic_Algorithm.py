import random, copy, torch
import numpy as np
from Type_Model import *
import tensorflow as tf 

def _is_torch_model(model): return hasattr(model, 'parameters') and isinstance(model, torch.nn.Module)

def _is_tf_model(model): return (tf is not None) and hasattr(model, 'trainable_variables') and isinstance(model, tf.keras.Model)

def _get_weights_np(model):
    if _is_torch_model(model): return [p.detach().cpu().numpy().copy() for p in model.parameters()]
    elif _is_tf_model(model): return [w.copy() for w in model.get_weights()]
    else: raise TypeError("Unsupported model type for genetic algorithm")

def _set_weights_np(model, weights):
    if _is_torch_model(model):
        with torch.no_grad():
            for p, w in zip(model.parameters(), weights):
                tensor_w = torch.from_numpy(np.array(w, copy=False)).to(p.device, dtype=p.dtype)
                p.copy_(tensor_w)
    elif _is_tf_model(model): model.set_weights([np.array(w, copy=False) for w in weights])
    else: raise TypeError("Unsupported model type for genetic algorithm")

def _ensure_built_if_tf(model, input_size):
    if _is_tf_model(model):
        # Build variables if the model hasn't been called yet
        try:
            if not getattr(model, 'built', False) or len(model.weights) == 0:
                dummy = tf.zeros((1, int(input_size)), dtype=tf.float32)
                _ = model(dummy, training=False)
        # Best effort; if build fails it will surface on set_weights
        except Exception: pass

def fitness_function(model, game):
    game.model = model
    score = game.run_with_model()
    return score

def initialize_population(type_model, size, input_size, output_size, hidden_sizes=None):
    population = []
    for _ in range(size):
        if type_model == "Pytorch": model = SimpleNN_Pytorch(input_size, output_size, hidden_sizes=hidden_sizes)
        elif type_model == "Tensorflow":
            model = SimpleNN_Tensorflow(input_size, output_size, hidden_sizes=hidden_sizes)
            _ensure_built_if_tf(model, input_size)
        else: raise ValueError(f"Unknown type_model: {type_model}")
        population.append(model)
    return population

def evaluate_population(population, game, num_trials=3):
    fitness_scores = []
    for model in population:
        score = [fitness_function(model, game) for _ in range(num_trials)]
        fitness_scores.append(sum(score) / num_trials)
    min_score = abs(min(fitness_scores)) if min(fitness_scores) < 0 else 0
    fitness_scores = [score + min_score + 1 for score in fitness_scores]
    return fitness_scores

def select_parents(population, fitness_scores, num_parents):
    sorted_pop_fitness = sorted(zip(population, fitness_scores), key=lambda x: x[1], reverse=True)
    top_count = max(2, len(sorted_pop_fitness) // 2)
    top_population = [ind for ind, fit in sorted_pop_fitness[:top_count]]
    top_fitness = [fit for ind, fit in sorted_pop_fitness[:top_count]]
    parents = random.choices(top_population, weights=top_fitness, k=num_parents)
    return parents

def _new_model(type_model, input_size, output_size, hidden_sizes):
    if type_model == "Pytorch": return SimpleNN_Pytorch(input_size, output_size, hidden_sizes=hidden_sizes)
    elif type_model == "Tensorflow":
        m = SimpleNN_Tensorflow(input_size, output_size, hidden_sizes=hidden_sizes)
        _ensure_built_if_tf(m, input_size)
        return m
    else: raise ValueError(f"Unknown type_model: {type_model}")

def crossover(parent1, parent2, type_model, input_size, output_size, hidden_sizes=None):
    w1 = _get_weights_np(parent1)
    w2 = _get_weights_np(parent2)
    child1_w, child2_w = [], []
    for a, b in zip(w1, w2):
        mask = np.random.rand(*a.shape) > 0.5
        c1 = np.where(mask, a, b)
        c2 = np.where(mask, b, a)
        child1_w.append(c1)
        child2_w.append(c2)
    child1 = _new_model(type_model, input_size, output_size, hidden_sizes)
    child2 = _new_model(type_model, input_size, output_size, hidden_sizes)
    _set_weights_np(child1, child1_w)
    _set_weights_np(child2, child2_w)
    return child1, child2

def mutate(model, mutation_rate=0.01, mutation_strength=0.1):
    weights = _get_weights_np(model)
    mutated = []
    for w in weights:
        mask = (np.random.rand(*w.shape) < float(mutation_rate))
        noise = np.random.randn(*w.shape) * float(mutation_strength)
        mutated.append((w + noise * mask).astype(w.dtype, copy=False))
    _set_weights_np(model, mutated)
    return model

def genetic_algorithm(game, type_model, input_size, output_size, generations=100, population_size=20, mutation_rate=0.01, mutation_strength=0.1, elitism=2, num_trials=3, hidden_sizes=None):
    population = initialize_population(type_model, population_size, input_size, output_size, hidden_sizes=hidden_sizes)
    best_fitness = -float('inf')
    best_model = None
    for generation in range(generations):
        game.generation = generation
        fitness_scores = evaluate_population(population, game, num_trials)
        current_best = max(fitness_scores)
        if current_best > best_fitness:
            best_fitness = current_best
            best_idx = fitness_scores.index(current_best)
            best_parent = population[best_idx]
            best_model = _new_model(type_model, input_size, output_size, hidden_sizes)
            _set_weights_np(best_model, _get_weights_np(best_parent))
        print(f"Generación {generation}: Mejor Fitness = {current_best}")
        sorted_population = [model for _, model in sorted(zip(fitness_scores, population), key=lambda x: x[0], reverse=True)]
        new_population = []
        for i in range(elitism):
            elite_parent = sorted_population[i]
            elite_copy = _new_model(type_model, input_size, output_size, hidden_sizes)
            _set_weights_np(elite_copy, _get_weights_np(elite_parent))
            new_population.append(elite_copy)
        num_offsprings = population_size - elitism
        parents = select_parents(population, fitness_scores, num_offsprings)
        offspring = []
        for i in range(0, len(parents) - 1, 2):
            child1, child2 = crossover(parents[i], parents[i+1], type_model, input_size, output_size, hidden_sizes)
            offspring.append(mutate(child1, mutation_rate, mutation_strength))
            offspring.append(mutate(child2, mutation_rate, mutation_strength))
        while len(offspring) < num_offsprings:
            extra_parent = random.choice(population)
            extra_child = _new_model(type_model, input_size, output_size, hidden_sizes)
            _set_weights_np(extra_child, _get_weights_np(extra_parent))
            offspring.append(mutate(extra_child, mutation_rate, mutation_strength))
