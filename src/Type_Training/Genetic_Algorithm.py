import random,copy
from Type_Model import *
# Función de fitness
def fitness_function(model, game):
    game.model = model  # Asigna el modelo al juego antes de ejecutarlo
    score = game.run_with_model()
    return score

# Algoritmo Genético
def initialize_population(size, input_size, output_size):
    population = []
    for _ in range(size):
        model = SimpleNN(input_size, output_size)
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
    # Ordena la población según fitness (mayor es mejor)
    sorted_pop_fitness = sorted(zip(population, fitness_scores), key=lambda x: x[1], reverse=True)
    # Selecciona el top 50% (o al menos 2 individuos) para la selección de padres.
    top_count = max(2, len(sorted_pop_fitness) // 2)
    top_population = [ind for ind, fit in sorted_pop_fitness[:top_count]]
    top_fitness = [fit for ind, fit in sorted_pop_fitness[:top_count]]
    # Se seleccionan num_parents individuos usando selección por ruleta (ponderada por fitness)
    parents = random.choices(top_population, weights=top_fitness, k=num_parents)
    return parents

# Crossover a nivel de cada parámetro usando una máscara aleatoria.
# Se generan dos hijos a partir de dos padres.
def crossover(parent1, parent2):
    child1 = copy.deepcopy(parent1)
    child2 = copy.deepcopy(parent2)
    for param1, param2, child_param1, child_param2 in zip(parent1.parameters(),parent2.parameters(),child1.parameters(),child2.parameters()):
        # Genera una máscara binaria con probabilidad 0.5 para cada elemento
        mask = torch.rand_like(param1) > 0.5
        # Combina los parámetros de ambos padres para cada hijo
        child_param1.data.copy_(param1.data * mask + param2.data * (~mask))
        child_param2.data.copy_(param2.data * mask + param1.data * (~mask))
    return child1, child2

# Mutación: Se añade ruido gaussiano a cada parámetro con una probabilidad (mutation_rate)
def mutate(model, mutation_rate=0.01, mutation_strength=0.1):
    with torch.no_grad():
        for param in model.parameters():
            if random.random() < mutation_rate:
                noise = torch.randn(param.size()) * mutation_strength
                param.add_(noise)
    return model

# Algoritmo Genético Integrado:
def genetic_algorithm(game, input_size, output_size, generations=100, population_size=20, mutation_rate=0.01, mutation_strength=0.1, elitism=2, num_trials=3):
    # Inicializa la población
    population = initialize_population(population_size, input_size, output_size)
    best_fitness = -float('inf')
    best_model = None
    for generation in range(generations):
        game.generation = generation  # Para mostrar la generación en la interfaz (si se usa)
        fitness_scores = evaluate_population(population, game, num_trials)
        current_best = max(fitness_scores)
        if current_best > best_fitness:
            best_fitness = current_best
            best_model = copy.deepcopy(population[fitness_scores.index(current_best)])
        print(f"Generación {generation}: Mejor Fitness = {current_best}")
        # Elitismo: se conservan los mejores 'elitism' individuos
        sorted_population = [model for _, model in sorted(zip(fitness_scores, population), key=lambda x: x[0], reverse=True)]
        new_population = [copy.deepcopy(sorted_population[i]) for i in range(elitism)]
        # Se deben generar el resto de la población mediante cruce y mutación
        num_offsprings = population_size - elitism
        # Selecciona padres de entre el top (por ejemplo, usando la función definida)
        parents = select_parents(population, fitness_scores, num_offsprings)
        offspring = []
        # Se emparejan padres de a dos para aplicar crossover
        for i in range(0, len(parents) - 1, 2):
            child1, child2 = crossover(parents[i], parents[i+1])
            offspring.append(mutate(child1, mutation_rate, mutation_strength))
            offspring.append(mutate(child2, mutation_rate, mutation_strength))
        # Si el número de offsprings es impar, se añade un extra mutado de un padre aleatorio
        while len(offspring) < num_offsprings:
            extra_parent = random.choice(population)
            offspring.append(mutate(copy.deepcopy(extra_parent), mutation_rate, mutation_strength))
        # La nueva población es la unión de los individuos elitistas y los offsprings
        population = new_population + offspring[:num_offsprings]
    # Se asigna el mejor modelo encontrado al juego
    game.model = best_model
    return best_model

def save_model(model, optimizer, path):
    print("save model")
    torch.save({
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
    }, path)

def load_model(path, input_size, output_size, optimizer=None):
    try:
        print("load model")
        model = SimpleNN(input_size, output_size)
        checkpoint = torch.load(path)
        model.load_state_dict(checkpoint['model_state_dict'])
        if optimizer:optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        return model
    except FileNotFoundError:
        print(f"The file {path} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred while loading the model: {e}")
        return None