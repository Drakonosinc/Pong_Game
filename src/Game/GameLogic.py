import numpy as np
from src.Entities.Players import Player
from src.Entities.Balls import Ball
from src.Events.GameEvents import PlayerMoveEvent
from src.Core.Interfaces.ISoundService import IAudioService
from src.Core.Domain.Geometry import Rectangle
class GameLogic:
    def __init__(self, width, height, config_game, mode_game, audio_service: IAudioService, event_manager):
        self.width = width
        self.height = height
        self.config = config_game 
        self.mode_game = mode_game
        self.audio_service = audio_service # Port inyectado
        self.event_manager = event_manager
        self.init_entities()
        self.event_manager.subscribe(PlayerMoveEvent, self.handle_player_move)
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
    def _reset_ball(self, ball, reward, player):
        ball.rect = Rectangle(*ball.reset_position)
        self._repeat_collision(ball, reward)
        player.update_score(1)
    def _handle_collision(self, player, ball, index, reward):
        if player.check_collision(ball.rect):
            if player.active[index]:
                self._repeat_collision(ball, reward)
                player.active[index] = False
        else: player.active[index] = True
    def _repeat_collision(self, ball, reward):
        ball.handle_collision(self.player_two, reward)
        self.audio_service.play("collision")
    def reset_game(self):
        self.player_one.reset()
        self.player_two.reset()
        for ball in self.balls: ball.reset()
    def auto_play_player1(self):
        p1 = self.player_one
        if p1.rect.top > 0 or p1.rect.bottom < self.height: p1.rect.y += self.balls[0].move_y
        if p1.rect.y >= 310: p1.rect.y = 310
        if p1.rect.y <= 0: p1.rect.y = 0
    def get_state_vector(self):
        return np.array([self.player_one.rect.x, self.player_one.rect.y, self.player_two.rect.x, 
                        self.player_two.rect.y, self.balls[0].rect.x, self.balls[0].rect.y])