from pygame import *
class Ball:
    def __init__(self, x, y, width, height, speedx, speedy):
        self.rect = Rect(x, y, width, height)
        self.move_x = speedx
        self.move_y = speedy
        self.reset_position = (x, y, width, height)
    def move_ball(self,WIDTH,HEIGHT):
        if self.rect.x>=WIDTH-25 or self.rect.x<=0:self.move_x*=-1
        if self.rect.y>=HEIGHT-25 or self.rect.y<=0:self.move_y*=-1
        self.rect.x+=self.move_x
        self.rect.y+=self.move_y
    def reset(self):
        self.rect = Rect(*self.reset_position)
        self.move_x *= -1
    def check_collision(self, other_rect):
        return self.rect.colliderect(other_rect)
    def handle_collision(self, player, reward):
        self.move_x *= -1
        player.reward += reward