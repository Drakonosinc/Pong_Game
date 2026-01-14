import torch
import numpy as np
from Type_Training import *

try:
    import tensorflow as tf  # type: ignore
except Exception:
    tf = None

class AIHandler:
    def __init__(self, game):
        self.game = game
        self.prev_state = None
        self.prev_action = None
        self.prev_reward = 0
    def _call_model(self, model, state: np.ndarray) -> np.ndarray:
        # Torch path
        if hasattr(model, 'parameters') and isinstance(model, torch.nn.Module):
            out = model(torch.tensor(state, dtype=torch.float32))
            return out.detach().cpu().numpy().reshape(-1)
        # TensorFlow path
        if tf is not None and hasattr(model, 'trainable_variables') and isinstance(model, tf.keras.Model):
            x = tf.convert_to_tensor(state, dtype=tf.float32)
            if len(x.shape) == 1: x = tf.expand_dims(x, axis=0)
            out = model(x, training=False)
            return out.numpy().reshape(-1)
        # Fallback: treat as numpy function-like
        return np.asarray(model(state)).reshape(-1)
    def actions_AI(self, model):
        if hasattr(self.game, '_qlearning_state') and self.game.config.config_AI["type_training"]["Q-learning"]: self._qlearning_actions(model)
        else:
            state = self.get_state()
            action = self._call_model(model, state)
            self.AI_actions(action)
    def _qlearning_actions(self, model):
        from Type_Training.Q_learning import _qlearning_trainer
        if _qlearning_trainer is None: return
        current_state = self.get_state()
        current_reward = self.game.game_logic.player_two.reward
        if self.prev_state is not None and self.prev_action is not None:
            reward = current_reward - self.prev_reward
            done = (self.game.game_logic.player_one.score >= self.game.config.config_game["max_score"] or self.game.game_logic.player_two.score >= self.game.config.config_game["max_score"])
            _qlearning_trainer.store_experience(self.prev_state, self.prev_action, reward, current_state, done)
        action = _qlearning_trainer.get_action(current_state)
        if action == 0 and self.game.game_logic.player_two.rect.top > 0: self.game.game_logic.player_two.rect.y -= 5
        elif action == 1 and self.game.game_logic.player_two.rect.bottom < self.game.HEIGHT: self.game.game_logic.player_two.rect.y += 5
        self.prev_state = current_state.copy()
        self.prev_action = action
        self.prev_reward = current_reward
    def AI_actions(self, action):
        if action[0] > 0 and self.game.game_logic.player_two.rect.top > 0: self.game.game_logic.player_two.rect.y -= 5
        if action[0] < 0 and self.game.game_logic.player_two.rect.bottom < self.game.HEIGHT: self.game.game_logic.player_two.rect.y += 5
    def reset_qlearning_state(self):
        self.prev_state = None
        self.prev_action = None
        self.prev_reward = 0
    def manual_save_model(self):
        if self.game.config.config_AI["type_training"]["Genetic"]: save_genetic_model(self.model, torch.optim.Adam(self.model.parameters(), lr=0.001), self.model_path)
        elif self.game.config.config_AI["type_training"]["Q-learning"]: save_qlearning_model(self.model, torch.optim.Adam(self.model.parameters(), lr=0.001), self.model_path)