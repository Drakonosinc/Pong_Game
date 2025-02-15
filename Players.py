from pygame import *
class Player:
    def __init__(self, x, y, width, height):
        self.rect = Rect(x, y, width, height)
        self.score=0
        self.reward=0
    def check_collision(self, other_rect):
        return self.rect.colliderect(other_rect)