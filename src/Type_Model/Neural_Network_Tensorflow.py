from tensorflow import layers, Model
import numpy as np

class SimpleNN(Model):
    def __init__(self, input_size, output_size, hidden_sizes=None):
        super(SimpleNN, self).__init__()
        if hidden_sizes is None or len(hidden_sizes) == 0: hidden_sizes = [128]
