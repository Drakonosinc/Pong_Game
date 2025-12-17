import pygame
from pygame.locals import *
class InputHandler:
    def __init__(self, game):
        self.game = game
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == QUIT: self.game.event_quit()
