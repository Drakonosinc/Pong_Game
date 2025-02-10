from Load_elements import *
from Button import *
class interface(load_elements):
    def menus(self):
        self.Pause()
        self.main_menu()
        self.game_mode()
        self.options_menu()
        self.visuals_menu()
        self.menu_keys()
        self.Game_over()
    def draw_buttons(self):
        self.button_factory_f5 = ButtonFactory({"screen": self.screen,"font": self.font5,"hover_color": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters})
        self.button_factory_f2_5 = self.button_factory_f5.change_item({"font": self.font2_5})
        self.buttons_game_over()
        self.buttons_mode_game()
        self.buttons_pausa()
        self.buttons_menu_options()
        self.buttons_visual()
        self.buttons_keys()
    def events_buttons(self,event):
        if self.main==2:
            self.increase_score_button.reactivate_pressed(event)
            self.decrease_score_button.reactivate_pressed(event)
    def execute_buttons(self,*args):
        for button in args:button.draw()
    def main_menu(self):
        if self.main==0:
            self.screen.fill(self.BLACK)
            self.screen.blit(self.font4.render("Space Pong", True, self.WHITE),(self.WIDTH//2-245,self.HEIGHT//2-180))
            self.execute_buttons(self.play_button,self.quit_button,self.options_button)
    def buttons_main_menu(self):
        self.play_button = self.button_factory_f5.create_TextButton({"text": "Press To Start","position": (self.WIDTH//2-200,self.HEIGHT//2-80),"command1":lambda:self.change_mains({"main":2})})
        self.quit_button = self.button_factory_f5.create_TextButton({"text": "Press To Exit","position": (self.WIDTH//2-200,self.HEIGHT//2-50),"sound_touch":self.sound_exitbutton,"command1": self.event_quit})
        self.options_button = self.button_factory_f5.create_TextButton({"text": "Options","position": (self.WIDTH-110,self.HEIGHT-40),"command1":lambda:self.change_mains({"main":4})})
    def Game_over(self):
        if self.main==1:
            self.filt(80)
            pygame.draw.rect(self.screen,"black",(0,0,700,400),15)
            self.screen.blit(self.font3.render("GAME OVER",True,"black"),(self.WIDTH/2-178,self.HEIGHT/2-180))
            self.execute_buttons(self.main_button,self.reset_button)
    def buttons_game_over(self):
        self.main_button=self.button_factory_f2_5.create_TextButton({"text": "Main Menu Press E","color": self.BLACK,"position": (self.WIDTH/2-166,self.HEIGHT/2-110),"command1":lambda:self.change_mains({"main":0,"run":True})})
        self.reset_button=self.button_factory_f2_5.create_TextButton({"text": "Reset Press R","color": self.BLACK,"position": (self.WIDTH/2-130,self.HEIGHT/2-80),"command1": self.reset,"command2":lambda:self.change_mains({"main":-1})})
    def game_mode(self):
        if self.main==2:
            self.screen.fill(self.BLACK)
            self.screen.blit((font_modegame:=pygame.font.Font(os.path.join(self.font_path,"8bitOperatorPlusSC-Bold.ttf"),22)).render("Game Mode",True,"white"),(self.WIDTH/2-70,self.HEIGHT/2-162))
            self.screen.blit(self.font5.render("Enter Player Name One",True,"white"),(7,10))
            self.screen.blit(self.font5.render("Enter Player Name Two",True,"white"),(416,10))
            pygame.draw.rect(self.screen,self.color_inputtext1,(8,40,271,25))
            pygame.draw.rect(self.screen,self.color_inputtext2,(418,40,275,25))
            self.input_player1=pygame.draw.rect(self.screen,self.GRAY,(8,40,271,25),2)
            self.input_player2=pygame.draw.rect(self.screen,self.GRAY,(418,40,275,25),2)
            self.screen.blit(self.font5.render(self.text_player1, True, self.BLACK), (self.input_player1.x+5, self.input_player1.y-2))
            self.screen.blit(self.font5.render(self.text_player2, True, self.BLACK), (self.input_player2.x+5, self.input_player2.y-2))
            self.screen.blit(font_modegame.render("Max Score",True,"white"),(self.WIDTH/2-68,self.HEIGHT/2-50))
            self.screen.blit(font_modegame.render(f"{self.max_score}",True,"white"),(self.WIDTH/2-8,self.HEIGHT/2-20))
            if self.mode_game["Training AI"]:self.main_training_ai()
            if self.pressed_mouse[0]:
                self.color_inputtext1=self.SKYBLUE if self.input_player1.collidepoint(self.mouse_pos) else self.WHITE
                self.color_inputtext2=self.SKYBLUE if self.input_player2.collidepoint(self.mouse_pos) else self.WHITE
            self.execute_buttons(self.back_button,self.continue_button,self.training_ai_button,self.player_button,self.ai_button,self.decrease_score_button,self.increase_score_button)
            self.decrease_score_button.change_item({"pressed": (x:=self.max_score > 1),"detect_mouse": x})
    def buttons_mode_game(self):
        self.back_button = self.button_factory_f5.create_PolygonButton({"position": ((50, 350), (50, 380), (25, 365)),"position2":((50, 340), (50, 390), (10, 365)),"command1":lambda:self.change_mains({"main":0})})
        self.continue_button = self.button_factory_f5.create_PolygonButton({"position": ((650, 350), (650, 380), (675, 365)),"position2":((650, 340), (650, 390), (690, 365)),"command1":lambda:self.change_mains({"main":-1,"run":True})})
        self.training_ai_button = self.button_factory_f5.create_TextButton({"text": "Training AI","position": (self.WIDTH/2-70,self.HEIGHT/2-136),"command1":lambda:self.type_mode(True),"command2":lambda:self.check_item(self.mode_game,self.SKYBLUE,self.WHITE,"color",**{"Training AI":self.training_ai_button,"Player":self.player_button,"AI":self.ai_button})})
        self.player_button = self.button_factory_f5.create_TextButton({"text": "One Vs One","position": (self.WIDTH/2-64,self.HEIGHT/2-110),"command1":lambda:self.type_mode(mode_two=True),"command2":lambda:self.check_item(self.mode_game,self.SKYBLUE,self.WHITE,"color",**{"Player":self.player_button,"Training AI":self.training_ai_button,"AI":self.ai_button})})
        self.ai_button = self.button_factory_f5.create_TextButton({"text": "One Vs Ai","position": (self.WIDTH/2-58,self.HEIGHT/2-84),"command1":lambda:self.type_mode(mode_three=True),"command2":lambda:self.check_item(self.mode_game,self.SKYBLUE,self.WHITE,"color",**{"AI":self.ai_button,"Player":self.player_button,"Training AI":self.training_ai_button})})
        self.decrease_score_button = self.button_factory_f5.create_PolygonButton({"color": self.BLACK,"position": ((320, 185), (320, 205), (300, 195)),"color2": self.WHITE,"command1":lambda:setattr(self, 'max_score',  max(1, self.max_score - 1))})
        self.increase_score_button = self.button_factory_f5.create_PolygonButton({"color": self.BLACK,"position": ((380, 185), (380, 205), (400, 195)),"color2": self.WHITE,"command1":lambda:setattr(self, 'max_score', self.max_score + 1)})
        self.config_training_ai()
    def main_training_ai(self):
        self.screen.blit(self.font5.render(f"Config Training\n{"AI":^26}", True, "White"),(self.WIDTH/2+120,self.HEIGHT/2-136))
        self.screen.blit(self.font5.render(f"Generation Size\n{self.config_AI['generation_value']:^26}", True, "White"),(self.WIDTH/2+120,self.HEIGHT/2-81))
        self.screen.blit(self.font5.render(f"Population Size\n{self.config_AI['population_value']:^26}", True, "White"),(self.WIDTH/2+120,self.HEIGHT/2-26))
        self.screen.blit(self.font5.render(f"Attempts By AI\n{self.config_AI['try_for_ai']:^{28 if self.config_AI['try_for_ai']<10 else 26}}", True, "White"),(self.WIDTH/2+120,self.HEIGHT/2+29))
        self.screen.blit(self.font5.render(f"Save model", True, "White"),(self.WIDTH/2+120,self.HEIGHT/2+84))
        self.execute_buttons(self.increase_generation,self.decrease_generation,self.increase_population,self.decrease_population,self.increase_try_for_ai,self.decrease_try_for_ai,self.save_model)
        self.save_model.change_item({"color":self.SKYBLUE if self.config_AI["model_save"] else self.RED,"text":"ON" if self.config_AI["model_save"] else "OFF"})
    def config_training_ai(self):
        self.increase_generation = Button({"screen": self.screen,"font": self.font5,"text": ">","position": (self.WIDTH-100,self.HEIGHT/2-55),"color2": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":lambda:self.increase_decrease_variable(self.config_AI,'generation_value')})
        self.decrease_generation = Button({"screen": self.screen,"font": self.font5,"text": "<","position": (self.WIDTH-178,self.HEIGHT/2-55),"color2": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":lambda:self.increase_decrease_variable(self.config_AI,'generation_value',True,-1)})
        self.increase_population = Button({"screen": self.screen,"font": self.font5,"text": ">","position": (self.WIDTH-100,self.HEIGHT/2),"color2": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":lambda:self.increase_decrease_variable(self.config_AI,'population_value')})
        self.decrease_population = Button({"screen": self.screen,"font": self.font5,"text": "<","position": (self.WIDTH-178,self.HEIGHT/2),"color2": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":lambda:self.increase_decrease_variable(self.config_AI,'population_value',True,-1)})
        self.increase_try_for_ai = Button({"screen": self.screen,"font": self.font5,"text": ">","position": (self.WIDTH-100,self.HEIGHT/2+55),"color2": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":lambda:self.increase_decrease_variable(self.config_AI,'try_for_ai')})
        self.decrease_try_for_ai = Button({"screen": self.screen,"font": self.font5,"text": "<","position": (self.WIDTH-178,self.HEIGHT/2+55),"color2": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":lambda:self.increase_decrease_variable(self.config_AI,'try_for_ai',True,-1)})
        self.save_model = Button({"screen": self.screen,"font": self.font5,"text": "OFF","color": self.SKYBLUE,"position": (self.WIDTH-85,self.HEIGHT/2+84),"color2": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":lambda:self.on_off(self.config_AI,"model_save"),"command2":self.save_config})
    def type_mode(self,mode_one=False,mode_two=False,mode_three=False):
        self.mode_game["Training AI"]=mode_one
        self.mode_game["Player"]=mode_two
        if self.model_training!=None:self.mode_game["AI"]=mode_three
        else:self.load_AI()
    def on_off(self,dic=None,variable=""):
        if dic:dic[variable]=not dic[variable]
        else:setattr(self,variable,not getattr(self,variable))
    def Pause(self):
        if self.main==3:
            self.filt(180)
            self.screen.blit(self.font3.render("Pause",True,"gray"),(self.WIDTH/2-105,self.HEIGHT/2-150))
            self.execute_buttons(self.exit_button,self.reset_pause_button,self.go_main_button)
    def buttons_pausa(self):
        self.exit_button=Button({"screen": self.screen,"font": self.font2_5,"text": "Exit","color": self.GRAY,"position": (self.WIDTH/2-40,self.HEIGHT/2-15),"color2": self.SKYBLUE,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":self.event_quit})
        self.reset_pause_button=Button({"screen": self.screen,"font": self.font2_5,"text": "Reset","color": self.GRAY,"position": (self.WIDTH/2-55,self.HEIGHT/2-85),"color2": self.SKYBLUE,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":lambda:self.change_mains({"main":-1}),"command2":self.reset})
        self.go_main_button=Button({"screen": self.screen,"font": self.font2_5,"text": "Menu","color": self.GRAY,"position": (self.WIDTH/2-45,self.HEIGHT/2-50),"color2": self.SKYBLUE,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":lambda:self.change_mains({"main":0,"run":True}),"command2":self.reset})
    def filt(self,number):
        background=pygame.Surface((self.WIDTH,self.HEIGHT),pygame.SRCALPHA)
        background.fill((0,0,0,number))
        self.screen.blit(background,(0,0))
    def options_menu(self):
        if self.main==4:
            self.screen.fill(self.BLACK)
            self.sound_button.change_item({"color":self.sound_type["color"],"text":self.sound_type["sound"]})
            self.execute_buttons(self.back_button,self.visual_button,self.sound_button,self.keys_button,self.language_button)
    def buttons_menu_options(self):
        self.back_button = Button({"screen": self.screen,"position": ((50, 350), (50, 380), (25, 365)),"position2":((50, 340), (50, 390), (10, 365)),"color2": self.GOLDEN,"type_button": 1,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":lambda:self.change_mains({"main":0})})
        self.visual_button=Button({"screen": self.screen,"font": self.font2_5,"text": "Visuals","position": (self.WIDTH/2-80,self.HEIGHT/2-150),"color2": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":lambda:self.change_mains({"main":5})})
        self.sound_button=Button({"screen": self.screen,"font": self.font2_5,"text": self.sound_type["sound"],"color": self.sound_type["color"],"position": (self.WIDTH/2-80,self.HEIGHT/2-115),"color2": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":lambda:self.on_off(self.config_sounds,"sound_main"),"command2":self.sound_on_off,"command3":self.save_config})
        self.keys_button=Button({"screen": self.screen,"font": self.font2_5,"text": "Keys","position": (self.WIDTH/2-80,self.HEIGHT/2-80),"color2": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":lambda:self.change_mains({"main":6})})
        self.language_button=Button({"screen": self.screen,"font": self.font2_5,"text": "Language","position": (self.WIDTH/2-80,self.HEIGHT/2-45),"color2": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,})
    def sound_on_off(self):
        self.sound_type["value"]=not self.sound_type["value"]
        def sound(color,sound_on_off,sound):
            self.sound_type["color"]=color
            self.sound_type["sound"]=sound_on_off
            sound.play(loops=-1) if color==self.SKYBLUE else sound.stop()
        sound(*(self.SKYBLUE,"Sound ON",self.sound_back) if self.sound_type["value"] else (self.RED,"Sound off",self.sound_back))
    def visuals_menu(self):
        if self.main==5:
            self.screen.blit(self.image, (0, 0))
            self.screen.blit(self.font2_5.render("WIDTH",True,self.SKYBLUE),(self.WIDTH/2-163,self.HEIGHT/2-200))
            self.screen.blit(self.font2_5.render("HEIGHT",True,self.SKYBLUE),(self.WIDTH/2+60,self.HEIGHT/2-200))
            self.screen.blit(self.font2_5.render("IMAGE",True,self.SKYBLUE),(self.WIDTH/2-52,self.HEIGHT/2+160))
            self.images_elements()
            self.execute_buttons(self.back_visual_button,self.decrease_width_button,self.increase_width_button,self.decrease_height_button,self.increase_height_button,self.decrease_planet_button,self.increase_planet_button,self.decrease_back_button,self.increase_back_button,self.decrease_player1_button,self.increase_player1_button,self.decrease_player2_button,self.increase_player2_button,self.save_visual_button,self.default_visual_button)
    def buttons_visual(self):
        self.back_visual_button = Button({"screen": self.screen,"position": ((50, 350), (50, 380), (25, 365)),"position2":((50, 340), (50, 390), (10, 365)),"color2": self.GOLDEN,"type_button": 1,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":lambda:self.change_mains({"main":4})})
        self.decrease_width_button=Button({"screen": self.screen,"font": self.font2_5,"text": "<","position": (self.WIDTH/2-200,self.HEIGHT/2-200),"color2": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":lambda:self.change_items("WIDTH",number=-10)})
        self.increase_width_button=Button({"screen": self.screen,"font": self.font2_5,"text": ">","position": (self.WIDTH/2-40,self.HEIGHT/2-200),"color2": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":lambda:self.change_items("WIDTH",number=10)})
        self.decrease_height_button=Button({"screen": self.screen,"font": self.font2_5,"text": "<","position": (self.WIDTH/2+20,self.HEIGHT/2-200),"color2": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":lambda:self.change_items("HEIGHT",number=-10)})
        self.increase_height_button=Button({"screen": self.screen,"font": self.font2_5,"text": ">","position": (self.WIDTH/2+200,self.HEIGHT/2-200),"color2": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":lambda:self.change_items("HEIGHT",number=10)})
        self.decrease_planet_button=Button({"screen": self.screen,"font": self.font2_5,"text": "<","position": (self.WIDTH/2-40,self.HEIGHT/2-22),"color2": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":lambda:self.change_items("value_planet","planets",-1)})
        self.increase_planet_button=Button({"screen": self.screen,"font": self.font2_5,"text": ">","position": (self.WIDTH/2+20,self.HEIGHT/2-22),"color2": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":lambda:self.change_items("value_planet","planets",1)})
        self.decrease_back_button=Button({"screen": self.screen,"font": self.font2_5,"text": "<","position": (self.WIDTH/2-80,self.HEIGHT/2+160),"color2": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":lambda:self.change_items("value_background","image_background",-1)})
        self.increase_back_button=Button({"screen": self.screen,"font": self.font2_5,"text": ">","position": (self.WIDTH/2+65,self.HEIGHT/2+160),"color2": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":lambda:self.change_items("value_background","image_background",1)})
        self.decrease_player1_button=Button({"screen": self.screen,"font": (font:=pygame.font.SysFont("times new roman", 30)),"text": "Λ","position": (self.WIDTH/2-330,self.HEIGHT/2-120),"color2": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":lambda:self.change_items("value_spacecraft1","spacecrafts",-1)})
        self.increase_player1_button=Button({"screen": self.screen,"font": (font2:=pygame.font.SysFont("times new roman", 38)),"text": "v","position": (self.WIDTH/2-330,self.HEIGHT/2+50),"color2": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":lambda:self.change_items("value_spacecraft1","spacecrafts",1)})
        self.decrease_player2_button=Button({"screen": self.screen,"font": font,"text": "Λ","position": (self.WIDTH/2+310,self.HEIGHT/2-120),"color2": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":lambda:self.change_items("value_spacecraft2","spacecrafts",-1)})
        self.increase_player2_button=Button({"screen": self.screen,"font": font2,"text": "v","position": (self.WIDTH/2+310,self.HEIGHT/2+50),"color2": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":lambda:self.change_items("value_spacecraft2","spacecrafts",1)})
        self.save_visual_button=Button({"screen": self.screen,"font": self.font5,"text": "Save Config","position": (self.WIDTH/2+200,self.HEIGHT/2+140),"color2": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":self.save_config})
        self.default_visual_button=Button({"screen": self.screen,"font": self.font5,"text": "Default config","position": (self.WIDTH/2+160,self.HEIGHT/2+160),"color2": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":lambda:self.config(visuals=True),"command2":self.config_screen})
    def change_items(self,item,background=None,number=0):
        self.config_visuals[item]=((self.config_visuals[item] + number) % len(self.config_visuals[background])) if background!=None else (self.config_visuals[item] + number)
        self.config_screen()
    def menu_keys(self):
        if self.main==6:
            self.screen.fill(self.BLACK)
            self.execute_buttons(self.back_keys_button,self.up_w_button,self.down_s_button,self.up_arrow_button,self.down_arrow_button,self.save_keys_button,self.default_keys_button)
    def buttons_keys(self):
        self.back_keys_button = Button({"screen": self.screen,"position": ((50, 350), (50, 380), (25, 365)),"position2":((50, 340), (50, 390), (10, 365)),"color2": self.GOLDEN,"type_button": 1,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":lambda:self.change_mains({"main":4})})
        self.up_w_button=Button({"screen": self.screen,"font": (font:=pygame.font.SysFont("times new roman", 80)),"text": self.config_keys["Name_key1"],"position": (self.WIDTH/2-240,self.HEIGHT/2-170),"color2": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":lambda:self.change_keys("UP_W","Name_key1",self.up_w_button)})
        self.down_s_button=Button({"screen": self.screen,"font": font,"text": self.config_keys["Name_key2"],"position": (self.WIDTH/2-217,self.HEIGHT/2-20),"color2": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":lambda:self.change_keys("DOWN_S","Name_key2",self.down_s_button)})
        self.up_arrow_button=Button({"screen": self.screen,"font": font,"text": self.config_keys["Name_key3"],"position": (self.WIDTH/2+200,self.HEIGHT/2-170),"color2": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":lambda:self.change_keys("UP_ARROW","Name_key3",self.up_arrow_button)})
        self.down_arrow_button=Button({"screen": self.screen,"font": font,"text": self.config_keys["Name_key4"],"position": (self.WIDTH/2+200,self.HEIGHT/2-20),"color2": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":lambda:self.change_keys("DOWN_ARROW","Name_key4",self.down_arrow_button)})
        self.save_keys_button=Button({"screen": self.screen,"font": self.font5,"text": "Save Config","position": (self.WIDTH/2+200,self.HEIGHT/2+140),"color2": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":self.save_config})
        self.default_keys_button=Button({"screen": self.screen,"font": self.font5,"text": "Default config","position": (self.WIDTH/2+160,self.HEIGHT/2+160),"color2": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":lambda:(self.config(keys=True),self.change_mains({"main":6,"command":self.buttons_keys}))})
    def change_keys(self,key,key_name,button=None):
        self.key=key
        self.key_name=key_name
        self.button_key=button
        for k in self.utils_keys.keys():self.utils_keys[k]=False if k!=self.key else not self.utils_keys[self.key]
        self.check_item(self.utils_keys,self.SKYBLUE,self.WHITE,"color",**{"UP_W":self.up_w_button,"DOWN_S":self.down_s_button,"UP_ARROW":self.up_arrow_button,"DOWN_ARROW":self.down_arrow_button})
    def event_keys(self,event):
        if self.key!=None and (self.utils_keys[self.key] and event.type==KEYDOWN):
            self.config_keys[self.key]=event.key
            self.config_keys[self.key_name]=event.unicode.upper()
            self.check_item(self.config_keys,self.config_keys[self.key_name],self.WHITE,"text",**{self.key:self.button_key})
            self.change_keys(self.key,self.key_name)
    def check_item(self,dic,is_true,is_false,item,**kwargs):
        for key,button in kwargs.items():setattr(button,item,(is_true if dic[key] else is_false))
    def fade_transition(self,fade_in,color=(0,0,0),limit=255):
        overlay = pygame.Surface((self.WIDTH, self.HEIGHT))
        overlay.fill(color)
        alpha=0 if not fade_in else 255
        while (not fade_in and alpha <= limit) or (fade_in and alpha >= limit):
            overlay.set_alpha(alpha)
            self.screen.blit(overlay, (0, 0))
            pygame.display.flip()
            self.clock.tick(20)
            alpha += -15 if fade_in else 15
    def change_mains(self,config):
        if fade_in:=config.get("fade_in",True):self.fade_transition(False,config.get("color",(0,0,0)),255)
        if fade_out:=config.get("fade_out",False):self.fade_transition(True,config.get("color2",(0,0,0)),0)
        self.main=config.get("main",None)
        if config.get("command",None):config["command"]()
        if config.get("run",False):setattr(self,"running",False),setattr(self, "game_over", True)
        if config.get("recursive",False):self.change_mains({"main":self.main,"fade_in":fade_in,"fade_out":fade_out})
    def increase_decrease_variable(self,dic=None,variable="",length=None,number=1,save=True):
        if dic!=None and length!=None:dic[variable]=max(1, dic[variable] + number)
        elif dic!=None:dic[variable]+=number
        else:setattr(self,variable,getattr(self,variable)+number)
        if save:self.save_config()