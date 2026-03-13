import numpy as np
from src.Core.Interfaces.IAIModel import IAIModel
from src.Events.GameEvents import GameStateChangedEvent, ActionDecidedEvent
class AIHandler:
    def __init__(self, game):
        self.game = game
