import pygame
from .Elements_interface import *
from Interface.Menus.Base_Menu import BaseMenu 
from Events.GameEvents import QuitEvent
class Interface(BaseMenu):
    def __init__(self, context):
        self.context = context
        self.window = context.window_manager
        self._screen = context.window_manager.canvas 
        self.config = context.config
        self.WIDTH = self.config.config_visuals["WIDTH"]
        self.HEIGHT = self.config.config_visuals["HEIGHT"]
        self.clock = pygame.time.Clock()
        BaseMenu.__init__(self, self)
        assets = context.assets
        self.font = assets.font
        self.font2 = assets.font2
        self.font2_5 = assets.font2_5
        self.font3 = assets.font3
        self.font4 = assets.font4
        self.font5 = assets.font5
        self.sound_buttonletters = assets.sound_buttonletters
        self.sound_touchletters = assets.sound_touchletters
        self.sound_exitbutton = assets.sound_exitbutton
        self.sound = assets.sound
        self.image = assets.image
        self.planet = assets.planet
        self.spacecraft = assets.spacecraft
        self.spacecraft2 = assets.spacecraft2
        self.SKYBLUE = assets.SKYBLUE
        self.RED = assets.RED
        self.BLACK = assets.BLACK
        self.WHITE = assets.WHITE
        self.YELLOW = assets.YELLOW
        self.setup_button_factories()
    @property
    def screen(self): return self._screen
    def setup_button_factories(self):
        self.button_factory_f5 = ElementsFactory({
            "screen": self.screen, 
            "window": self.window,
            "font": self.font5,
            "sound_hover": self.sound_buttonletters,
            "sound_touch": self.sound_touchletters})
        self.button_factory_f2_5 = ElementsFactory({
            "screen": self.screen,
            "window": self.window,
            "font": self.font2_5,
            "sound_hover": self.sound_buttonletters,
            "sound_touch": self.sound_touchletters})
    def events_buttons(self, event):
        if hasattr(self, 'decrease_score_button'): self.decrease_score_button.reactivate_pressed(event)
        if hasattr(self, 'increase_score_button'): self.increase_score_button.reactivate_pressed(event)
        if hasattr(self, 'input_player1'): self.input_player1.change_text(event)
        if hasattr(self, 'input_player2'): self.input_player2.change_text(event)
        if hasattr(self, 'scroll'): self.scroll.events(event)
        if hasattr(self, 'box_type_training'): self.box_type_training.events(event)
        if hasattr(self, 'box_type_model'): self.box_type_model.events(event)
    def event_quit(self): self.context.event_manager.post(QuitEvent())