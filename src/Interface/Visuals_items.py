import pygame
class Visuals_items:
    def __init__(self, game): self.game = game
    def mode_speed(self): self.game.screen.blit(self.game.font.render(f"Speed: {self.game.speed}", True, self.game.YELLOW),(self.game.WIDTH//2-40,360))
    