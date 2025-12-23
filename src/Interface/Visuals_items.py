import pygame
class Visuals_items:
    def __init__(self, game): self.game = game
    def mode_speed(self): self.game.screen.blit(self.game.font.render(f"Speed: {self.game.speed}", True, self.game.YELLOW),(self.game.WIDTH//2-40,360))
    def name_players(self):
        self.game.screen.blit(self.game.font.render(f"{self.game.input_player1.show_player()}", True, self.game.YELLOW),(45,360))
        self.game.screen.blit(self.game.font.render(f"{self.game.input_player2.show_player()}", True, self.game.YELLOW),(580,360))
    def draw_generation(self):
        if self.game.config.config_AI["type_training"]["Q-learning"]: self.game.screen.blit(self.game.font2.render(f"Episode: {self.game.generation}", True, self.game.YELLOW), (10, 10))
        else: self.game.screen.blit(self.game.font2.render(f"Generation: {self.game.generation}", True, self.game.YELLOW), (10, 10))
    def scores(self):
        self.screen.blit(self.font.render(f"Score {self.player_one.score}", True, self.YELLOW),(45,380))
        self.screen.blit(self.font.render(f"Score {self.player_two.score}", True, self.YELLOW),(580,380))