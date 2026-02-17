import torch
import numpy as np
from src.Core.Interfaces.IAIModel import IAIModel
class PyTorchAdapter(IAIModel):
    def __init__(self, model: torch.nn.Module):
        self.model = model
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
