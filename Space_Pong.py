from Interface import *
import numpy as np
class Space_pong_game(interface):
    def __init__(self,model=None):
        super().__init__()
        self.model=model
        self.load_AI()
        self.load_varials()
        self.objects()
        self.draw_buttons()
    def load_varials(self):
        self.running:bool=False
        self.game_over:bool=False
        self.clock=pygame.time.Clock()
        self.FPS:int=60
        self.generation:int=0
        self.value1:int=4
        self.value2:int=4
        self.score1:int=0
        self.score2:int=0
        self.reward:int=0
        self.main:int=0 # -1=game, 0=menu, 1=game over, 2=game mode, 3=pausa, 4=options, 5=visuals, 6=menu keys
        self.color_inputtext1=self.WHITE
        self.color_inputtext2=self.WHITE
        self.text_player1:str="player 1"
        self.text_player2:str="PC"
        self.speed:int=0
        self.speed_up:bool=True
        self.speed_down:bool=True
        self.mode_game:dict[str,bool]={"Training AI":False,"Player":True,"AI":False}
        self.max_score:int=5
        self.touch_ball:list=[True,True]
        self.sound_type:dict={"sound":"Sound ON","color":self.SKYBLUE,"value":True}
        self.utils_keys:dict[str,bool]={"UP_W":False,"DOWN_S":False,"UP_ARROW":False,"DOWN_ARROW":False}
        self.key=None
    def objects(self):
        self.object1=Rect(25,150,11,90)
        self.object2=Rect(665,150,11,90)
        self.object3=Rect(self.WIDTH//2-28,self.HEIGHT//2-29,36,36)
    def get_state(self):
        return np.array([self.object1.x, self.object1.y, self.object2.x, self.object2.y,self.object3.x,self.object3.y])
    def handle_keys(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:self.event_quit()
            self.event_keydown(event)
            self.events_buttons(event)
            if self.main==6:self.event_keys(event)
        self.pressed_keys=pygame.key.get_pressed()
        self.pressed_mouse=pygame.mouse.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()
        self.press_keys()
    def event_quit(self):
        self.sound_exitbutton.play(loops=0)
        self.running,self.game_over=False,True
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
        if self.main==-1 and (self.mode_game["Player"] or self.mode_game["AI"]):
            if self.pressed_keys[self.config_keys["UP_W"]] and self.object1.top > 0:self.object1.y -= 5
            if self.pressed_keys[self.config_keys["DOWN_S"]] and self.object1.bottom < self.HEIGHT:self.object1.y += 5
        if self.main==-1 and self.mode_game["Player"]:
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
        if self.mode_game["Training AI"]:self.draw_generation()
        if self.mode_game["Training AI"] or self.mode_game["AI"]:self.draw_activations(),self.draw_model_data()
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
        if self.mode_game["Training AI"] and (self.score1==self.max_score or self.score2==self.max_score):self.reset(running=False,fps=self.FPS,speed=self.speed,speed_up=self.speed_up,speed_down=self.speed_down)
        if (self.mode_game["Player"] or self.mode_game["AI"]) and (self.score1==self.max_score or self.score2==self.max_score):self.change_mains({"main":1,"command":self.reset})
    def player1_code(self):
        if self.object1.top > 0 or self.object1.bottom < self.HEIGHT:self.object1.y+=self.value2
        if self.object1.y>=310:self.object1.y=310
        if self.object1.y<=0:self.object1.y=0
    def draw_activations(self):
        if self.mode_game["AI"]:self.model=self.model_training
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
        if self.mode_game["AI"]:self.model=self.model_training
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
        if self.mode_game["Training AI"]:self.player1_code()
        self.action_ai(self.model if self.mode_game["Training AI"] else self.model_training)
    def action_ai(self,model):
        state=self.get_state()
        action = model(torch.tensor(state, dtype=torch.float32)).detach().numpy()
        self.IA_actions(action)
    def item_repeat_run(self):
        pygame.display.flip()
        self.clock.tick(self.FPS)
    def run(self):
        self.running=True
        while self.running and all(not mode for mode in self.mode_game.values()):
            self.handle_keys(),self.draw(),self.item_repeat_run()
    def run_with_model(self):
        self.running=True
        self.reward=0
        while self.running and self.game_over==False:
            self.handle_keys(),self.draw()
            if self.main==-1:
                if self.mode_game["Training AI"] or self.mode_game["AI"]:self.type_game()
                self.move_ball(),self.restart()
            self.item_repeat_run()
        return self.reward