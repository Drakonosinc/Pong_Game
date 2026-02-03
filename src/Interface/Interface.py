from .Elements_interface import *
from .Menus import *
from Utils.States import GameState
class Interface(BaseMenu):
    def __init__(self, context):
        BaseMenu.__init__(self, self)
        self.context = context
        self.window = context.window_manager
        self.screen = context.window_manager.canvas
        self.config = context.config
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
        self.initialize_menus()
    def initialize_menus(self):
        self.main_menu = MainMenu(self)
        self.game_over_menu = GameOver(self)
        self.game_mode_menu = GameMode(self)
        self.pause_menu = Pause(self)
        self.options_menu = OptionsMenu(self)
        self.visuals_menu = VisualsMenu(self)
        self.keys_menu = KeysMenu(self)
        self.menu_AI = AIMenu(self)
    def menus(self, current_state_enum):
        menu_routes = {
            GameState.MENU: self.main_menu.render,
            GameState.GAME_OVER: self.game_over_menu.render,
            GameState.MODE_SELECT: self.game_mode_menu.render,
            GameState.PAUSE: self.pause_menu.render,
            GameState.OPTIONS: self.options_menu.render,
            GameState.VISUALS: self.visuals_menu.render,
            GameState.KEYS: self.keys_menu.render,
            GameState.AI_MENU: self.menu_AI.render }
        if current_state_enum in menu_routes: menu_routes[current_state_enum]()
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
    def draw_buttons(self):
        self.setup_button_factories()
        self.main_menu.setup_buttons()
        self.game_over_menu.setup_buttons()
        self.game_mode_menu.setup_buttons()
        self.pause_menu.setup_buttons()
        self.options_menu.setup_buttons()
        self.visuals_menu.setup_buttons()
        self.keys_menu.setup_buttons()
        self.menu_AI.setup_buttons()
    def events_buttons(self, event):
        if hasattr(self, 'decrease_score_button'): self.decrease_score_button.reactivate_pressed(event)
        if hasattr(self, 'increase_score_button'): self.increase_score_button.reactivate_pressed(event)
        if hasattr(self, 'input_player1'): self.input_player1.change_text(event)
        if hasattr(self, 'input_player2'): self.input_player2.change_text(event)
        if hasattr(self, 'scroll'): self.scroll.events(event)
        if hasattr(self, 'box_type_training'): self.box_type_training.events(event)
        if hasattr(self, 'box_type_model'): self.box_type_model.events(event)