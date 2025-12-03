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
