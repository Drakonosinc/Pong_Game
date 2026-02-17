import torch
import numpy as np
from src.Core.Interfaces.IAIModel import IAIModel
class PyTorchAdapter(IAIModel):
    def __init__(self, model: torch.nn.Module):
