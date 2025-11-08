from tensorflow import layers, Model
import numpy as np

class SimpleNN(Model):
    def __init__(self, input_size, output_size, hidden_sizes=None):
