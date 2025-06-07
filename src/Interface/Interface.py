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
        self.game_mode_menu = Game_Mode(self)
    def menus(self):
        menu_routes = {
            0: self.main_menu.render,
            1: self.game_over_menu.render,
            2: self.game_mode_menu.render,}
        if self.main==3:self.Pause()
        elif self.main==4:self.options_menu()
        elif self.main==5:self.visuals_menu()
        elif self.main==6:self.menu_keys()
        if self.main in menu_routes:menu_routes[self.main]()
    def setup_button_factories(self):
        self.button_factory_f5 = ElementsFactory({"screen": self.screen,"font": self.font5,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters})
        self.button_factory_f2_5 = ElementsFactory({"screen": self.screen,"font": self.font2_5,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters})
    def draw_buttons(self):
        self.setup_button_factories()
        self.main_menu.setup_buttons()
        self.game_over_menu.setup_buttons()
        self.game_mode_menu.setup_buttons()
        self.buttons_pausa()
        self.buttons_menu_options()
        self.buttons_visual()
        self.buttons_keys()
    def events_buttons(self,event):
        self.increase_score_button.reactivate_pressed(event)
        self.decrease_score_button.reactivate_pressed(event)
        self.input_player1.change_text(event)
        self.input_player2.change_text(event)
        self.scroll.events(event)
    def game_mode(self):
        self.screen.blit(font_modegame.render("Max Score",True,"white"),(self.WIDTH/2-68,self.HEIGHT/2-50))
        self.screen.blit(font_modegame.render(f"{self.config.config_game["max_score"]}",True,"white"),(self.WIDTH/2-8,self.HEIGHT/2-20))
        self.main_training_ai() if self.mode_game["Training AI"] else self.options_game()
        self.execute_buttons(self.back_button,self.continue_button,self.training_ai_button,self.player_button,self.ai_button,self.decrease_score_button,self.increase_score_button,self.input_player1,self.input_player2)
        self.decrease_score_button.change_item({"pressed": (x:=self.config.config_game["max_score"] > 1),"detect_mouse": x})
    def main_training_ai(self):
        self.save_model.change_item({"color":self.SKYBLUE if self.config.config_AI["model_save"] else self.RED,"text":"ON" if self.config.config_AI["model_save"] else "OFF"})
    def options_game(self):
        self.screen.blit(self.font5.render(f"Configuration of\n{"Gameplay":^23}", True, "White"),(self.WIDTH/2+120,self.HEIGHT/2-136))
        self.screen.blit(self.font5.render(f"Number of Balls\n{self.config.config_game['number_balls']:^{28 if self.config.config_game['number_balls']<10 else 26}}", True, "White"),(self.WIDTH/2+120,self.HEIGHT/2-81))
        self.execute_buttons(self.increase_balls,self.decrease_balls)
    def Pause(self):
        self.filt(180)
        self.screen.blit(self.font3.render("Pause",True,"gray"),(self.WIDTH/2-105,self.HEIGHT/2-150))
        self.execute_buttons(self.exit_button,self.reset_pause_button,self.go_main_button)
    def buttons_pausa(self):
        self.exit_button=self.button_factory_f2_5.create_TextButton({"text": "Exit","color": self.GRAY,"position": (self.WIDTH/2-40,self.HEIGHT/2-15),"color2": self.SKYBLUE,"sound_touch":None,"command1":self.event_quit})
        self.reset_pause_button=self.button_factory_f2_5.create_TextButton({"text": "Reset","color": self.GRAY,"position": (self.WIDTH/2-55,self.HEIGHT/2-85),"color2": self.SKYBLUE,"command1":lambda:self.change_mains({"main":-1}),"command2":self.reset})
        self.go_main_button=self.button_factory_f2_5.create_TextButton({"text": "Menu","color": self.GRAY,"position": (self.WIDTH/2-45,self.HEIGHT/2-50),"color2": self.SKYBLUE,"command1":lambda:self.change_mains({"main":0,"run":True}),"command2":self.reset})
    def options_menu(self):
        self.screen.fill(self.BLACK)
        self.sound_button.change_item({"color":self.sound_type["color"],"text":self.sound_type["sound"]})
        self.execute_buttons(self.back_button,self.visual_button,self.sound_button,self.keys_button,self.language_button)
    def buttons_menu_options(self):
        self.back_button = self.button_factory_f5.create_PolygonButton({"position": ((50, 350), (50, 380), (25, 365)),"position2":((50, 340), (50, 390), (10, 365)),"command1":lambda:self.change_mains({"main":0})})
        self.visual_button=self.button_factory_f2_5.create_TextButton({"text": "Visuals","position": (self.WIDTH/2-80,self.HEIGHT/2-150),"command1":lambda:self.change_mains({"main":5})})
        self.sound_button=self.button_factory_f2_5.create_TextButton({"text": self.sound_type["sound"],"color": self.sound_type["color"],"position": (self.WIDTH/2-80,self.HEIGHT/2-115),"command1":lambda:self.on_off(self.config.config_sounds,"sound_main"),"command2":self.sound_on_off,"command3":self.config.save_config})
        self.keys_button=self.button_factory_f2_5.create_TextButton({"text": "Keys","position": (self.WIDTH/2-80,self.HEIGHT/2-80),"command1":lambda:self.change_mains({"main":6})})
        self.language_button=self.button_factory_f2_5.create_TextButton({"text": "Language","position": (self.WIDTH/2-80,self.HEIGHT/2-45)})
    def sound_on_off(self):
        self.sound_type["value"]=not self.sound_type["value"]
        def sound(color,sound_on_off,sound):
            self.sound_type["color"]=color
            self.sound_type["sound"]=sound_on_off
            sound.play(loops=-1) if color==self.SKYBLUE else sound.stop()
        sound(*(self.SKYBLUE,"Sound ON",self.sound_back) if self.sound_type["value"] else (self.RED,"Sound off",self.sound_back))
    def visuals_menu(self):
        self.screen.blit(self.image, (0, 0))
        self.screen.blit(self.font2_5.render("WIDTH",True,self.SKYBLUE),(self.WIDTH/2-163,self.HEIGHT/2-200))
        self.screen.blit(self.font2_5.render("HEIGHT",True,self.SKYBLUE),(self.WIDTH/2+60,self.HEIGHT/2-200))
        self.screen.blit(self.font2_5.render("IMAGE",True,self.SKYBLUE),(self.WIDTH/2-52,self.HEIGHT/2+160))
        self.images_elements()
        self.execute_buttons(self.back_visual_button,self.decrease_width_button,self.increase_width_button,self.decrease_height_button,self.increase_height_button,self.decrease_planet_button,self.increase_planet_button,self.decrease_back_button,self.increase_back_button,self.decrease_player1_button,self.increase_player1_button,self.decrease_player2_button,self.increase_player2_button,self.save_visual_button,self.default_visual_button)
    def buttons_visual(self):
        self.back_visual_button = self.button_factory_f5.create_PolygonButton({"position": ((50, 350), (50, 380), (25, 365)),"position2":((50, 340), (50, 390), (10, 365)),"command1":lambda:self.change_mains({"main":4})})
        self.decrease_width_button=self.button_factory_f2_5.create_TextButton({"text": "<","position": (self.WIDTH/2-200,self.HEIGHT/2-200),"command1":lambda:self.change_items("WIDTH",number=-10)})
        self.increase_width_button=self.button_factory_f2_5.create_TextButton({"text": ">","position": (self.WIDTH/2-40,self.HEIGHT/2-200),"command1":lambda:self.change_items("WIDTH",number=10)})
        self.decrease_height_button=self.button_factory_f2_5.create_TextButton({"text": "<","position": (self.WIDTH/2+20,self.HEIGHT/2-200),"command1":lambda:self.change_items("HEIGHT",number=-10)})
        self.increase_height_button=self.button_factory_f2_5.create_TextButton({"text": ">","position": (self.WIDTH/2+200,self.HEIGHT/2-200),"command1":lambda:self.change_items("HEIGHT",number=10)})
        self.decrease_planet_button=self.button_factory_f2_5.create_TextButton({"text": "<","position": (self.WIDTH/2-40,self.HEIGHT/2-22),"command1":lambda:self.change_items("value_planet","planets",-1)})
        self.increase_planet_button=self.button_factory_f2_5.create_TextButton({"text": ">","position": (self.WIDTH/2+20,self.HEIGHT/2-22),"command1":lambda:self.change_items("value_planet","planets",1)})
        self.decrease_back_button=self.button_factory_f2_5.create_TextButton({"text": "<","position": (self.WIDTH/2-80,self.HEIGHT/2+160),"command1":lambda:self.change_items("value_background","image_background",-1)})
        self.increase_back_button=self.button_factory_f2_5.create_TextButton({"text": ">","position": (self.WIDTH/2+65,self.HEIGHT/2+160),"command1":lambda:self.change_items("value_background","image_background",1)})
        self.decrease_player1_button=self.button_factory_f2_5.create_TextButton({"font": self.font3_5,"text": "Λ","position": (self.WIDTH/2-330,self.HEIGHT/2-120),"command1":lambda:self.change_items("value_spacecraft1","spacecrafts",-1)})
        self.increase_player1_button=self.button_factory_f2_5.create_TextButton({"font": self.font3_8,"text": "v","position": (self.WIDTH/2-330,self.HEIGHT/2+50),"command1":lambda:self.change_items("value_spacecraft1","spacecrafts",1)})
        self.decrease_player2_button=self.button_factory_f2_5.create_TextButton({"font": self.font3_5,"text": "Λ","position": (self.WIDTH/2+310,self.HEIGHT/2-120),"command1":lambda:self.change_items("value_spacecraft2","spacecrafts",-1)})
        self.increase_player2_button=self.button_factory_f2_5.create_TextButton({"font": self.font3_8,"text": "v","position": (self.WIDTH/2+310,self.HEIGHT/2+50),"command1":lambda:self.change_items("value_spacecraft2","spacecrafts",1)})
        self.save_visual_button=self.button_factory_f5.create_TextButton({"text": "Save Config","position": (self.WIDTH/2+200,self.HEIGHT/2+140),"command1":self.config.save_config})
        self.default_visual_button=self.button_factory_f5.create_TextButton({"text": "Default config","position": (self.WIDTH/2+160,self.HEIGHT/2+160),"command1":lambda:self.config.config(visuals=True),"command2":self.config_screen})
    def change_items(self,item,background=None,number=0):
        self.config.config_visuals[item]=((self.config.config_visuals[item] + number) % len(self.config.config_visuals[background])) if background!=None else (self.config.config_visuals[item] + number)
        self.config_screen()
    def menu_keys(self):
        self.screen.fill(self.BLACK)
        self.execute_buttons(self.back_keys_button,self.up_w_button,self.down_s_button,self.up_arrow_button,self.down_arrow_button,self.save_keys_button,self.default_keys_button)
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