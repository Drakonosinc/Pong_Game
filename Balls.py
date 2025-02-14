from pygame import *
class Ball:
    def __init__(self, x, y, width, height):
        self.rect = Rect(x, y, width, height)
        self.move_x = 0
        self.move_y = 0
    def move_ball(self,sound=None):
        if self.rect.x>=self.WIDTH-25 or self.rect.x<=0:
            self.move_x*=-1
            if sound is not None:sound.play(loops=1)
            def repeat():self.rect.x,self.rect.y=300,200
            if self.object3.x>=self.WIDTH-25 or self.object3.x<=0:repeat()
        if self.rect.y>=self.HEIGHT-25 or self.rect.y<=0:self.move_y*=-1
    def check_collision(self, other_rect):
        return self.rect.colliderect(other_rect)
    def reset(self, x, y):
        self.rect.x, self.rect.y = x, y
    def check_collision(self, other_rect):
        return self.rect.colliderect(other_rect)