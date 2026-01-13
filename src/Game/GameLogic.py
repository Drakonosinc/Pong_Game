from pygame import Rect
from Entities import *
class GameLogic:
    def __init__(self, game):
        self.game = game
        self.width = game.WIDTH
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
        else: player.active[index] = True
    def _repeat_collision(self, ball, reward):
        ball.handle_collision(self.player_two, reward)
        self.game.sound.play(loops=0)
    def reset_game(self):
        self.player_one.reset()
        self.player_two.reset()
        for ball in self.balls: ball.reset()
    def auto_play_player1(self):
        p1 = self.player_one
        if p1.rect.top > 0 or p1.rect.bottom < self.height: p1.rect.y += self.balls[0].move_y
        if p1.rect.y >= 310: p1.rect.y = 310
        if p1.rect.y <= 0: p1.rect.y = 0