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
    def handle_game_state_changed(self, event: GameStateChangedEvent):
        state_array = event.state_dto.to_array()
