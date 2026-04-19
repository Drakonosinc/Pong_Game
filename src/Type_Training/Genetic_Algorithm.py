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
