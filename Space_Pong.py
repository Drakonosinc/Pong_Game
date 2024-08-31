import pygame,os,json
from pygame.locals import *
from Genetic_Algorithm import *
import numpy as np

class Space_pong_game():
    def __init__(self,model=None):
        self.load_config()
        pygame.init()
        pygame.display.set_caption("Pong")
        self.model=model
        self.model_path=os.path.join(os.path.dirname(__file__), "IA/best_model.pth")
        if os.path.exists(self.model_path):self.model_training = load_model(self.model_path, 6, 2)
        else:self.model_training = None
        self.running=False
        self.game_over=False
        self.WIDTH=self.config_visuals["WIDTH"]
        self.HEIGHT=self.config_visuals["HEIGHT"]
        self.screen=pygame.display.set_mode((self.WIDTH,self.HEIGHT))
        self.clock=pygame.time.Clock()
        self.FPS=60
        self.define_colors()
        self.load_images()
        self.load_fonts()
        self.load_sounds()
        self.objects()
        self.generation=0
        self.value1=4
        self.value2=4
        self.score1=0
        self.score2=0
        self.reward=0
        self.counter=0
        self.pause_counter=0
        self.main=4 # -1=game, 0=menu, 1=game over, 2=game mode, 3=pausa, 4=options, 5=visuals, 6=menu keys
        self.color_inputtext1=self.WHITE
        self.color_inputtext2=self.WHITE
        self.colors_game_mode=[self.WHITE,self.WHITE,self.WHITE]
        self.text_player1="player 1"
        self.text_player2="PC"
        self.speed=0
        self.speed_up=True
        self.speed_down=True
        self.notsound_playing=[True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True]
        self.mode_game=[True,False,False]
        self.max_score=5
        self.EVENT_SCORE = pygame.USEREVENT + 1
        pygame.time.set_timer(self.EVENT_SCORE,500)
        self.touch_ball=[True,True]
        self.sound_type={"sound":"Sound ON","color":self.SKYBLUE,"value":True}
    def load_config(self):
        config_path = os.path.join(os.path.dirname(__file__), "Config")
        with open(os.path.join(config_path,"config.txt"), 'r') as file:
            config = json.load(file)
        self.config_visuals = config["config_visuals"]
        self.config_keys = config["config_keys"]
# this method is unnecessary its only use is for quick corrections in the future.
    def config(self):
        # print(event.key) con eso podre tomar el boton que presione y cambiarlo al que quiera
        self.config_visuals={"WIDTH":700,"HEIGHT":400,
                            "image_background":["background1.jpg","background2.jpg","background3.jpg","background4.jpg","background5.jpg","background6.jpg","background7.jpg","background8.jpg"],
                            "value_background":0,
                            "planets":["Mars.png"],
                            "value_planet":0,
                            "spacecrafts":["nave1.png"],
                            "value_spacecraft":0}
        self.config_keys={"UP_W":K_w,"DOWN_S":K_s,
                        "UP_ARROW":K_UP,"DOWN_ARROW":K_DOWN}
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
        self.config_keys["DOWN_S"]=K_s
        self.config_keys["UP_ARROW"]=K_UP
        self.config_keys["DOWN_ARROW"]=K_DOWN
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
        self.planet=pygame.transform.scale(self.planet,(36,36))
        self.spacecraft=pygame.image.load(os.path.join(self.image_path,self.config_visuals["spacecrafts"][self.config_visuals["value_spacecraft"]])).convert_alpha()
        self.spacecraft=pygame.transform.scale(self.spacecraft,(350,200))
        self.spacecraft=pygame.transform.rotate(self.spacecraft,self.angle)
        self.spacecraft2=pygame.transform.rotate(self.spacecraft,self.angle*2)
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
        self.object3=Rect(332,182,36,36)
    def get_state(self):
        return np.array([self.object1.x, self.object1.y, self.object2.x, self.object2.y,self.object3.x,self.object3.y])
    def handle_keys(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.sound_exitbutton.play(loops=0)
                self.running,self.game_over=False,True
            elif event.type == self.EVENT_SCORE:
                self.notsound_playing[9]=True
                self.notsound_playing[10]=True
                self.notsound_playing[13]=True
                self.notsound_playing[14]=True
            if event.type==KEYDOWN:
                if self.main==3 or self.main==-1:
                    if event.key==K_p:
                        self.main=3
                        self.pause_counter+=1
                        if self.pause_counter%2==0:self.main=-1
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
                    if event.key==K_1:save_model(self.model, self.model_path)
        self.pressed_keys=pygame.key.get_pressed()
        self.pressed_mouse=pygame.mouse.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()
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
        self.screen.blit(self.image, (0, 0))
        self.screen.blit(self.spacecraft, (-77,self.object1.y-140))
        self.screen.blit(self.spacecraft2, (578,self.object2.y-140))
        self.screen.blit(self.planet, (self.object3.x,self.object3.y))
    def draw(self):
        self.images_elements()
        if self.mode_game[0]:self.draw_generation()
        if self.mode_game[0] or self.mode_game[2]:
            self.draw_activations()
            self.draw_model_data()
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
            if self.object3.x>=self.WIDTH-25:
                self.score1+=1
                self.reward+=-1
                self.object3.x=300
                self.object3.y=200
            if self.object3.x<=0:
                self.score2+=1
                self.reward+=1
                self.object3.x=300
                self.object3.y=200
        if self.object3.y>=self.HEIGHT-25 or self.object3.y<=0:self.value2*=-1
        if self.object3.colliderect(self.object1):
            if self.touch_ball[0]:
                self.reward+=-1
                self.value1*=-1
                self.sound.play(loops=0)
                self.touch_ball[0]=False
        else:self.touch_ball[0]=True
        if self.object3.colliderect(self.object2):
            if self.touch_ball[1]:
                self.reward+=1
                self.value1*=-1
                self.sound.play(loops=0)
                self.touch_ball[1]=False
        else:self.touch_ball[1]=True
        self.object3.x+=self.value1
        self.object3.y+=self.value2
    def scores(self):
        self.screen.blit(self.font.render(f"Score {self.score1}", True, self.YELLOW),(45,380))
        self.screen.blit(self.font.render(f"Score {self.score2}", True, self.YELLOW),(580,380))
    def IA_actions(self,action):
        if action[0]>0 and self.object2.top > 0:self.object2.y -= 5
        if action[0]<0 and self.object2.bottom < self.HEIGHT:self.object2.y += 5
    def restart(self):
        if self.mode_game[0] and (self.score1==self.max_score or self.score2==self.max_score):
            self.running=False
            self.score1=0
            self.score2=0
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
            # Define las posiciones de las neuronas en la capa oculta
            neuron_positions = [(self.WIDTH - 800 + i * 20, self.HEIGHT // 2) for i in range(num_activations)]
            # Dibuja las conexiones y las neuronas
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
            if self.pressed_mouse[0]:
                if press_quit.collidepoint(self.mouse_pos):
                    self.sound_exitbutton.play(loops=0)
                    self.game_over=True
    def Game_over(self):
        if self.main==1:
            self.screen.fill(self.background)
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
            self.training_ai_button=self.screen.blit(self.font5.render("Training AI",True,self.colors_game_mode[0]),(self.WIDTH/2-70,self.HEIGHT/2-136))
            self.one_vs_one_button=self.screen.blit(self.font5.render("One Vs One",True,self.colors_game_mode[1]),(self.WIDTH/2-64,self.HEIGHT/2-110))
            self.one_vs_ai_button=self.screen.blit(self.font5.render("One Vs Ai",True,self.colors_game_mode[2]),(self.WIDTH/2-58,self.HEIGHT/2-84))
            self.screen.blit(font_modegame.render("Max Score",True,"white"),(self.WIDTH/2-68,self.HEIGHT/2-50))
            self.screen.blit(font_modegame.render(f"{self.max_score}",True,"white"),(self.WIDTH/2-8,self.HEIGHT/2-20))
            self.decrease_point=self.button_arrow(None,((320, 185), (320, 205), (300, 195)),((320, 185), (320, 205), (300, 195)),self.BLACK,7,None,False,(True if self.max_score>1 else False))
            self.increase_point=self.button_arrow(None,((380, 185), (380, 205), (400, 195)),((380, 185), (380, 205), (400, 195)),self.BLACK,8,None,False)
            if self.pressed_mouse[0]:
                self.color_inputtext1=self.SKYBLUE if self.input_player1.collidepoint(self.mouse_pos) else self.WHITE
                self.color_inputtext2=self.SKYBLUE if self.input_player2.collidepoint(self.mouse_pos) else self.WHITE
                if self.training_ai_button.collidepoint(self.mouse_pos):
                    self.mode_game[0],self.mode_game[1],self.mode_game[2]=True,False,False
                    if self.notsound_playing[4]:
                        self.sound_touchletters.play(loops=0)
                        self.notsound_playing[4]=False
                else:self.notsound_playing[4]=True
                if self.one_vs_one_button.collidepoint(self.mouse_pos):
                    self.mode_game[0],self.mode_game[1],self.mode_game[2]=False,True,False
                    if self.notsound_playing[5]:
                        self.sound_touchletters.play(loops=0)
                        self.notsound_playing[5]=False
                else:self.notsound_playing[5]=True
                if self.model_training!=None:
                    if self.one_vs_ai_button.collidepoint(self.mouse_pos):
                        self.mode_game[0],self.mode_game[1],self.mode_game[2]=False,False,True
                        if self.notsound_playing[6]:
                            self.sound_touchletters.play(loops=0)
                            self.notsound_playing[6]=False
                    else:self.notsound_playing[6]=True
                else:
                    if self.one_vs_ai_button.collidepoint(self.mouse_pos) and os.path.exists(self.model_path):self.model_training = load_model(self.model_path, 6, 2)
                if self.increase_point.collidepoint(self.mouse_pos):
                    if self.notsound_playing[9]:
                        self.max_score+=1
                        self.sound_touchletters.play(loops=0)
                        self.notsound_playing[9]=False
                else:self.notsound_playing[9]=True
                if self.decrease_point.collidepoint(self.mouse_pos):
                    if self.notsound_playing[10] and self.max_score>1:
                        self.max_score-=1
                        self.sound_touchletters.play(loops=0)
                        self.notsound_playing[10]=False
                else:self.notsound_playing[10]=True
            self.colors_game_mode[0]=self.SKYBLUE if self.mode_game[0] else self.WHITE
            self.colors_game_mode[1]=self.SKYBLUE if self.mode_game[1] else self.WHITE
            self.colors_game_mode[2]=self.SKYBLUE if self.mode_game[2] else self.WHITE
    def Pause(self):
        if self.main==3:
            self.screen.blit(self.font3.render("Pause",True,"black"),(self.WIDTH/2-105,self.HEIGHT/2-150))
            close=self.button(self.screen,None,self.font2_5,"Exit",self.BLACK,(self.WIDTH/2-40,self.HEIGHT/2-15),3,self.SKYBLUE,False)
            self.button(self.screen,-1,self.font2_5,"Reset",self.BLACK,(self.WIDTH/2-55,self.HEIGHT/2-85),0,self.SKYBLUE,command=self.reset)
            self.button(self.screen,0,self.font2_5,"Menu",self.BLACK,(self.WIDTH/2-45,self.HEIGHT/2-50),1,self.SKYBLUE,command=self.reset)
            if self.pressed_mouse[0]:
                if close.collidepoint(self.mouse_pos):
                    self.sound_exitbutton.play(loops=0)
                    self.game_over=True
    def button(self,screen,main:int,font,text:str,color,position,number:int,color2=None,pressed=True,command=None,detect_mouse=True):
        button=screen.blit(font.render(text,True,color),position)
        if button.collidepoint(self.mouse_pos) and detect_mouse:
            screen.blit(font.render(text,True,color2),position)
            if self.notsound_playing[number]:
                self.sound_buttonletters.play(loops=0)
                self.notsound_playing[number]=False
        else:self.notsound_playing[number]=True
        if self.pressed_mouse[0] and pressed:
            if button.collidepoint(self.mouse_pos):
                self.sound_touchletters.play(loops=0)
                self.main=main
                if command!=None:command()
        if pressed==False:return button
    def button_arrow(self,main,position,position2,color,number:int,number2=None,pressed=True,detect_mouse=True):
        arrow_button=pygame.draw.polygon(self.screen, color, position)
        if arrow_button.collidepoint(self.mouse_pos) and detect_mouse:
            pygame.draw.polygon(self.screen, self.WHITE, position2)
            if self.notsound_playing[number]:
                self.sound_buttonletters.play(loops=0)
                self.notsound_playing[number]=False
        else:self.notsound_playing[number]=True
        if self.pressed_mouse[0] and pressed:
            if arrow_button.collidepoint(self.mouse_pos):
                if self.notsound_playing[number2]:
                    self.sound_touchletters.play(loops=0)
                    self.main=main
                    self.notsound_playing[number2]=False
            else:self.notsound_playing[number2]=True
        if pressed==False:return arrow_button
    def options_menu(self):
        if self.main==4:
            self.screen.fill(self.BLACK)
            self.anim_options()
            self.button_arrow(0,((50, 350), (50, 380), (25, 365)),((50, 340), (50, 390), (10, 365)),self.WHITE,2,13)
    def anim_options(self):
        self.button(self.screen,5,self.font2_5,"Visuals",self.WHITE,(self.WIDTH/2-80,self.HEIGHT/2-150),0,self.GOLDEN,True)
        sound_action=self.button(self.screen,None,self.font2_5,self.sound_type["sound"],self.sound_type["color"],(self.WIDTH/2-80,self.HEIGHT/2-115),1,self.GOLDEN,False)
        self.button(self.screen,6,self.font2_5,"Keys",self.WHITE,(self.WIDTH/2-80,self.HEIGHT/2-80),3,self.GOLDEN,True)
        if self.pressed_mouse[0]:
            if sound_action.collidepoint(self.mouse_pos):
                if self.notsound_playing[14]:
                    self.sound_touchletters.play(loops=0)
                    self.sound_type["value"]=not self.sound_type["value"]
                    self.notsound_playing[14]=False
                    if self.sound_type["value"]:
                        self.sound_type["color"]=self.SKYBLUE
                        self.sound_type["sound"]="Sound ON"
                        self.sound_back.play(loops=-1)
                    else:
                        self.sound_type["color"]=self.RED
                        self.sound_type["sound"]="Sound off"
                        self.sound_back.stop()
            else:self.notsound_playing[14]=True
    def visuals_menu(self):
        if self.main==5:
            self.images_elements()
            self.anim_visuals()
            self.button_arrow(4,((50, 350), (50, 380), (25, 365)),((50, 340), (50, 390), (10, 365)),self.WHITE,2,13)
    def anim_visuals(self):
        self.screen.blit(self.font2_5.render("WIDTH",True,self.WHITE),(self.WIDTH/2-163,self.HEIGHT/2-200))
        self.screen.blit(self.font2_5.render("HEIGHT",True,self.WHITE),(self.WIDTH/2+60,self.HEIGHT/2-200))
        self.screen.blit(self.font2_5.render("IMAGE",True,self.SKYBLUE),(self.WIDTH/2-52,self.HEIGHT/2+160))
        lower_width=self.screen.blit(self.font2_5.render("<",True,self.WHITE),(self.WIDTH/2-200,self.HEIGHT/2-200))
        higher_width=self.screen.blit(self.font2_5.render(">",True,self.WHITE),(self.WIDTH/2-40,self.HEIGHT/2-200))
        lower_height=self.screen.blit(self.font2_5.render("<",True,self.WHITE),(self.WIDTH/2+20,self.HEIGHT/2-200))
        higher_height=self.screen.blit(self.font2_5.render(">",True,self.WHITE),(self.WIDTH/2+200,self.HEIGHT/2-200))
        lower_Ball=self.screen.blit(self.font2_5.render("<",True,self.WHITE),(self.WIDTH/2-40,self.HEIGHT/2-22))
        higher_ball=self.screen.blit(self.font2_5.render(">",True,self.WHITE),(self.WIDTH/2+20,self.HEIGHT/2-22))
        previous_image=self.screen.blit(self.font2_5.render("<",True,self.WHITE),(self.WIDTH/2-80,self.HEIGHT/2+160))
        next_image=self.screen.blit(self.font2_5.render(">",True,self.WHITE),(self.WIDTH/2+65,self.HEIGHT/2+160))
    def menu_keys(self):
        if self.main==6:
            self.screen.fill(self.BLACK)
            self.button_arrow(4,((50, 350), (50, 380), (25, 365)),((50, 340), (50, 390), (10, 365)),self.WHITE,2,13)
    def name_players(self):
        self.screen.blit(self.font.render(f"{self.text_player1}", True, self.YELLOW),(45,360))
        self.screen.blit(self.font.render(f"{self.text_player2}", True, self.YELLOW),(580,360))
    def mode_speed(self):
        self.screen.blit(self.font.render(f"Speed: {self.speed}", True, self.YELLOW),(self.WIDTH//2-40,360))
    def reset(self):
        self.objects()
        self.score1=0
        self.score2=0
        self.pause_counter=0
        self.FPS=60
        self.speed=0
        self.speed_up=True
        self.speed_down=True
        self.running=False
    def run_with_model(self):
        self.running=True
        score = 0
        while self.running and self.game_over==False:
            self.handle_keys()
            self.draw()
            if self.main==-1 and self.mode_game[0]:
                state=self.get_state()
                action = self.model(torch.tensor(state, dtype=torch.float32)).detach().numpy()
                self.IA_actions(action)
                self.move_ball()
                self.player1_code()
                self.restart()
                score =self.reward
            if self.main==-1 and self.mode_game[1]:
                self.move_ball()
                self.restart()
            if self.main==-1 and self.mode_game[2]:
                state=self.get_state()
                action = self.model_training(torch.tensor(state, dtype=torch.float32)).detach().numpy()
                self.IA_actions(action)
                self.move_ball()
                self.restart()
            pygame.display.flip()
            self.clock.tick(self.FPS)
        return score