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
        self.font4_5 = assets.font4_5
        self.font5 = assets.font5
        self.sound_buttonletters = assets.sound_buttonletters
        self.sound_touchletters = assets.sound_touchletters
        self.sound_exitbutton = assets.sound_exitbutton
        self.sound_back = assets.sound_back
        self.sound = assets.sound
        self.image = assets.image
        self.planet = assets.planet
        self.spacecraft = assets.spacecraft
        self.spacecraft2 = assets.spacecraft2
        self.GRAY = assets.GRAY
        self.SKYBLUE = assets.SKYBLUE
        self.RED = assets.RED
        self.BLACK = assets.BLACK
        self.WHITE = assets.WHITE
        self.GREEN = assets.GREEN
        self.BLUE = assets.BLUE
        self.YELLOW = assets.YELLOW
        self.GOLDEN = assets.GOLDEN
    def bind_game(self, game):
        self.game = game
    def __getattr__(self, name):
        assets = self.__dict__.get("context").assets if "context" in self.__dict__ else None
        if assets and hasattr(assets, name): return getattr(assets, name)
        game = self.__dict__.get("game")
        if game and hasattr(game, name): return getattr(game, name)
