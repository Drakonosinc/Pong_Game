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
