import torch
import numpy as np
class AIHandler:
    def __init__(self, game):
        self.game = game
        self.prev_state = None
        self.prev_action = None
        self.prev_reward = 0
    def get_state(self):
        return np.array([self.game.player_one.rect.x, self.game.player_one.rect.y, self.game.player_two.rect.x, 
                        self.game.player_two.rect.y, self.game.balls[0].rect.x, self.game.balls[0].rect.y])
    def actions_AI(self, model):
        if hasattr(self.game, '_qlearning_state') and self.game.config.config_AI["type_training"]["Q-learning"]: self._qlearning_actions(model)
        else:
            state = self.get_state()
            action = model(torch.tensor(state, dtype=torch.float32)).detach().numpy()
            self.AI_actions(action)
    def _qlearning_actions(self, model):
        from Type_Training.Q_learning import _qlearning_trainer
        if _qlearning_trainer is None: return
        current_state = self.get_state()
        current_reward = self.game.player_two.reward
        if self.prev_state is not None and self.prev_action is not None:
            reward = current_reward - self.prev_reward
            done = (self.game.player_one.score >= self.game.config.config_game["max_score"] or self.game.player_two.score >= self.game.config.config_game["max_score"])
            _qlearning_trainer.store_experience(self.prev_state, self.prev_action, reward, current_state, done)
        action = _qlearning_trainer.get_action(current_state)
        if action == 0 and self.game.player_two.rect.top > 0: self.game.player_two.rect.y -= 5
        elif action == 1 and self.game.player_two.rect.bottom < self.game.HEIGHT: self.game.player_two.rect.y += 5
        self.prev_state = current_state.copy()
        self.prev_action = action
        self.prev_reward = current_reward
    def AI_actions(self, action):
        if action[0] > 0 and self.game.player_two.rect.top > 0: self.game.player_two.rect.y -= 5
        if action[0] < 0 and self.game.player_two.rect.bottom < self.game.HEIGHT: self.game.player_two.rect.y += 5
    def reset_qlearning_state(self):
        """Reset Q-learning state for new episode"""
        self.prev_state = None
        self.prev_action = None
        self.prev_reward = 0