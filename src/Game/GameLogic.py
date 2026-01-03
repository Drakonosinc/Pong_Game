from pygame import Rect

class GameLogic:
    def __init__(self, game):
        self.game = game
        self.width = game.WIDTH
        self.height = game.HEIGHT
    def init_entities(self):
        self.balls = [Ball(self.WIDTH//2-28,self.HEIGHT//2-29,36,36,4+i,4+i) for i in range(1 if self.mode_game["Training AI"] else self.config.config_game["number_balls"])]
        self.player_one = Player(25,150,11,90,[True] * len(self.balls))
        self.player_two = Player(665,150,11,90,[True] * len(self.balls))