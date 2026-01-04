from pygame import Rect
from Entities import *
class GameLogic:
    def __init__(self, game):
        self.game = game
        self.init_entities()
    def init_entities(self):
        self.balls = [Ball(self.game.WIDTH//2-28,self.game.HEIGHT//2-29,36,36,4+i,4+i) for i in range(1 if self.game.mode_game["Training AI"] else self.game.config.config_game["number_balls"])]
        self.player_one = Player(25,150,11,90,[True] * len(self.balls))
        self.player_two = Player(665,150,11,90,[True] * len(self.balls))
    def update(self):
        for i, ball in enumerate(self.balls):
            ball.move_ball(self.width, self.height)
            if ball.rect.x >= self.width - 25: self._reset_ball(ball, -1, self.player_one)
            if ball.rect.x <= 0: self._reset_ball(ball, 1, self.player_two)
            self._handle_collision(self.player_one, ball, i, -1)
            self._handle_collision(self.player_two, ball, i, 1)
    def _reset_ball(self, ball, reward, player):
        ball.rect = Rect(*ball.reset_position)
        self._repeat_collision(ball, reward)
        player.update_score(1)
    def _handle_collision(self, player, ball, index, reward):
        if player.check_collision(ball):
            if player.active[index]:
                self._repeat_collision(ball, reward)
                player.active[index] = False