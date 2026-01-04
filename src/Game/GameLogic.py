from pygame import Rect
from Entities import *
class GameLogic:
    def __init__(self, game):
        self.game = game
        self.width = game.WIDTH
        self.height = game.HEIGHT
    def init_entities(self):
        self.balls = [Ball(self.WIDTH//2-28,self.HEIGHT//2-29,36,36,4+i,4+i) for i in range(1 if self.mode_game["Training AI"] else self.config.config_game["number_balls"])]
        self.player_one = Player(25,150,11,90,[True] * len(self.balls))
        self.player_two = Player(665,150,11,90,[True] * len(self.balls))
    def update(self):
        for i, ball in enumerate(self.balls):
            ball.move_ball(self.width, self.height)
            if ball.rect.x >= self.width - 25: self._reset_ball(ball, -1, self.player_one)
            if ball.rect.x <= 0: self._reset_ball(ball, 1, self.player_two)
