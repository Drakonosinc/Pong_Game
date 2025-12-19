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
        self.game.mouse_pos = pygame.mouse.get_pos()
        self._process_continuous_presses()
    def _process_keydown_events(self, event):
        if event.type == KEYDOWN:
            if self.game.main == 3 and event.key == K_p: self.game.main = -1
            elif self.game.main == -1 and event.key == K_p: self.game.main = 3
            if self.game.main == 3 or self.game.main == -1:
                if self.game.speed_up and event.key == K_KP_PLUS: self.game.change_speed(15, 1, 10, "speed_up", speed_up=self.game.speed_up)
                if self.game.speed_down and event.key == K_KP_MINUS: self.game.change_speed(-15, -1, -1, "speed_down", speed_down=self.game.speed_down)
            if self.game.main == -1 and event.key == K_1: self.game.manual_save_model()
    def _process_continuous_presses(self):
        keys = self.game.pressed_keys
        if keys[K_ESCAPE]: self.game.running = False
        if self.game.main == -1 and (self.game.mode_game["Player"] or self.game.mode_game["AI"]):
