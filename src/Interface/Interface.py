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
    def menus(self):
        menu_routes = {
            0: self.main_menu.render,
            1: self.game_over_menu.render,
            2: self.game_mode_menu.render,
            3: self.pause_menu.render,
            4: self.options_menu.render,
            5: self.visuals_menu.render,}
        if self.main in menu_routes:menu_routes[self.main]()
    def setup_button_factories(self):
        self.button_factory_f5 = ElementsFactory({"screen": self.screen,"font": self.font5,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters})
        self.button_factory_f2_5 = ElementsFactory({"screen": self.screen,"font": self.font2_5,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters})
    def draw_buttons(self):
        self.setup_button_factories()
        self.main_menu.setup_buttons()
        self.game_over_menu.setup_buttons()
        self.game_mode_menu.setup_buttons()
        self.pause_menu.setup_buttons()
        self.options_menu.setup_buttons()
        self.visuals_menu.setup_buttons()
    def events_buttons(self,event):
        self.increase_score_button.reactivate_pressed(event)
        self.decrease_score_button.reactivate_pressed(event)
        self.input_player1.change_text(event)
        self.input_player2.change_text(event)
        self.scroll.events(event)
    def buttons_keys(self):
        self.back_keys_button = self.button_factory_f5.create_PolygonButton({"position": ((50, 350), (50, 380), (25, 365)),"position2":((50, 340), (50, 390), (10, 365)),"command1":lambda:self.change_mains({"main":4})})
        self.up_w_button=self.button_factory_f5.create_TextButton({"font": self.font4_5,"text": self.config.config_keys["Name_key1"],"position": (self.WIDTH/2-240,self.HEIGHT/2-170),"command1":lambda:self.change_keys("UP_W","Name_key1",self.up_w_button)})
        self.down_s_button=self.button_factory_f5.create_TextButton({"font": self.font4_5,"text": self.config.config_keys["Name_key2"],"position": (self.WIDTH/2-217,self.HEIGHT/2-20),"command1":lambda:self.change_keys("DOWN_S","Name_key2",self.down_s_button)})
        self.up_arrow_button=self.button_factory_f5.create_TextButton({"font": self.font4_5,"text": self.config.config_keys["Name_key3"],"position": (self.WIDTH/2+200,self.HEIGHT/2-170),"command1":lambda:self.change_keys("UP_ARROW","Name_key3",self.up_arrow_button)})
        self.down_arrow_button=self.button_factory_f5.create_TextButton({"font": self.font4_5,"text": self.config.config_keys["Name_key4"],"position": (self.WIDTH/2+200,self.HEIGHT/2-20),"command1":lambda:self.change_keys("DOWN_ARROW","Name_key4",self.down_arrow_button)})
        self.save_keys_button=self.button_factory_f5.create_TextButton({"text": "Save Config","position": (self.WIDTH/2+200,self.HEIGHT/2+140),"command1":self.config.save_config})
        self.default_keys_button=self.button_factory_f5.create_TextButton({"text": "Default config","position": (self.WIDTH/2+160,self.HEIGHT/2+160),"command1":lambda:(self.config.config(keys=True),self.change_mains({"main":6,"command":self.buttons_keys}))})
    def change_keys(self,key,key_name,button=None):
        self.key=key
        self.key_name=key_name
        self.button_key=button
        for k in self.utils_keys.keys():self.utils_keys[k]=False if k!=self.key else not self.utils_keys[self.key]
        self.check_item(self.utils_keys,self.SKYBLUE,self.WHITE,"color",**{"UP_W":self.up_w_button,"DOWN_S":self.down_s_button,"UP_ARROW":self.up_arrow_button,"DOWN_ARROW":self.down_arrow_button})
    def event_keys(self,event):
        if self.key!=None and (self.utils_keys[self.key] and event.type==KEYDOWN):
            self.config.config_keys[self.key]=event.key
            self.config.config_keys[self.key_name]=event.unicode.upper()
            self.check_item(self.config.config_keys,self.config.config_keys[self.key_name],self.WHITE,"text",**{self.key:self.button_key})
            self.change_keys(self.key,self.key_name)