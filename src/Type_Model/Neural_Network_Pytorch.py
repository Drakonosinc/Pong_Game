import torch
import torch.nn as nn
import torch.nn.functional as F

class SimpleNN(nn.Module):
    def __init__(self, input_size, output_size, hidden_sizes=None):
        super(SimpleNN, self).__init__()
        if hidden_sizes is None or len(hidden_sizes) == 0:
            hidden_sizes = [128]
