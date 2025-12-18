import pygame
from pygame.locals import *
class InputHandler:
    def __init__(self, game):
        self.game = game
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == QUIT: self.game.event_quit()
            self._process_keydown_events(event)
            if self.game.main == 2: self.game.events_buttons(event)
            if self.game.main == 6: self.game.keys_menu.event_keys(event)
        self.game.pressed_keys = pygame.key.get_pressed()
        self.game.pressed_mouse = pygame.mouse.get_pressed()
