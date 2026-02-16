from abc import ABC, abstractmethod
import numpy as np
class IAIModel(ABC):
    @abstractmethod
    def predict(self, state: np.ndarray) -> np.ndarray: pass
