import pygame,os,json
from pygame.locals import *
from Genetic_Algorithm import *
from Interface import *
import numpy as np
class Space_pong_game(interface):
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
            with open(os.path.join(config_path,"config.json"), 'r') as file:config = json.load(file)
            self.config_visuals = config["config_visuals"]
            self.config_keys = config["config_keys"]
        except:self.config(alls=True)
    def config(self,visuals=False,keys=False,alls=False):
        if visuals or alls:self.config_visuals={"WIDTH":700,"HEIGHT":400,
                            "image_background":["background1.jpg","background2.jpg","background3.jpg","background4.jpg","background5.jpg","background6.jpg","background7.jpg","background8.jpg"],
                            "value_background":0,
                            "planets":["Mars.png","Mars1.png","meteorite.png","Saturn.png","earth.png"],
                            "value_planet":0,
                            "spacecrafts":["spaceship.png","spaceship2.png","spaceship3.png"],
                            "value_spacecraft1":0,
                            "value_spacecraft2":0}
        if keys or alls:self.config_keys={"UP_W":K_w,"Name_key1":"W",
                        "DOWN_S":K_s,"Name_key2":"S",
                        "UP_ARROW":K_UP,"Name_key3":"↑",
                        "DOWN_ARROW":K_DOWN,"Name_key4":"↓"}
    def save_config(self):
        config_path = os.path.join(os.path.dirname(__file__), "Config")
        config = {"config_visuals": self.config_visuals,"config_keys": self.config_keys}
        with open(os.path.join(config_path,"config.json"), 'w') as file:json.dump(config, file, indent=4)
    def load_model(self,model):
        self.model=model
        self.model_path=os.path.join(os.path.dirname(__file__), "IA/best_model.pth")
        self.model_training = load_model(self.model_path, 6, 2) if os.path.exists(self.model_path) else None
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
            if event.type==pygame.QUIT:self.event_quit()
            self.news_events(event)
            self.event_keydown(event)
            if self.main==6:self.event_keys(event)
        self.pressed_keys=pygame.key.get_pressed()
        self.pressed_mouse=pygame.mouse.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()
        self.press_keys()
    def event_quit(self):
        self.sound_exitbutton.play(loops=0)
        self.running,self.game_over=False,True
    def news_events(self,event):
        if event.type == self.EVENT_NEW:
            self.notsound_playing[9],self.notsound_playing[10],self.notsound_playing[13],self.notsound_playing[14],self.notsound_playing[17],self.notsound_playing[18],self.notsound_playing[19]=True,True,True,True,True,True,True
            self.notsound_playing[20],self.notsound_playing[21],self.notsound_playing[22],self.notsound_playing[23],self.notsound_playing[24],self.notsound_playing[25],self.notsound_playing[27]=True,True,True,True,True,True,True
            self.notsound_playing[29]=True
    def change_speed(self,fps,speed,number,objet,speed_down=True,speed_up=True):
        self.FPS+=fps
        self.speed+=speed
        self.speed_down=speed_down
        self.speed_up=speed_up
        if self.speed==number:setattr(self,objet,False)
    def input_text(self,event,main,color_objet,objet,objet_text):
        if self.main==main and color_objet==self.SKYBLUE:
            if event.key == K_BACKSPACE:setattr(self,objet,objet_text[:-1])
            else:setattr(self,objet,getattr(self,objet)+event.unicode)
    def event_keydown(self,event):
        if event.type==KEYDOWN:
            if self.main==3 and event.key==K_p:self.main=-1
            elif self.main==-1 and event.key==K_p:self.main=3
            if self.main==3 or self.main==-1:
                if self.speed_up and event.key==K_KP_PLUS:self.change_speed(15,1,10,"speed_up",speed_up=self.speed_up)
                if self.speed_down and event.key==K_KP_MINUS:self.change_speed(-15,-1,-1,"speed_down",speed_down=self.speed_down)
            self.input_text(event,2,self.color_inputtext1,"text_player1",self.text_player1)
            self.input_text(event,2,self.color_inputtext2,"text_player2",self.text_player2)
            if self.main==-1 and event.key==K_1:save_model(self.model, torch.optim.Adam(self.model.parameters(), lr=0.001),self.model_path)
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
        self.menus()
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
        self.screen.blit(self.font2.render(f"Generation: {self.generation}", True, self.YELLOW), (10, 10))
    def draw_model_data(self):
        if self.mode_game[2]:self.model=self.model_training
        if self.model is not None:
            weights_text = self.font.render(f"Model Weights: {self.model.fc1.weight.data.numpy().flatten()[:5]}", True, self.YELLOW)
            self.screen.blit(weights_text, (10, 50))
            if self.model.activations is not None:
                activations_text = self.font.render(f"Activations: {self.model.activations.flatten()[:5]}", True, self.YELLOW)
                self.screen.blit(activations_text, (10, 70))
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
            self.handle_keys(),self.draw()
            if self.main==-1:
                if self.mode_game[0] or self.mode_game[2]:self.type_game()
                self.move_ball(),self.restart()
                score =self.reward
            pygame.display.flip()
            self.clock.tick(self.FPS)
        return score