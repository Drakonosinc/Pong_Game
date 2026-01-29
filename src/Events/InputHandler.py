import pygame
from pygame.locals import *
from Utils.States import GameState
from .GameEvents import *
class InputHandler:
    def __init__(self, game, event_manager):
        self.game = game
        self.event_manager = event_manager
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == QUIT: self.event_manager.post(QuitEvent())
            self._process_keydown_events(event)
            self.game.state_manager.handle_event(event)
        self.game.pressed_keys = pygame.key.get_pressed()
        self.game.pressed_mouse = pygame.mouse.get_pressed()
        self.game.mouse_pos = pygame.mouse.get_pos()
        self._process_continuous_presses()
    def _process_keydown_events(self, event):
        if event.type == KEYDOWN:
            if event.key == K_F11: self.event_manager.post(ToggleFullscreenEvent())
            if self.game.main == GameState.PAUSE and event.key == K_p: self.event_manager.post(ResumeGameEvent())
            elif self.game.main == GameState.PLAYING and event.key == K_p: self.event_manager.post(PauseGameEvent())
            if self.game.main in [GameState.PAUSE, GameState.PLAYING]:
                if self.game.speed_up and event.key == K_KP_PLUS: self.event_manager.post(ChangeSpeedEvent(15, 1, 10, "speed_up"))
                if self.game.speed_down and event.key == K_KP_MINUS: self.event_manager.post(ChangeSpeedEvent(-15, -1, -1, "speed_down"))
            if self.game.main == GameState.PLAYING and event.key == K_1: self.event_manager.post(SaveModelEvent())
    def _process_continuous_presses(self):
        keys = self.game.pressed_keys
        if keys[K_ESCAPE]: self.game.running = False
        if self.game.main == GameState.PLAYING:
            config_keys = self.game.config.config_keys
            if self.game.mode_game["Player"] or self.game.mode_game["AI"]:
                if keys[config_keys["UP_W"]]: self.event_manager.post(PlayerMoveEvent(player_index=1, direction=-1))
                if keys[config_keys["DOWN_S"]]: self.event_manager.post(PlayerMoveEvent(player_index=1, direction=1))
            if self.game.mode_game["Player"]:
                if keys[config_keys["UP_ARROW"]]: self.event_manager.post(PlayerMoveEvent(player_index=2, direction=-1))
                if keys[config_keys["DOWN_ARROW"]]: self.event_manager.post(PlayerMoveEvent(player_index=2, direction=1))
        if self.game.main == GameState.GAME_OVER:
            if keys[K_r]: self.event_manager.post(ChangeStateEvent({"main": GameState.PLAYING, "reset": True}))
            if keys[K_e]: self.event_manager.post(ChangeStateEvent({"main": GameState.MENU, "run": True}))