import numpy as np
try: import tensorflow as tf
except ImportError: tf = None
from src.Core.Interfaces.IAIModel import IAIModel
class TensorFlowAdapter(IAIModel):
    def __init__(self, model):
        if tf is None: raise ImportError("TensorFlow no está instalado en el entorno actual.")
        self.model = model
    def predict(self, state: np.ndarray) -> np.ndarray:
        x = tf.convert_to_tensor(state, dtype=tf.float32)
        if len(x.shape) == 1: x = tf.expand_dims(x, axis=0)
        out = self.model(x, training=False)
