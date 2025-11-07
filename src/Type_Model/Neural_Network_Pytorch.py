import torch
import torch.nn as nn
import torch.nn.functional as F

class SimpleNN(nn.Module):
    def __init__(self, input_size, output_size, hidden_sizes=None):
        super(SimpleNN, self).__init__()
        if hidden_sizes is None or len(hidden_sizes) == 0: hidden_sizes = [128]
        self.hidden_layers = nn.ModuleList()
        in_features = input_size
        for h in hidden_sizes:
            self.hidden_layers.append(nn.Linear(in_features, int(h)))
            in_features = int(h)
        self.output_layer = nn.Linear(in_features, output_size)
        self.fc1 = self.hidden_layers[0]
        self.activations = None
    def forward(self, x):
