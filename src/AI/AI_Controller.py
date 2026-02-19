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
            action = self.model_adapter.predict(state)
            self.AI_actions(action)
    def _qlearning_actions(self):
        from src.Type_Training.Q_learning import _qlearning_trainer
        if _qlearning_trainer is None: return
        current_state = self.get_state()
        current_reward = self.game.game_logic.player_two.reward
        if self.prev_state is not None and self.prev_action is not None:
            reward = current_reward - self.prev_reward
            done = (self.game.game_logic.player_one.score >= self.game.config.config_game["max_score"] or 
                    self.game.game_logic.player_two.score >= self.game.config.config_game["max_score"])
            _qlearning_trainer.store_experience(self.prev_state, self.prev_action, reward, current_state, done)
        action = _qlearning_trainer.get_action(current_state)
        p2 = self.game.game_logic.player_two
        if action == 0 and p2.rect.top > 0: p2.rect.y -= 5
        elif action == 1 and p2.rect.bottom < self.game.HEIGHT: p2.rect.y += 5
        self.prev_state = current_state.copy()
        self.prev_action = action
        self.prev_reward = current_reward
    def AI_actions(self, action):
