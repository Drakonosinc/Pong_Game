import numpy as np
from src.Core.Interfaces.IAIModel import IAIModel
class MockAdapter(IAIModel):
    def __init__(self, output_size: int = 2): self.output_size = output_size
