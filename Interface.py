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
        self.buttons_main_menu()
        self.buttons_game_over()
        self.buttons_mode_game()
        # self.buttons_pausa()
        # self.buttons_menu_options()
        # self.buttons_visual()
    def execute_buttons(self,*args):
        for button in args:button.draw()
    def main_menu(self):
        if self.main==0:
            self.screen.fill(self.BLACK)
            self.screen.blit(self.font4.render("Space Pong", True, self.WHITE),(self.WIDTH//2-245,self.HEIGHT//2-180))
            self.execute_buttons(self.play_button,self.quit_button,self.options_button)
    def buttons_main_menu(self):
        self.play_button = Button({"screen": self.screen,"font": self.font5,"text": "Press To Start","color": self.WHITE,"position": (self.WIDTH//2-200,self.HEIGHT//2-80),"color2": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":lambda:setattr(self,'main',2)})
        self.quit_button = Button({"screen": self.screen,"font": self.font5,"text": "Press To Exit","color": self.WHITE,"position": (self.WIDTH//2-200,self.HEIGHT//2-50),"color2": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_exitbutton,"command1": self.event_quit})
        self.options_button = Button({"screen": self.screen,"font": self.font5,"text": "Options","color": self.WHITE,"position": (self.WIDTH-110,self.HEIGHT-40),"color2": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":lambda:setattr(self,'main',4)})
    def Game_over(self):
        if self.main==1:
            self.filt(80)
            pygame.draw.rect(self.screen,"black",(0,0,700,400),15)
            self.screen.blit(self.font3.render("GAME OVER",True,"black"),(self.WIDTH/2-178,self.HEIGHT/2-180))
            self.execute_buttons(self.main_button,self.reset_button)
    def buttons_game_over(self):
        self.main_button=Button({"screen": self.screen,"font": self.font2_5,"text": "Main Menu Press E","color": self.BLACK,"position": (self.WIDTH/2-166,self.HEIGHT/2-110),"color2": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":lambda:setattr(self,'main',0)})
        self.reset_button=Button({"screen": self.screen,"font": self.font2_5,"text": "Reset Press R","color": self.BLACK,"position": (self.WIDTH/2-130,self.HEIGHT/2-80),"color2": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1": self.reset,"command2":lambda:setattr(self,'main',2)})
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
            if self.pressed_mouse[0]:
                self.color_inputtext1=self.SKYBLUE if self.input_player1.collidepoint(self.mouse_pos) else self.WHITE
                self.color_inputtext2=self.SKYBLUE if self.input_player2.collidepoint(self.mouse_pos) else self.WHITE
            self.execute_buttons(self.back_button,self.continue_button,self.training_ai_button,self.player_button,self.ai_button,self.decrease_button,self.increase_button)
    def buttons_mode_game(self):
        self.back_button = Button({"screen": self.screen,"color": self.WHITE,"position": ((50, 350), (50, 380), (25, 365)),"position2":((50, 340), (50, 390), (10, 365)),"color2": self.GOLDEN,"type_button": 1,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":lambda:setattr(self,'main',0)})
        self.continue_button = Button({"screen": self.screen,"color": self.WHITE,"position": ((650, 350), (650, 380), (675, 365)),"position2":((650, 340), (650, 390), (690, 365)),"color2": self.GOLDEN,"type_button": 1,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":lambda:setattr(self,'main',-1)})
        self.training_ai_button = Button({"screen": self.screen,"font": self.font5,"text": "Training AI","color": self.WHITE,"position": (self.WIDTH/2-70,self.HEIGHT/2-136),"color2": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":lambda:self.type_mode(True),"command2":lambda:self.check_colors(self.mode_game,self.SKYBLUE,self.WHITE,**{"Training AI":self.training_ai_button,"Player":self.player_button,"AI":self.ai_button})})
        self.player_button = Button({"screen": self.screen,"font": self.font5,"text": "One Vs One","color": self.WHITE,"position": (self.WIDTH/2-64,self.HEIGHT/2-110),"color2": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":lambda:self.type_mode(mode_two=True),"command2":lambda:self.check_colors(self.mode_game,self.SKYBLUE,self.WHITE,**{"Player":self.player_button,"Training AI":self.training_ai_button,"AI":self.ai_button})})
        self.ai_button = Button({"screen": self.screen,"font": self.font5,"text": "One Vs Ai","color": self.WHITE,"position": (self.WIDTH/2-58,self.HEIGHT/2-84),"color2": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":lambda:self.type_mode(mode_three=True),"command2":lambda:self.check_colors(self.mode_game,self.SKYBLUE,self.WHITE,**{"AI":self.ai_button,"Player":self.player_button,"Training AI":self.training_ai_button})})
        self.decrease_button = Button({"screen": self.screen,"color": self.BLACK,"position": ((320, 185), (320, 205), (300, 195)),"color2": self.GOLDEN,"type_button": 1,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":lambda:setattr(self, 'max_score', self.max_score - 1),"command2":lambda:self.decrease_button.change_item({"pressed":(x:=False if self.max_score<=1 else True),"detect_mouse":x})})
        self.increase_button = Button({"screen": self.screen,"color": self.BLACK,"position": ((380, 185), (380, 205), (400, 195)),"color2": self.GOLDEN,"type_button": 1,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":lambda:setattr(self, 'max_score', self.max_score + 1),"command2":lambda:self.decrease_button.change_item({"pressed":True,"detect_mouse":True})})
    def type_mode(self,mode_one=False,mode_two=False,mode_three=False):
        self.mode_game["Training AI"]=mode_one
        self.mode_game["Player"]=mode_two
        if self.model_training!=None:self.mode_game["AI"]=mode_three
        else:self.load_AI()
    def Pause(self):
        if self.main==3:
            self.filt(180)
            self.screen.blit(self.font3.render("Pause",True,"gray"),(self.WIDTH/2-105,self.HEIGHT/2-150))
            close=self.button(self.screen,None,self.font2_5,"Exit",self.GRAY,(self.WIDTH/2-40,self.HEIGHT/2-15),3,self.SKYBLUE,False)
            self.button(self.screen,-1,self.font2_5,"Reset",self.GRAY,(self.WIDTH/2-55,self.HEIGHT/2-85),0,self.SKYBLUE,command=self.reset)
            self.button(self.screen,0,self.font2_5,"Menu",self.GRAY,(self.WIDTH/2-45,self.HEIGHT/2-50),1,self.SKYBLUE,command=self.reset)
            if self.pressed_mouse[0] and close.collidepoint(self.mouse_pos):self.event_quit()
    def filt(self,number):
        background=pygame.Surface((self.WIDTH,self.HEIGHT),pygame.SRCALPHA)
        background.fill((0,0,0,number))
        self.screen.blit(background,(0,0))
    def options_menu(self):
        if self.main==4:
            self.screen.fill(self.BLACK)
            self.anim_options()
            self.button_arrow(0,((50, 350), (50, 380), (25, 365)),((50, 340), (50, 390), (10, 365)),self.WHITE,2,13)
    def anim_options(self):
        self.button(self.screen,5,self.font2_5,"Visuals",self.WHITE,(self.WIDTH/2-80,self.HEIGHT/2-150),0,self.GOLDEN,True)
        self.button(self.screen,None,self.font2_5,self.sound_type["sound"],self.sound_type["color"],(self.WIDTH/2-80,self.HEIGHT/2-115),1,self.GOLDEN,command=self.sound_on_off,number2=14)
        self.button(self.screen,6,self.font2_5,"Keys",self.WHITE,(self.WIDTH/2-80,self.HEIGHT/2-80),3,self.GOLDEN,True)
        self.button(self.screen,None,self.font2_5,"Language",self.WHITE,(self.WIDTH/2-80,self.HEIGHT/2-45),4,self.GOLDEN,True,number2=9)
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
            self.images_elements()
            self.anim_visuals()
            self.button_arrow(4,((50, 350), (50, 380), (25, 365)),((50, 340), (50, 390), (10, 365)),self.WHITE,2,13)
    def anim_visuals(self):
        self.screen.blit(self.font2_5.render("WIDTH",True,self.SKYBLUE),(self.WIDTH/2-163,self.HEIGHT/2-200))
        self.screen.blit(self.font2_5.render("HEIGHT",True,self.SKYBLUE),(self.WIDTH/2+60,self.HEIGHT/2-200))
        self.screen.blit(self.font2_5.render("IMAGE",True,self.SKYBLUE),(self.WIDTH/2-52,self.HEIGHT/2+160))
        self.button(self.screen,None,self.font2_5,"<",self.GOLDEN,(self.WIDTH/2-200,self.HEIGHT/2-200),1,self.SKYBLUE,command=lambda: self.config_visuals.update({"WIDTH": (self.config_visuals["WIDTH"] - 10)}),number2=9,command2=self.config_screen)
        self.button(self.screen,None,self.font2_5,">",self.GOLDEN,(self.WIDTH/2-40,self.HEIGHT/2-200),3,self.SKYBLUE,command=lambda: self.config_visuals.update({"WIDTH": (self.config_visuals["WIDTH"] + 10)}),number2=10,command2=self.config_screen)
        self.button(self.screen,None,self.font2_5,"<",self.GOLDEN,(self.WIDTH/2+20,self.HEIGHT/2-200),4,self.SKYBLUE,command=lambda: self.config_visuals.update({"HEIGHT": (self.config_visuals["HEIGHT"] - 10)}),number2=14,command2=self.config_screen)
        self.button(self.screen,None,self.font2_5,">",self.GOLDEN,(self.WIDTH/2+200,self.HEIGHT/2-200),0,self.SKYBLUE,command=lambda: self.config_visuals.update({"HEIGHT": (self.config_visuals["HEIGHT"] + 10)}),number2=17,command2=self.config_screen)
        self.button(self.screen,None,self.font2_5,"<",self.GOLDEN,(self.WIDTH/2-40,self.HEIGHT/2-22),5,self.SKYBLUE,command=lambda: self.config_visuals.update({"value_planet": (self.config_visuals["value_planet"] - 1) % len(self.config_visuals["planets"])}),number2=18,command2=self.load_images)
        self.button(self.screen,None,self.font2_5,">",self.GOLDEN,(self.WIDTH/2+20,self.HEIGHT/2-22),6,self.SKYBLUE,command=lambda: self.config_visuals.update({"value_planet": (self.config_visuals["value_planet"] + 1) % len(self.config_visuals["planets"])}),number2=19,command2=self.load_images)
        self.button(self.screen,None,self.font2_5,"<",self.GOLDEN,(self.WIDTH/2-80,self.HEIGHT/2+160),7,self.SKYBLUE,command=lambda: self.config_visuals.update({"value_background": (self.config_visuals["value_background"] - 1) % len(self.config_visuals["image_background"])}),number2=20,command2=self.load_images)
        self.button(self.screen,None,self.font2_5,">",self.GOLDEN,(self.WIDTH/2+65,self.HEIGHT/2+160),8,self.SKYBLUE,command=lambda: self.config_visuals.update({"value_background": (self.config_visuals["value_background"] + 1) % len(self.config_visuals["image_background"])}),number2=21,command2=self.load_images)
        self.button(self.screen,None,font:=pygame.font.SysFont("times new roman", 30),"Λ",self.WHITE,(self.WIDTH/2-330,self.HEIGHT/2-120),11,self.SKYBLUE,command=lambda: self.config_visuals.update({"value_spacecraft1": (self.config_visuals["value_spacecraft1"] + 1) % len(self.config_visuals["spacecrafts"])}),number2=22,command2=self.load_images)
        self.button(self.screen,None,font2:=pygame.font.SysFont("times new roman", 38),"v",self.WHITE,(self.WIDTH/2-330,self.HEIGHT/2+50),12,self.SKYBLUE,command=lambda: self.config_visuals.update({"value_spacecraft1": (self.config_visuals["value_spacecraft1"] - 1) % len(self.config_visuals["spacecrafts"])}),number2=23,command2=self.load_images)
        self.button(self.screen,None,font,"Λ",self.WHITE,(self.WIDTH/2+310,self.HEIGHT/2-120),15,self.SKYBLUE,number2=24,command=lambda: self.config_visuals.update({"value_spacecraft2": (self.config_visuals["value_spacecraft2"] + 1) % len(self.config_visuals["spacecrafts"])}),command2=self.load_images)
        self.button(self.screen,None,font2,"v",self.WHITE,(self.WIDTH/2+310,self.HEIGHT/2+50),26,self.SKYBLUE,number2=25,command=lambda: self.config_visuals.update({"value_spacecraft2": (self.config_visuals["value_spacecraft2"] - 1) % len(self.config_visuals["spacecrafts"])}),command2=self.load_images)
        self.button(self.screen,None,self.font5,"Save Config",self.SKYBLUE,(self.WIDTH/2+200,self.HEIGHT/2+140),28,self.GOLDEN,command=self.save_config,number2=27)
        self.button(self.screen,None,self.font5,"default config",self.SKYBLUE,(self.WIDTH/2+160,self.HEIGHT/2+160),30,self.GOLDEN,command=lambda:self.config(visuals=True),number2=29,command2=self.load_images)
    def menu_keys(self):
        if self.main==6:
            self.screen.fill(self.BLACK)
            self.anim_keys()
            self.button_arrow(4,((50, 350), (50, 380), (25, 365)),((50, 340), (50, 390), (10, 365)),self.WHITE,2,13)
    def anim_keys(self):
        self.button(self.screen,None,font:=pygame.font.SysFont("times new roman", 80),self.config_keys["Name_key1"],self.SKYBLUE if self.utils_keys["UP_W"] else self.WHITE,(self.WIDTH/2-240,self.HEIGHT/2-170),0,self.GOLDEN,command=lambda:self.change_keys("UP_W","Name_key1"),number2=9)
        self.button(self.screen,None,font,self.config_keys["Name_key2"],self.SKYBLUE if self.utils_keys["DOWN_S"] else self.WHITE,(self.WIDTH/2-217,self.HEIGHT/2-20),3,self.GOLDEN,command=lambda:self.change_keys("DOWN_S","Name_key2"),number2=10)
        self.button(self.screen,None,font,self.config_keys["Name_key3"] if self.config_keys["Name_key3"]!="" else "↑",self.SKYBLUE if self.utils_keys["UP_ARROW"] else self.WHITE,(self.WIDTH/2+200,self.HEIGHT/2-170),4,self.GOLDEN,command=lambda:self.change_keys("UP_ARROW","Name_key3"),number2=14)
        self.button(self.screen,None,font,self.config_keys["Name_key4"] if self.config_keys["Name_key4"]!="" else "↓",self.SKYBLUE if self.utils_keys["DOWN_ARROW"] else self.WHITE,(self.WIDTH/2+200,self.HEIGHT/2-20),5,self.GOLDEN,command=lambda:self.change_keys("DOWN_ARROW","Name_key4"),number2=17)
        self.button(self.screen,None,self.font5,"Save Config",self.SKYBLUE,(self.WIDTH/2+200,self.HEIGHT/2+140),28,self.GOLDEN,command=self.save_config,number2=27)
        self.button(self.screen,None,self.font5,"default config",self.SKYBLUE,(self.WIDTH/2+160,self.HEIGHT/2+160),30,self.GOLDEN,command=lambda:self.config(keys=True),number2=29)
    def change_keys(self,key,key_name):
        self.key=key
        self.key_name=key_name
        for k in self.utils_keys.keys():self.utils_keys[k]=False if k!=self.key else not self.utils_keys[self.key]
    def event_keys(self,event):
        if self.key!=None and (self.utils_keys[self.key] and event.type==KEYDOWN):
            self.config_keys[self.key]=event.key
            self.config_keys[self.key_name]=event.unicode.upper()
            self.utils_keys[self.key]= not self.utils_keys[self.key]
    def check_colors(self,dic,color1,color2,**kwargs):
        for key,button in kwargs.items():setattr(button,"color",(color1 if dic[key] else color2))