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
        for i, layer in enumerate(self.hidden_layers):
            x = torch.relu(layer(x))
            if i == 0:
                with torch.no_grad():
                    act = x.detach().cpu().numpy().reshape(1, -1)
                    if act.max() - act.min() != 0: self.activations = (act - act.min()) / (act.max() - act.min())
                    else: self.activations = act
        x = self.output_layer(x)
