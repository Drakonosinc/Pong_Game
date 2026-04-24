import random
import numpy as np
try: import torch
except ImportError: torch = None
def _load_tensorflow(optional: bool = True):
    try:
        import tensorflow as tf
        return tf
    except ImportError:
        if optional: return None
        raise ImportError("TensorFlow no esta instalado en el entorno actual.")
def _build_model(type_model, input_size, output_size, hidden_sizes=None):
    if type_model == "Pytorch":
        if torch is None:
            raise ImportError("PyTorch no esta instalado en el entorno actual.")
        from src.Type_Model.Neural_Network_Pytorch import SimpleNN_Pytorch
        return SimpleNN_Pytorch(input_size, output_size, hidden_sizes=hidden_sizes)
    if type_model == "Tensorflow":
        _load_tensorflow(optional=False)
        from src.Type_Model.Neural_Network_Tensorflow import SimpleNN_Tensorflow
        return SimpleNN_Tensorflow(input_size, output_size, hidden_sizes=hidden_sizes)
    raise ValueError(f"Unknown type_model: {type_model}")
def _is_torch_model(model):
    return torch is not None and hasattr(model, "parameters") and isinstance(model, torch.nn.Module)
def _is_tf_model(model):
    if not hasattr(model, "trainable_variables"): return False
    tf = _load_tensorflow(optional=True)
    return (tf is not None) and isinstance(model, tf.keras.Model)
def _get_weights_np(model):
    if _is_torch_model(model): return [p.detach().cpu().numpy().copy() for p in model.parameters()]
    if _is_tf_model(model): return [w.copy() for w in model.get_weights()]
    raise TypeError("Unsupported model type for genetic algorithm")
def _set_weights_np(model, weights):
    if _is_torch_model(model):
        with torch.no_grad():
            for p, w in zip(model.parameters(), weights):
                tensor_w = torch.from_numpy(np.array(w, copy=False)).to(p.device, dtype=p.dtype)
                p.copy_(tensor_w)
        return
    if _is_tf_model(model):
        model.set_weights([np.array(w, copy=False) for w in weights])
        return
    raise TypeError("Unsupported model type for genetic algorithm")
def _ensure_built_if_tf(model, input_size):
    if _is_tf_model(model):
        try:
            if not getattr(model, "built", False) or len(model.weights) == 0:
                tf = _load_tensorflow(optional=False)
                dummy = tf.zeros((1, int(input_size)), dtype=tf.float32)
                _ = model(dummy, training=False)
        except Exception: pass
def fitness_function(model, game):
    game.model = model
    if hasattr(game, "ai_handler") and hasattr(game.ai_handler, "set_runtime_model"):
        game.ai_handler.set_runtime_model(model)
    return game.run_with_model()
def initialize_population(type_model, size, input_size, output_size, hidden_sizes=None):
    population = []
    for _ in range(size):
        model = _build_model(type_model, input_size, output_size, hidden_sizes=hidden_sizes)
        _ensure_built_if_tf(model, input_size)
        population.append(model)
    return population
def evaluate_population(population, game, num_trials=3):
    evaluated_population = []
    fitness_scores = []
    for model in population:
        if game.exit: break
        score = []
        for _ in range(num_trials):
            score.append(fitness_function(model, game))
            if game.exit: break
        if not score: break
        evaluated_population.append(model)
        fitness_scores.append(sum(score) / len(score))
        if game.exit: break
    if not fitness_scores: return [], []
    min_score = abs(min(fitness_scores)) if min(fitness_scores) < 0 else 0
    fitness_scores = [score + min_score + 1 for score in fitness_scores]
    return evaluated_population, fitness_scores
def select_parents(population, fitness_scores, num_parents):
    sorted_pop_fitness = sorted(zip(population, fitness_scores), key=lambda x: x[1], reverse=True)
    top_count = max(2, len(sorted_pop_fitness) // 2)
    top_population = [individual for individual, _ in sorted_pop_fitness[:top_count]]
    top_fitness = [fitness for _, fitness in sorted_pop_fitness[:top_count]]
    return random.choices(top_population, weights=top_fitness, k=num_parents)
def _new_model(type_model, input_size, output_size, hidden_sizes):
    model = _build_model(type_model, input_size, output_size, hidden_sizes=hidden_sizes)
    _ensure_built_if_tf(model, input_size)
    return model
def crossover(parent1, parent2, type_model, input_size, output_size, hidden_sizes=None):
    w1 = _get_weights_np(parent1)
    w2 = _get_weights_np(parent2)
    child1_w, child2_w = [], []
    for a, b in zip(w1, w2):
        mask = np.random.rand(*a.shape) > 0.5
        child1_w.append(np.where(mask, a, b))
        child2_w.append(np.where(mask, b, a))
    child1 = _new_model(type_model, input_size, output_size, hidden_sizes)
    child2 = _new_model(type_model, input_size, output_size, hidden_sizes)
    _set_weights_np(child1, child1_w)
    _set_weights_np(child2, child2_w)
    return child1, child2
def mutate(model, mutation_rate=0.01, mutation_strength=0.1):
    weights = _get_weights_np(model)
    mutated = []
    for w in weights:
        mask = np.random.rand(*w.shape) < float(mutation_rate)
        noise = np.random.randn(*w.shape) * float(mutation_strength)
        mutated.append((w + noise * mask).astype(w.dtype, copy=False))
