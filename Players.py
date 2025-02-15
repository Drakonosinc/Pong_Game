from pygame import *
class Player:
    def __init__(self, x, y, width, height):
        self.rect = Rect(x, y, width, height)