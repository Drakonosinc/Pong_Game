import torch
import torch.nn as nn
import torch.nn.functional as F

class SimpleNN(nn.Module):
    def __init__(self, input_size, output_size, hidden_sizes=None):
        super(SimpleNN, self).__init__()
