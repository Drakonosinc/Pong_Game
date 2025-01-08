import pygame,os,json
from pygame.locals import *
from Genetic_Algorithm import *
import numpy as np

class Space_pong_game():
    def __init__(self,model=None):
        self.load_config()
        pygame.init()
        pygame.display.set_caption("Space Pong")
        self.load_model(model)
        self.define_colors()
        self.load_fonts()
        self.load_sounds()
        self.load_varials()
        self.config_screen()
        self.load_images()
        self.objects()
        self.new_events()
    def load_config(self):
        try:
            config_path = os.path.join(os.path.dirname(__file__), "Config")
            with open(os.path.join(config_path,"config.txt"), 'r') as file:
                config = json.load(file)
            self.config_visuals = config["config_visuals"]
            self.config_keys = config["config_keys"]
        except:self.config()
    def config(self):
        self.config_visuals={"WIDTH":700,"HEIGHT":400,
                            "image_background":["background1.jpg","background2.jpg","background3.jpg","background4.jpg","background5.jpg","background6.jpg","background7.jpg","background8.jpg"],
                            "value_background":0,
                            "planets":["Mars.png","Mars1.png","meteorite.png","Saturn.png","earth.png"],
                            "value_planet":0,
                            "spacecrafts":["spaceship.png","spaceship2.png","spaceship3.png"],
                            "value_spacecraft1":0,
                            "value_spacecraft2":0}
        self.config_keys={"UP_W":K_w,"Name_key1":"W",
                        "DOWN_S":K_s,"Name_key2":"S",
                        "UP_ARROW":K_UP,"Name_key3":"↑",
                        "DOWN_ARROW":K_DOWN,"Name_key4":"↓"}
    def save_config(self):
        config_path = os.path.join(os.path.dirname(__file__), "Config")
        config = {"config_visuals": self.config_visuals,
                    "config_keys": self.config_keys}
        with open(os.path.join(config_path,"config.txt"), 'w') as file:
            json.dump(config, file, indent=4)
    def prefinished_config_visuals(self):
        self.config_visuals["WIDTH"]=700
        self.config_visuals["HEIGHT"]=400
        self.config_visuals["value_background"]=0
        self.config_visuals["value_planet"]=0
        self.config_visuals["value_spacecraft"]=0
    def prefinished_config_keys(self):
        self.config_keys["UP_W"]=K_w
        self.config_keys["Name_key1"]="W"
        self.config_keys["DOWN_S"]=K_s
        self.config_keys["Name_key2"]="S"
        self.config_keys["UP_ARROW"]=K_UP
        self.config_keys["Name_key3"]="↑"
        self.config_keys["DOWN_ARROW"]=K_DOWN
        self.config_keys["Name_key4"]="↓"
    def load_model(self,model):
        self.model=model
        self.model_path=os.path.join(os.path.dirname(__file__), "IA/best_model.pth")
        if os.path.exists(self.model_path):self.model_training = load_model(self.model_path, 6, 2)
        else:self.model_training = None
    def load_varials(self):
        self.running=False
        self.game_over=False
        self.clock=pygame.time.Clock()
        self.FPS=60
        self.generation=0
        self.value1=4
        self.value2=4
        self.score1=0
        self.score2=0
        self.reward=0
        self.main=0 # -1=game, 0=menu, 1=game over, 2=game mode, 3=pausa, 4=options, 5=visuals, 6=menu keys
        self.color_inputtext1=self.WHITE
        self.color_inputtext2=self.WHITE
        self.text_player1="player 1"
        self.text_player2="PC"
        self.speed=0
        self.speed_up=True
        self.speed_down=True
        self.notsound_playing=[True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,
                            True,True,True,True,True,True,True,True,True,True,True,True,True,True,True]
        self.mode_game=[True,False,False]
        self.max_score=5
        self.touch_ball=[True,True]
        self.sound_type={"sound":"Sound ON","color":self.SKYBLUE,"value":True}
        self.utils_keys={"UP_W":False,"DOWN_S":False,"UP_ARROW":False,"DOWN_ARROW":False}
        self.key=None
    def config_screen(self):
        self.WIDTH=self.config_visuals["WIDTH"]
        self.HEIGHT=self.config_visuals["HEIGHT"]
        self.screen=pygame.display.set_mode((self.WIDTH,self.HEIGHT))
        self.load_images()
    def define_colors(self):
        self.GRAY=(127,127,127)
        self.WHITE=(255,255,255)
        self.BLACK=(0,0,0)
        self.GREEN=(0,255,0)
        self.BLUE=(0,0,255)
        self.SKYBLUE=(135,206,235)
        self.YELLOW=(255,255,0)
        self.RED=(255,0,0)
        self.GOLDEN=(255,199,51)
        self.background=self.GRAY
    def load_images(self):
        self.angle=90
        self.image_path = os.path.join(os.path.dirname(__file__), "images")
        self.image=pygame.image.load(os.path.join(self.image_path,self.config_visuals["image_background"][self.config_visuals["value_background"]])).convert()
        self.image=pygame.transform.scale(self.image,(self.WIDTH,self.HEIGHT))
        self.planet=pygame.image.load(os.path.join(self.image_path,self.config_visuals["planets"][self.config_visuals["value_planet"]])).convert_alpha()
        self.planet=pygame.transform.scale(self.planet,(40,40))
        self.spacecraft=pygame.image.load(os.path.join(self.image_path,self.config_visuals["spacecrafts"][self.config_visuals["value_spacecraft1"]])).convert_alpha()
        self.spacecraft=pygame.transform.scale(self.spacecraft,(350,200))
        self.spacecraft=pygame.transform.rotate(self.spacecraft,self.angle)
        self.spacecraft2=pygame.image.load(os.path.join(self.image_path,self.config_visuals["spacecrafts"][self.config_visuals["value_spacecraft2"]])).convert_alpha()
        self.spacecraft2=pygame.transform.scale(self.spacecraft2,(350,200))
        self.spacecraft2=pygame.transform.rotate(self.spacecraft2,self.angle*3)
    def load_fonts(self):
        self.font_path = os.path.join(os.path.dirname(__file__), "fonts")
        self.font=pygame.font.Font(None,25)
        self.font2=pygame.font.Font(None,35)
        self.font2_5=pygame.font.Font(os.path.join(self.font_path,"8bitOperatorPlusSC-Bold.ttf"),30)
        self.font3=pygame.font.Font(os.path.join(self.font_path,"8bitOperatorPlusSC-Bold.ttf"),60)
        self.font4=pygame.font.Font(os.path.join(self.font_path,"8bitOperatorPlusSC-Bold.ttf"),75)
        self.font5=pygame.font.Font(os.path.join(self.font_path,"8bitOperatorPlusSC-Bold.ttf"),20)
    def load_sounds(self):
        self.sound_path = os.path.join(os.path.dirname(__file__), "sounds")
        self.sound=pygame.mixer.Sound(os.path.join(self.sound_path,"pong.wav"))
        self.sound_touchletters=pygame.mixer.Sound(os.path.join(self.sound_path,"touchletters.wav"))
        self.sound_exitbutton=pygame.mixer.Sound(os.path.join(self.sound_path,"exitbutton.wav"))
        self.sound_buttonletters=pygame.mixer.Sound(os.path.join(self.sound_path,"buttonletters.mp3"))
        self.sound_back=pygame.mixer.Sound(os.path.join(self.sound_path,"pong_back.mp3"))
        self.sound_back.play(loops=-1)
        self.sound_back.set_volume(0.2)
    def objects(self):
        self.object1=Rect(25,150,11,90)
        self.object2=Rect(665,150,11,90)
        self.object3=Rect(self.WIDTH//2-28,self.HEIGHT//2-29,36,36)
    def new_events(self):
        self.EVENT_NEW = pygame.USEREVENT + 1
        pygame.time.set_timer(self.EVENT_NEW,500)
    def get_state(self):
        return np.array([self.object1.x, self.object1.y, self.object2.x, self.object2.y,self.object3.x,self.object3.y])
    def handle_keys(self):
        for event in pygame.event.get():
            self.event_quit(event)
            self.news_events(event)
            self.event_keydown(event)
            if self.main==6:self.event_keys(event)
        self.pressed_keys=pygame.key.get_pressed()
        self.pressed_mouse=pygame.mouse.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()
        self.press_keys()
    def event_quit(self,event):
        if event.type==pygame.QUIT:
            self.sound_exitbutton.play(loops=0)
            self.running,self.game_over=False,True
    def news_events(self,event):
        if event.type == self.EVENT_NEW:
            self.notsound_playing[9],self.notsound_playing[10],self.notsound_playing[13],self.notsound_playing[14],self.notsound_playing[17],self.notsound_playing[18],self.notsound_playing[19]=True,True,True,True,True,True,True
            self.notsound_playing[20],self.notsound_playing[21],self.notsound_playing[22],self.notsound_playing[23],self.notsound_playing[24],self.notsound_playing[25],self.notsound_playing[27]=True,True,True,True,True,True,True
            self.notsound_playing[29]=True
    def event_keydown(self,event):
        if event.type==KEYDOWN:
            if self.main==3 and event.key==K_p:self.main=-1
            elif self.main==-1 and event.key==K_p:self.main=3
            if self.main==3 or self.main==-1:
                if self.speed_up:
                    if event.key==K_KP_PLUS:
                        self.FPS+=15
                        self.speed+=1
                        self.speed_down=True
                        if self.speed==10:self.speed_up=False
                if self.speed_down:
                    if event.key==K_KP_MINUS:
                        self.FPS-=15
                        self.speed-=1
                        self.speed_up=True
                        if self.speed==-1:self.speed_down=False
            if self.main==2:
                if self.color_inputtext1==self.SKYBLUE:
                    if event.key == pygame.K_BACKSPACE:self.text_player1 = self.text_player1[:-1]
                    else:self.text_player1 += event.unicode
                if self.color_inputtext2==self.SKYBLUE:
                    if event.key == pygame.K_BACKSPACE:self.text_player2 = self.text_player2[:-1]
                    else:self.text_player2 += event.unicode
            if self.main==-1:
                if event.key==K_1:save_model(self.model, torch.optim.Adam(self.model.parameters(), lr=0.001),self.model_path)
    def press_keys(self):
        if self.pressed_keys[K_ESCAPE]:self.running=False
        if self.main==-1 and (self.mode_game[1] or self.mode_game[2]):
            if self.pressed_keys[self.config_keys["UP_W"]] and self.object1.top > 0:self.object1.y -= 5
            if self.pressed_keys[self.config_keys["DOWN_S"]] and self.object1.bottom < self.HEIGHT:self.object1.y += 5
        if self.main==-1 and self.mode_game[1]:
            if self.pressed_keys[self.config_keys["UP_ARROW"]] and self.object2.top > 0:self.object2.y -= 5
            if self.pressed_keys[self.config_keys["DOWN_ARROW"]] and self.object2.bottom < self.HEIGHT:self.object2.y += 5
        if self.main==1:
            if self.pressed_keys[K_r]:self.main=-1
            if self.pressed_keys[K_e]:self.main=0
    def images_elements(self):
        self.rotated_ball = pygame.transform.rotate(self.planet, self.object3.x)
        self.screen.blit(self.spacecraft, (-77,self.object1.y-140))
        self.screen.blit(self.spacecraft2, (578,self.object2.y-140))
        self.screen.blit(self.rotated_ball, (self.object3.x,self.object3.y))
    def draw(self):
        self.screen.blit(self.image, (0, 0))
        if self.mode_game[0]:self.draw_generation()
        if self.mode_game[0] or self.mode_game[2]:self.draw_activations(),self.draw_model_data()
        self.images_elements()
        self.scores()
        self.name_players()
        self.mode_speed()
        self.Pause()
        self.main_menu()
        self.game_mode()
        self.options_menu()
        self.visuals_menu()
        self.menu_keys()
        self.Game_over()
    def move_ball(self):
        if self.object3.x>=self.WIDTH-25 or self.object3.x<=0:
            self.value1*=-1
            self.sound.play(loops=1)
            def repeat(reward,objet):
                self.object3.x=300
                self.object3.y=200
                self.reward+=reward
                setattr(self,objet,getattr(self,objet)+1)
            if self.object3.x>=self.WIDTH-25:repeat(-1,"score1")
            if self.object3.x<=0:repeat(1,"score2")
        if self.object3.y>=self.HEIGHT-25 or self.object3.y<=0:self.value2*=-1
        self.ball_collision(0,-1,self.object1)
        self.ball_collision(1,1,self.object2)
        self.object3.x+=self.value1
        self.object3.y+=self.value2
    def ball_collision(self,number1,reward,objet):
        if self.object3.colliderect(objet):
            if self.touch_ball[number1]:
                self.reward+=reward
                self.value1*=-1
                self.sound.play(loops=0)
                self.touch_ball[number1]=False
        else:self.touch_ball[number1]=True
    def scores(self):
        self.screen.blit(self.font.render(f"Score {self.score1}", True, self.YELLOW),(45,380))
        self.screen.blit(self.font.render(f"Score {self.score2}", True, self.YELLOW),(580,380))
    def IA_actions(self,action):
        if action[0]>0 and self.object2.top > 0:self.object2.y -= 5
        if action[0]<0 and self.object2.bottom < self.HEIGHT:self.object2.y += 5
    def restart(self):
        if self.mode_game[0] and (self.score1==self.max_score or self.score2==self.max_score):self.reset(running=False,fps=self.FPS,speed=self.speed,speed_up=self.speed_up,speed_down=self.speed_down)
        if (self.mode_game[1] or self.mode_game[2]) and (self.score1==self.max_score or self.score2==self.max_score):
            self.reset()
            self.main=1
    def player1_code(self):
        if self.object1.top > 0 or self.object1.bottom < self.HEIGHT:self.object1.y+=self.value2
        if self.object1.y>=310:self.object1.y=310
        if self.object1.y<=0:self.object1.y=0
    def draw_activations(self):
        if self.mode_game[2]:self.model=self.model_training
        if self.model.activations is not None:
            activations = self.model.activations
            num_activations = activations.shape[1]
            neuron_positions = [(self.WIDTH - 800 + i * 20, self.HEIGHT // 2) for i in range(num_activations)]
            for pos in neuron_positions:
                pygame.draw.circle(self.screen, self.WHITE, pos, 5)
                pygame.draw.line(self.screen, self.WHITE, (self.WIDTH - 210, self.HEIGHT // 2), pos, 1)
                pygame.draw.line(self.screen, self.WHITE, (self.WIDTH - 190, self.HEIGHT // 2), pos, 1)
            for i in range(num_activations):
                activation_value = activations[0][i]
                activation_value = max(0, min(activation_value, 1))
                color_intensity = int(activation_value * 255)
                color = (color_intensity, color_intensity, color_intensity)
                pygame.draw.circle(self.screen, color, neuron_positions[i], 5)
    def draw_generation(self):
        generation_text = self.font2.render(f"Generation: {self.generation}", True, self.YELLOW)
        self.screen.blit(generation_text, (10, 10))
    def draw_model_data(self):
        if self.mode_game[2]:self.model=self.model_training
        if self.model is not None:
            weights_text = self.font.render(f"Model Weights: {self.model.fc1.weight.data.numpy().flatten()[:5]}", True, self.YELLOW)
            self.screen.blit(weights_text, (10, 50))
            if self.model.activations is not None:
                activations_text = self.font.render(f"Activations: {self.model.activations.flatten()[:5]}", True, self.YELLOW)
                self.screen.blit(activations_text, (10, 70))
    def main_menu(self):
        if self.main==0:
            self.screen.fill(self.BLACK)
            self.screen.blit(self.font4.render("Space Pong", True, self.WHITE),(self.WIDTH//2-245,self.HEIGHT//2-180))
            self.button(self.screen,2,self.font5,"Press To Start",self.WHITE,(self.WIDTH//2-200,self.HEIGHT//2-80),0,self.GOLDEN)
            press_quit=self.button(self.screen,None,self.font5,"Press To Exit",self.WHITE,(self.WIDTH//2-200,self.HEIGHT//2-50),1,self.GOLDEN,False)
            self.button(self.screen,4,self.font5,"Options",self.WHITE,(self.WIDTH-110,self.HEIGHT-40),11,self.GOLDEN)
            if self.pressed_mouse[0] and press_quit.collidepoint(self.mouse_pos):
                self.sound_exitbutton.play(loops=0)
                self.game_over=True
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
            if self.pressed_mouse[0] and close.collidepoint(self.mouse_pos):
                self.sound_exitbutton.play(loops=0)
                self.game_over=True
    def filt(self,number):
        background=pygame.Surface((self.WIDTH,self.HEIGHT),pygame.SRCALPHA)
        background.fill((0,0,0,number))
        self.screen.blit(background,(0,0))
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
            if self.utils_keys[self.key]:
                if event.type==KEYDOWN:
                    self.config_keys[self.key]=event.key
                    self.config_keys[self.key_name]=event.unicode.upper()
                    self.utils_keys[self.key]= not self.utils_keys[self.key]
    def name_players(self):
        self.screen.blit(self.font.render(f"{self.text_player1}", True, self.YELLOW),(45,360))
        self.screen.blit(self.font.render(f"{self.text_player2}", True, self.YELLOW),(580,360))
    def mode_speed(self):
        self.screen.blit(self.font.render(f"Speed: {self.speed}", True, self.YELLOW),(self.WIDTH//2-40,360))
    def reset(self,running=True,fps=60,speed=0,speed_up=True,speed_down=True):
        self.objects()
        self.score1,self.score2=0,0
        self.FPS=fps
        self.speed=speed
        self.speed_up=speed_up
        self.speed_down=speed_down
        self.running=running
    def type_game(self):
        if self.mode_game[0]:self.player1_code()
        self.action_ai(self.model if self.mode_game[0] else self.model_training)
    def action_ai(self,model):
        state=self.get_state()
        action = model(torch.tensor(state, dtype=torch.float32)).detach().numpy()
        self.IA_actions(action)
    def run_with_model(self):
        self.running=True
        score,self.reward=0,0
        while self.running and self.game_over==False:
            self.handle_keys()
            self.draw()
            if self.main==-1:
                if self.mode_game[0] or self.mode_game[2]:self.type_game()
                self.move_ball(),self.restart()
                score =self.reward
            pygame.display.flip()
            self.clock.tick(self.FPS)
        return score