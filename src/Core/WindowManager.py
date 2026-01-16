import pygame
from pygame.locals import *
class WindowManager:
    def __init__(self, title="Space Pong AI", width=1000, height=600):
        self.window_width = width
        self.window_height = height
        self.render_width = width   
        self.render_height = height
        self.fullscreen = False
        monitor_info = pygame.display.Info()
        self.monitor_width = monitor_info.current_w
        self.monitor_height = monitor_info.current_h
        self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
        pygame.display.set_caption(title)
        self.canvas = pygame.Surface((self.render_width, self.render_height))
    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
