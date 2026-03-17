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
    def handle_state_changed(self, event: GameStateChangedEvent):
        self.current_state_dto = event.state_dto
        self.p1_score = event.p1_score
        self.p2_score = event.p2_score
    def images_elements(self, screen):
