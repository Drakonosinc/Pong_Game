from keras import layers, Model
import numpy as np

class SimpleNN(Model):
    def __init__(self, input_size, output_size):
        super(SimpleNN, self).__init__()
        self.fc1 = layers.Dense(128, activation='relu', input_shape=(input_size,))
        self.fc2 = layers.Dense(output_size)
        self.activations = None
