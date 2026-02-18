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
    def get_state(self): return self.game.game_logic.get_state_vector()
    def actions_AI(self):
        if self.game.config.config_AI["type_training"]["Q-learning"]: self._qlearning_actions()
        else:
            if not self.model_adapter: return
            state = self.get_state()
