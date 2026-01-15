import pygame
from pygame.locals import *
class WindowManager:
    def __init__(self, title="Space Pong AI", width=1000, height=600):
        self.window_width = width
        self.window_height = height
        self.render_width = width   
        self.render_height = height
