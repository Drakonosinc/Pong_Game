import numpy as np
from src.Core.Interfaces.IAIModel import IAIModel
from src.Events.GameEvents import GameStateChangedEvent, ActionDecidedEvent
class AIHandler:
    def __init__(self, game):
        self.game = game
        self.prev_state = None
        self.prev_action = None
        self.prev_reward = 0
        self.model_adapter: IAIModel = None 
        self.game.event_manager.subscribe(GameStateChangedEvent, self.handle_game_state_changed)
    def set_model(self, model_adapter: IAIModel): 
        self.model_adapter = model_adapter
    def set_runtime_model(self, model):
        if model is None: return
        if isinstance(model, IAIModel):
            self.model_adapter = model
            return
        current_model = self.model_adapter.get_internal_model() if self.model_adapter else None
        if current_model is model: return
        type_model = self.game.config.config_AI.get("type_model", {})
        if type_model.get("Pytorch", False):
            from src.Infrastructure.AI.Adapters.PyTorchAdapter import PyTorchAdapter
            self.model_adapter = PyTorchAdapter(model)
        elif type_model.get("Tensorflow", False):
            from src.Infrastructure.AI.Adapters.TensorFlowAdapter import TensorFlowAdapter
            self.model_adapter = TensorFlowAdapter(model)

    def handle_game_state_changed(self, event: GameStateChangedEvent):
        state_array = event.state_dto.to_array()
        if self.game.config.config_AI["type_training"]["Q-learning"]: self._qlearning_actions(state_array, event.reward, event.p1_score, event.p2_score)
        else:
            if not self.model_adapter: return
            action = self.model_adapter.predict(state_array)
            self.game.event_manager.post(ActionDecidedEvent(action))
    def _qlearning_actions(self, current_state, current_reward, p1_score, p2_score):
        from src.Type_Training.Q_learning import _qlearning_trainer
        if _qlearning_trainer is None: return
        if self.prev_state is not None and self.prev_action is not None:
            reward = current_reward - self.prev_reward
            max_score = self.game.config.config_game["max_score"]
            done = (p1_score >= max_score or p2_score >= max_score)
            _qlearning_trainer.store_experience(self.prev_state, self.prev_action, reward, current_state, done)
        action = _qlearning_trainer.get_action(current_state)
        self.game.event_manager.post(ActionDecidedEvent(action))
        self.prev_state = current_state.copy()
        self.prev_action = action
        self.prev_reward = current_reward
    def reset_qlearning_state(self):
        self.prev_state = None
        self.prev_action = None
        self.prev_reward = 0
    def manual_save_model(self):
        if self.model_adapter: self.model_adapter.save(self.game.model_path)