from tensorflow import layers, Model
import numpy as np

class SimpleNN(Model):
    def __init__(self, input_size, output_size, hidden_sizes=None):
        super(SimpleNN, self).__init__()
        if hidden_sizes is None or len(hidden_sizes) == 0: hidden_sizes = [128]
        self.hidden_layers = [layers.Dense(int(h), activation='relu') for h in hidden_sizes]
        self.output_layer = layers.Dense(output_size)
        self.fc1 = self.hidden_layers[0]
        self.activations = None
    def forward(self, x):
        for i, layer in enumerate(self.hidden_layers):
            x = layer(x)
            if i == 0:
                self.activations = x
                try:
                    activations_np = self.activations.numpy().reshape(1, -1)
                    min_val = np.min(activations_np)
