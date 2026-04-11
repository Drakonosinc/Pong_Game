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
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
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
    def config_screen(self):
        new_w = self.config.config_visuals["WIDTH"]
        new_h = self.config.config_visuals["HEIGHT"]
        self.window.window_width = new_w
        self.window.window_height = new_h
        if not self.window.fullscreen: self.window.screen = pygame.display.set_mode((new_w, new_h), pygame.RESIZABLE)
        self.WIDTH = self.window.render_width
        self.HEIGHT = self.window.render_height
        self.context.assets.reload_graphics()
        self._screen = self.window.canvas
        self._sync_assets()
        self.setup_button_factories()
    def load_AI(self):
        model_training = AILoader(self.context).load_model()
        self.model_training = model_training
        if self.game:
            self.game.model_training = model_training
            if getattr(self.game, "ai_handler", None): self.game.ai_handler.set_runtime_model(model_training)
        return model_training
    def events_buttons(self, event):
        if hasattr(self, 'decrease_score_button'): self.decrease_score_button.reactivate_pressed(event)
        if hasattr(self, 'increase_score_button'): self.increase_score_button.reactivate_pressed(event)
        if hasattr(self, 'input_player1'): self.input_player1.change_text(event)
        if hasattr(self, 'input_player2'): self.input_player2.change_text(event)
        if hasattr(self, 'scroll'): 