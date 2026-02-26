import numpy as np
try: import tensorflow as tf
except ImportError: tf = None
from src.Core.Interfaces.IAIModel import IAIModel
class TensorFlowAdapter(IAIModel):
    def __init__(self, model):
        if tf is None: raise ImportError("TensorFlow no está instalado en el entorno actual.")
        self.model = model
    def predict(self, state: np.ndarray) -> np.ndarray:
