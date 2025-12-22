import pygame
class Visuals_items:
    def __init__(self, game): self.game = game
    def mode_speed(self): self.game.screen.blit(self.game.font.render(f"Speed: {self.game.speed}", True, self.game.YELLOW),(self.game.WIDTH//2-40,360))
    def name_players(self):
        self.screen.blit(self.font.render(f"{self.input_player1.show_player()}", True, self.YELLOW),(45,360))
        self.screen.blit(self.font.render(f"{self.input_player2.show_player()}", True, self.YELLOW),(580,360))