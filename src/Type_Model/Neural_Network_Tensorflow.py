from keras import layers, Model
import numpy as np

class SimpleNN(Model):
    def __init__(self, input_size, output_size):
        super(SimpleNN, self).__init__()
        self.fc1 = layers.Dense(128, activation='relu', input_shape=(input_size,))
        self.fc2 = layers.Dense(output_size)
        self.activations = None
    def forward(self, x):
        x = self.fc1(x)
        self.activations = self.fc1.output
        if hasattr(x, 'numpy'):
            activations_np = self.activations.numpy().reshape(1, -1)
            min_val = np.min(activations_np)
            max_val = np.max(activations_np)
            self.activations = (activations_np - min_val) / (max_val - min_val)
        x = self.fc2(x)
        return x