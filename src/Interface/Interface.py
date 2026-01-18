from Loaders.Load_elements import *
from .Elements_interface import *
from .Menus import *
class interface(load_elements,BaseMenu):
    def __init__(self):
        load_elements.__init__(self)
        BaseMenu.__init__(self,self)
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
    def menus(self):
        menu_routes = {
            0: self.main_menu.render,
            1: self.game_over_menu.render,
            2: self.game_mode_menu.render,
            3: self.pause_menu.render,
            4: self.options_menu.render,
            5: self.visuals_menu.render,
            6: self.keys_menu.render,
            7: self.menu_AI.render}
        if self.main in menu_routes:menu_routes[self.main]()
    def setup_button_factories(self):
        self.button_factory_f5 = ElementsFactory({"screen": self.screen, "window": self.window,"font": self.font5,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters})
        self.button_factory_f2_5 = ElementsFactory({"screen": self.screen,"font": self.font2_5,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters})
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
    def events_buttons(self,event):
        self.decrease_score_button.reactivate_pressed(event)
        self.increase_score_button.reactivate_pressed(event)
        self.input_player1.change_text(event)
        self.input_player2.change_text(event)
        self.scroll.events(event)
        self.box_type_training.events(event)
        self.box_type_model.events(event)