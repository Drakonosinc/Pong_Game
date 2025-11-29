import random, copy, torch
import numpy as np
from Type_Model import *
import tensorflow as tf 

def _is_torch_model(model):
    return hasattr(model, 'parameters') and isinstance(model, torch.nn.Module)

def _is_tf_model(model):
    return (tf is not None) and hasattr(model, 'trainable_variables') and isinstance(model, tf.keras.Model)

def _get_weights_np(model):
