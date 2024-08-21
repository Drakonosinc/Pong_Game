import torch
import torch.nn as nn

class SimpleNN(nn.Module):
    def __init__(self, input_size, output_size):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(input_size, 128)
        self.fc2 = nn.Linear(128, output_size)
        self.activations=None
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        self.activations = x.detach().numpy().reshape(1, -1)  # Asegúrate de que las activaciones sean una matriz 2D
        self.activations = (self.activations - self.activations.min()) / (self.activations.max() - self.activations.min())  # Normaliza las activaciones
        x = self.fc2(x)
        return x