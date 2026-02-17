import numpy as np
from src.Core.Interfaces.IAIModel import IAIModel
class MockAdapter(IAIModel):
    def __init__(self, output_size: int = 2): self.output_size = output_size
    def predict(self, state: np.ndarray) -> np.ndarray: return np.random.uniform(-1, 1, self.output_size)
    def save(self, path: str): print(f"[MockAdapter] 'Saving' model to {path}")
    def load(self, path: str): print(f"[MockAdapter] 'Loading' model from {path}")
    def get_internal_model(self): return None