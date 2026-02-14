from src.Core.Domain.Geometry import Rectangle
class Player:
    def __init__(self, x, y, width, height, active):
        self.rect = Rectangle(x, y, width, height)
        self.active = active
        self.score = 0
        self.reward = 0
        self.reset_position = (x, y, width, height)
    def reset(self):
        self.rect = Rectangle(*self.reset_position)
        self.active = [True] * len(self.active)
        self.score = 0
    def check_collision(self, other_rect): return self.rect.colliderect(other_rect)
    def update_score(self, score): self.score += score