import pygame
class Visuals_items:
    def __init__(self, game):
        self.game = game
    def mode_speed(self): self.screen.blit(self.font.render(f"Speed: {self.speed}", True, self.YELLOW),(self.WIDTH//2-40,360))
    