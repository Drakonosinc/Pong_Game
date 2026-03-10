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
        velocity = 5
        target_player = None
        if event.player_index == 1: target_player = self.player_one
        elif event.player_index == 2: target_player = self.player_two
        if target_player:
            if event.direction == -1 and target_player.rect.top > 0: target_player.rect.y -= velocity
            elif event.direction == 1 and target_player.rect.bottom < self.height: target_player.rect.y += velocity
    def update(self):
        for i, ball in enumerate(self.balls):
            ball.move_ball(self.width, self.height)
            if ball.rect.x >= self.width - 25: self._reset_ball(ball, -1, self.player_one)
            if ball.rect.x <= 0: self._reset_ball(ball, 1, self.player_two)
            self._handle_collision(self.player_one, ball, i, -1)
            self._handle_collision(self.player_two, ball, i, 1)
        if self.mode_game["Training AI"] or self.mode_game["AI"]: self.emit_state()
    def emit_state(self):
        dto = WorldStateDTO(
            p1_x=self.player_one.rect.x, p1_y=self.player_one.rect.y,
            p2_x=self.player_two.rect.x, p2_y=self.player_two.rect.y,
            ball_x=self.balls[0].rect.x, ball_y=self.balls[0].rect.y)
        self.event_manager.post(GameStateChangedEvent(
            state_dto=dto,
            player_two_reward=self.player_two.reward,
            p1_score=self.player_one.score,
            p2_score=self.player_two.score))
    def handle_action_decided(self, event: ActionDecidedEvent):
        action = event.action
        p2 = self.player_two
        if isinstance(action, (int, np.integer)):
            if action == 0 and p2.rect.top > 0: p2.rect.y -= 5
            elif action == 1 and p2.rect.bottom < self.height: p2.rect.y += 5
        else:
            if action[0] > 0 and p2.rect.top > 0: p2.rect.y -= 5
            if action[0] < 0 and p2.rect.bottom < self.height: p2.rect.y += 5
    def _reset_ball(self, ball, reward, player):
        ball.rect = Rectangle(*ball.reset_position)
        self._repeat_collision(ball, reward)
        