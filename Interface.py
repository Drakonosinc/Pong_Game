import pygame,os
from pygame.locals import *
from Genetic_Algorithm import *
class interface():
    def menus(self):
        self.Pause()
        self.main_menu()
        self.game_mode()
        self.options_menu()
        self.visuals_menu()
        self.menu_keys()
        self.Game_over()
    def main_menu(self):
        if self.main==0:
            self.screen.fill(self.BLACK)
            self.screen.blit(self.font4.render("Space Pong", True, self.WHITE),(self.WIDTH//2-245,self.HEIGHT//2-180))
            self.button(self.screen,2,self.font5,"Press To Start",self.WHITE,(self.WIDTH//2-200,self.HEIGHT//2-80),0,self.GOLDEN)
            press_quit=self.button(self.screen,None,self.font5,"Press To Exit",self.WHITE,(self.WIDTH//2-200,self.HEIGHT//2-50),1,self.GOLDEN,False)
            self.button(self.screen,4,self.font5,"Options",self.WHITE,(self.WIDTH-110,self.HEIGHT-40),11,self.GOLDEN)
            if self.pressed_mouse[0] and press_quit.collidepoint(self.mouse_pos):self.event_quit()
    def Game_over(self):
        if self.main==1:
            self.filt(80)
            pygame.draw.rect(self.screen,"black",(0,0,700,400),15)
            self.screen.blit(self.font3.render("GAME OVER",True,"black"),(self.WIDTH/2-178,self.HEIGHT/2-180))
            self.screen.blit(self.font2_5.render("Main Menu Press E",True,"black"),(self.WIDTH/2-166,self.HEIGHT/2-110))
            self.screen.blit(self.font2_5.render("Reset Press R",True,"black"),(self.WIDTH/2-130,self.HEIGHT/2-80))
    def game_mode(self):
        if self.main==2:
            self.screen.fill(self.BLACK)
            self.screen.blit(self.font5.render("Enter Player Name One",True,"white"),(7,10))
            self.screen.blit(self.font5.render("Enter Player Name Two",True,"white"),(416,10))
            pygame.draw.rect(self.screen,self.color_inputtext1,(8,40,271,25))
            pygame.draw.rect(self.screen,self.color_inputtext2,(418,40,275,25))
            self.input_player1=pygame.draw.rect(self.screen,self.GRAY,(8,40,271,25),2)
            self.input_player2=pygame.draw.rect(self.screen,self.GRAY,(418,40,275,25),2)
            self.screen.blit(self.font5.render(self.text_player1, True, self.BLACK), (self.input_player1.x+5, self.input_player1.y-2))
            self.screen.blit(self.font5.render(self.text_player2, True, self.BLACK), (self.input_player2.x+5, self.input_player2.y-2))
            self.button_arrow(0,((50, 350), (50, 380), (25, 365)),((50, 340), (50, 390), (10, 365)),self.WHITE,2,13)
            self.button_arrow(-1,((650, 350), (650, 380), (675, 365)),((650, 340), (650, 390), (690, 365)),self.WHITE,16,15)
            self.screen.blit((font_modegame:=pygame.font.Font(os.path.join(self.font_path,"8bitOperatorPlusSC-Bold.ttf"),22)).render("Game Mode",True,"white"),(self.WIDTH/2-70,self.HEIGHT/2-162))
            self.button(self.screen,None,self.font5,"Training AI",(self.SKYBLUE if self.mode_game[0] else self.WHITE),(self.WIDTH/2-70,self.HEIGHT/2-136),None,None,True,lambda:(self.mode_game.__setitem__(0, True), self.mode_game.__setitem__(1, False), self.mode_game.__setitem__(2, False)),False,4)
            self.button(self.screen,None,self.font5,"One Vs One",(self.SKYBLUE if self.mode_game[1] else self.WHITE),(self.WIDTH/2-64,self.HEIGHT/2-110),None,None,True,lambda:(self.mode_game.__setitem__(0, False), self.mode_game.__setitem__(1, True), self.mode_game.__setitem__(2, False)),False,5)
            if self.model_training!=None:self.button(self.screen,None,self.font5,"One Vs Ai",(self.SKYBLUE if self.mode_game[2] else self.WHITE),(self.WIDTH/2-58,self.HEIGHT/2-84),None,None,True,lambda:(self.mode_game.__setitem__(0, False), self.mode_game.__setitem__(1, False), self.mode_game.__setitem__(2, True)),False,6)
            else:
                if os.path.exists(self.model_path):self.model_training = load_model(self.model_path, 6, 2)
            self.screen.blit(font_modegame.render("Max Score",True,"white"),(self.WIDTH/2-68,self.HEIGHT/2-50))
            self.screen.blit(font_modegame.render(f"{self.max_score}",True,"white"),(self.WIDTH/2-8,self.HEIGHT/2-20))
            self.button_arrow(None,((320, 185), (320, 205), (300, 195)),((320, 185), (320, 205), (300, 195)),self.BLACK,7,10,(x:=True if self.max_score>1 else False),x,command=lambda: setattr(self, 'max_score', self.max_score - 1))
            self.button_arrow(None,((380, 185), (380, 205), (400, 195)),((380, 185), (380, 205), (400, 195)),self.BLACK,8,9,command=lambda: setattr(self, 'max_score', self.max_score + 1))
            if self.pressed_mouse[0]:
                self.color_inputtext1=self.SKYBLUE if self.input_player1.collidepoint(self.mouse_pos) else self.WHITE
                self.color_inputtext2=self.SKYBLUE if self.input_player2.collidepoint(self.mouse_pos) else self.WHITE
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
        self.button(self.screen,None,self.font5,"default config",self.SKYBLUE,(self.WIDTH/2+160,self.HEIGHT/2+160),30,self.GOLDEN,command=self.prefinished_config_visuals,number2=29,command2=self.load_images)
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
        self.button(self.screen,None,self.font5,"default config",self.SKYBLUE,(self.WIDTH/2+160,self.HEIGHT/2+160),30,self.GOLDEN,command=self.prefinished_config_keys,number2=29)
    def change_keys(self,key,key_name):
        self.key=key
        self.key_name=key_name
        self.utils_keys[self.key]= not self.utils_keys[self.key]
    def event_keys(self,event):
        if self.key!=None:
            if self.utils_keys[self.key] and event.type==KEYDOWN:
                self.config_keys[self.key]=event.key
                self.config_keys[self.key_name]=event.unicode.upper()
                self.utils_keys[self.key]= not self.utils_keys[self.key]
    def button(self,screen,main:int,font,text:str,color,position,number:int,color2=None,pressed=True,command=None,detect_mouse=True,number2=None,command2=None):
        button=screen.blit(font.render(text,True,color),position)
        if detect_mouse:
            if button.collidepoint(self.mouse_pos):
                screen.blit(font.render(text,True,color2),position)
                if self.notsound_playing[number]:
                    self.sound_buttonletters.play(loops=0)
                    self.notsound_playing[number]=False
            else:self.notsound_playing[number]=True
        if self.pressed_mouse[0] and pressed:
            if button.collidepoint(self.mouse_pos) and number2==None:
                self.sound_touchletters.play(loops=0)
                if main!=None:self.main=main
                if command!=None:command()
                if command2!=None:command2()
            if number2!=None:
                if button.collidepoint(self.mouse_pos):
                    if self.notsound_playing[number2]:
                        self.sound_touchletters.play(loops=0)
                        self.notsound_playing[number2]=False
                        if command!=None:command()
                        if command2!=None:command2()
                else:self.notsound_playing[number2]=True
        if pressed==False:return button
    def button_arrow(self,main,position,position2,color,number:int,number2=None,pressed=True,detect_mouse=True,command=None):
        arrow_button=pygame.draw.polygon(self.screen, color, position)
        if detect_mouse:
            if arrow_button.collidepoint(self.mouse_pos):
                pygame.draw.polygon(self.screen, self.WHITE, position2)
                if self.notsound_playing[number]:
                    self.sound_buttonletters.play(loops=0)
                    self.notsound_playing[number]=False
            else:self.notsound_playing[number]=True
        if self.pressed_mouse[0] and pressed:
            if arrow_button.collidepoint(self.mouse_pos):
                if self.notsound_playing[number2]:
                    self.sound_touchletters.play(loops=0)
                    self.notsound_playing[number2]=False
                    if main!=None:self.main=main
                    if command!=None:command()
            else:self.notsound_playing[number2]=True
        if pressed==False:return arrow_button