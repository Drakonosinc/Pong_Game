import torch
import numpy as np
from src.Core.Interfaces.IAIModel import IAIModel
class PyTorchAdapter(IAIModel):
    def __init__(self, model: torch.nn.Module):
        self.model = model
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
    def predict(self, state: np.ndarray) -> np.ndarray:
        self.model.eval()
        with torch.no_grad():
            state_tensor = torch.FloatTensor(state).to(self.device)
            output = self.model(state_tensor)
            return output.cpu().numpy().flatten()
