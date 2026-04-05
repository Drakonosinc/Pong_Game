import pygame
from .Elements_interface import *
from Interface.Menus.Base_Menu import BaseMenu 
from Events.GameEvents import QuitEvent
from Loaders.AILoader import AILoader
class Interface(BaseMenu):
    def __init__(self, context):
        self.context = context
        self.game = None
        self.window = context.window_manager
        self._screen = context.window_manager.canvas 
        self.config = context.config
        self.WIDTH = self.config.config_visuals["WIDTH"]
        self.HEIGHT = self.config.config_visuals["HEIGHT"]
        self.clock = pygame.time.Clock()
        BaseMenu.__init__(self, self)
        self._sync_assets()
        self.setup_button_factories()
    def _sync_assets(self):
        assets = self.context.assets
        self.font_path = assets.font_path
        self.font = assets.font
        self.font2 = assets.font2
        self.font2_5 = assets.font2_5
        self.font3 = assets.font3
        self.font3_5 = assets.font3_5
        self.font3_8 = assets.font3_8
        self.font4 = assets.font4
