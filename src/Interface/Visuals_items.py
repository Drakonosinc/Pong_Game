import pygame
from src.Events.GameEvents import GameStateChangedEvent
class Visuals_items:
    def __init__(self, game):
        self.game = game
        self.assets = game.context.assets
        self.ui = game.ui 
        self.current_state_dto = None
        self.p1_score = 0
        self.p2_score = 0
        self.game.event_manager.subscribe(GameStateChangedEvent, self.handle_state_changed)
