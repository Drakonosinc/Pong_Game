import random,copy,torch
from Type_Model import *
# Función de fitness
def fitness_function(model, game):
    game.model = model  # Asigna el modelo al juego antes de ejecutarlo
    score = game.run_with_model()
    return score

# Algoritmo Genético
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
def genetic_algorithm(game, input_size, output_size, generations=100, population_size=20, mutation_rate=0.01, mutation_strength=0.1, elitism=2, num_trials=3, hidden_sizes=None):
    # Inicializa la población
    population = initialize_population(population_size, input_size, output_size, hidden_sizes=hidden_sizes)
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

def load_model(path, input_size, output_size, optimizer=None, hidden_sizes=None):
    try:
        print("load model")
        checkpoint = torch.load(path)
        state_dict = checkpoint.get('model_state_dict', checkpoint)
        # Detect legacy format (fc1/fc2) vs new (hidden_layers/output_layer)
        has_fc = any(k.startswith('fc1.') or k.startswith('fc2.') for k in state_dict.keys())
        has_hidden = any(k.startswith('hidden_layers.') for k in state_dict.keys())
        def _filtered_load(model, sd):
            msd = model.state_dict()
            filtered = {k: v for k, v in sd.items() if k in msd and msd[k].shape == v.shape}
            missing = [k for k in sd.keys() if k not in filtered]
            if missing:
                # silently skip mismatched keys to avoid size errors
                pass
            model.load_state_dict(filtered, strict=False)
        if has_fc:
            # Build architecture from fc1 weight shape (old layout had exactly one hidden layer)
            if 'fc1.weight' in state_dict:
                first_hidden = state_dict['fc1.weight'].shape[0]
            else:
                # fallback: use any weight matrix rows as hidden size
                any_w = next((v for k, v in state_dict.items() if k.endswith('.weight')), None)
                first_hidden = any_w.shape[0] if any_w is not None else 128
            model = SimpleNN(input_size, output_size, hidden_sizes=[first_hidden])
            # Remap known keys
            remapped = {}
            if 'fc1.weight' in state_dict: remapped['hidden_layers.0.weight'] = state_dict['fc1.weight']
            if 'fc1.bias' in state_dict:   remapped['hidden_layers.0.bias']   = state_dict['fc1.bias']
            # Output layer: only map if shapes match declared output_size and hidden size
            ow, ob = state_dict.get('fc2.weight'), state_dict.get('fc2.bias')
            if ow is not None and ob is not None:
                if ow.shape[0] == output_size and ow.shape[1] == first_hidden and ob.shape[0] == output_size:
                    remapped['output_layer.weight'] = ow
                    remapped['output_layer.bias'] = ob
            _filtered_load(model, remapped)
        elif has_hidden:
            # Recreate exact architecture from checkpoint
            indices = sorted({int(k.split('.')[1]) for k in state_dict.keys() if k.startswith('hidden_layers.')})
            sizes = []
            for i in indices:
                w_key = f'hidden_layers.{i}.weight'
                if w_key in state_dict:
                    sizes.append(state_dict[w_key].shape[0])
            if not sizes: sizes = hidden_sizes or [128]
            model = SimpleNN(input_size, output_size, hidden_sizes=sizes)
            # Filter to only keys that match the new model's shapes
            _filtered_load(model, state_dict)
        else:
            # Unknown format; fallback to requested/ default architecture
            model = SimpleNN(input_size, output_size, hidden_sizes=hidden_sizes)
            _filtered_load(model, state_dict)
        if optimizer and 'optimizer_state_dict' in checkpoint:
            optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        return model
    except FileNotFoundError:
        print(f"The file {path} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred while loading the model: {e}")
        return None
