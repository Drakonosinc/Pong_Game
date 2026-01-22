import pygame
from pygame.locals import *
from Utils.States import GameState
class InputHandler:
    def __init__(self, game):
        self.game = game
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == QUIT: self.game.event_quit()
            self._process_keydown_events(event)
            if self.game.main == GameState.MODE_SELECT: self.game.events_buttons(event)
            if self.game.main == GameState.KEYS: self.game.keys_menu.event_keys(event)
        self.game.pressed_keys = pygame.key.get_pressed()
        self.game.pressed_mouse = pygame.mouse.get_pressed()
        self.game.mouse_pos = pygame.mouse.get_pos()
        self._process_continuous_presses()
    def _process_keydown_events(self, event):
        if event.type == KEYDOWN:
            if event.key == K_F11: self.game.window.toggle_fullscreen()
            if self.game.main == GameState.PAUSE and event.key == K_p: self.game.main = GameState.PLAYING
            elif self.game.main == GameState.PLAYING and event.key == K_p: self.game.main = GameState.PAUSE
            if self.game.main == GameState.PAUSE or self.game.main == GameState.PLAYING:
                if self.game.speed_up and event.key == K_KP_PLUS: self.game.change_speed(15, 1, 10, "speed_up", speed_up=self.game.speed_up)
                if self.game.speed_down and event.key == K_KP_MINUS: self.game.change_speed(-15, -1, -1, "speed_down", speed_down=self.game.speed_down)
            if self.game.main == GameState.PLAYING and event.key == K_1: self.game.ai_handler.manual_save_model()
    def _process_continuous_presses(self):
        keys = self.game.pressed_keys
        if keys[K_ESCAPE]: self.game.running = False
        if self.game.main == GameState.PLAYING and (self.game.mode_game["Player"] or self.game.mode_game["AI"]):
            p1 = self.game.game_logic.player_one
            if keys[self.game.config.config_keys["UP_W"]] and p1.rect.top > 0: p1.rect.y -= 5
            if keys[self.game.config.config_keys["DOWN_S"]] and p1.rect.bottom < self.game.HEIGHT: p1.rect.y += 5
        if self.game.main == GameState.PLAYING and self.game.mode_game["Player"]:
            p2 = self.game.game_logic.player_two
            if keys[self.game.config.config_keys["UP_ARROW"]] and p2.rect.top > 0: p2.rect.y -= 5
            if keys[self.game.config.config_keys["DOWN_ARROW"]] and p2.rect.bottom < self.game.HEIGHT: p2.rect.y += 5
        if self.game.main == GameState.GAME_OVER:
            if keys[K_r]: self.game.change_mains({"main": GameState.PLAYING})
            if keys[K_e]: self.game.change_mains({"main": GameState.MENU, "run": True})