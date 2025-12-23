import pygame
class Visuals_items:
    def __init__(self, game): self.game = game
    def mode_speed(self): self.game.screen.blit(self.game.font.render(f"Speed: {self.game.speed}", True, self.game.YELLOW),(self.game.WIDTH//2-40,360))
    def name_players(self):
        self.game.screen.blit(self.game.font.render(f"{self.game.input_player1.show_player()}", True, self.game.YELLOW),(45,360))
        self.game.screen.blit(self.game.font.render(f"{self.game.input_player2.show_player()}", True, self.game.YELLOW),(580,360))
    def draw_generation(self):
        if self.config.config_AI["type_training"]["Q-learning"]: self.screen.blit(self.font2.render(f"Episode: {self.generation}", True, self.YELLOW), (10, 10))
        else: self.screen.blit(self.font2.render(f"Generation: {self.generation}", True, self.YELLOW), (10, 10))
    