import numpy as np
from src.Core.Interfaces.IAIModel import IAIModel
class AIHandler:
    def __init__(self, game):
        self.game = game
        self.prev_state = None
        self.prev_action = None
        self.prev_reward = 0
        self.model_adapter: IAIModel = None 
    def set_model(self, model_adapter: IAIModel): self.model_adapter = model_adapter
