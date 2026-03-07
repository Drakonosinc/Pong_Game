import numpy as np
from src.Entities.Players import Player
from src.Entities.Balls import Ball
from src.Events.GameEvents import PlayerMoveEvent, GameStateChangedEvent, ActionDecidedEvent
from src.Core.Interfaces.ISoundService import IAudioService
from src.Core.Domain.Geometry import Rectangle
from src.Core.Domain.DTOs import WorldStateDTO
class GameLogic:
    def __init__(self, width, height, config_game, mode_game, audio_service: IAudioService, event_manager):
        self.width = width
        self.height = height
        self.config = config_game 
        self.mode_game = mode_game
        self.audio_service = audio_service
        self.event_manager = event_manager
        self.init_entities()
        self.event_manager.subscribe(PlayerMoveEvent, self.handle_player_move)
        self.event_manager.subscribe(ActionDecidedEvent, self.handle_action_decided)
    def init_entities(self):
        num_balls = 1 if self.mode_game["Training AI"] else self.config["number_balls"]
        self.balls = [Ball(self.width//2-28, self.height//2-29, 36, 36, 4+i, 4+i) for i in range(num_balls)]
        self.player_one = Player(25, 150, 11, 90, [True] * len(self.balls))
        self.player_two = Player(665, 150, 11, 90, [True] * len(self.balls))
    def handle_player_move(self, event: PlayerMoveEvent):
