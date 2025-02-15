from Interface import *
import numpy as np
from Balls import *
from Players import *
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
        self.exit:bool=False
        self.clock=pygame.time.Clock()
        self.FPS:int=60
        self.generation:int=0
        self.main:int=0 # -1=game, 0=menu, 1=game over, 2=game mode, 3=pausa, 4=options, 5=visuals, 6=menu keys
        self.speed:int=0
        self.speed_up:bool=True
        self.speed_down:bool=True
        self.mode_game:dict[str,bool]={"Training AI":False,"Player":False,"AI":False}
        self.max_score:int=5
        self.sound_type:dict={"sound":f"Sound {"ON" if (x:=self.config_sounds["sound_main"]) else "OFF"}","color":self.SKYBLUE if x else self.RED,"value":x}
        self.utils_keys:dict[str,bool]={"UP_W":False,"DOWN_S":False,"UP_ARROW":False,"DOWN_ARROW":False}
        self.key=None
    def objects(self):
        self.player_one=Player(25,150,11,90)
        self.player_two=Player(665,150,11,90)
        self.balls=[ Ball(self.WIDTH//2-28,self.HEIGHT//2-29,36,36,3+i,3+i) for i in range(1 if self.mode_game["Training AI"] else self.config_game["number_balls"])]
    def get_state(self):
        return np.array([self.player_one.rect.x, self.player_one.rect.y, self.player_two.rect.x, self.player_two.rect.y,self.balls[0].rect.x,self.balls[0].rect.y])
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
        self.type_mode()
        self.game_over,self.running,self.exit=True,False,True
    def change_speed(self,fps,speed,number,objet,speed_down=True,speed_up=True):
        self.FPS+=fps
        self.speed+=speed
        self.speed_down=speed_down
        self.speed_up=speed_up
        if self.speed==number:setattr(self,objet,False)
    def event_keydown(self,event):
        if event.type==KEYDOWN:
            if self.main==3 and event.key==K_p:self.main=-1
            elif self.main==-1 and event.key==K_p:self.main=3
            if self.main==3 or self.main==-1:
                if self.speed_up and event.key==K_KP_PLUS:self.change_speed(15,1,10,"speed_up",speed_up=self.speed_up)
                if self.speed_down and event.key==K_KP_MINUS:self.change_speed(-15,-1,-1,"speed_down",speed_down=self.speed_down)
            if self.main==-1 and event.key==K_1:save_model(self.model, torch.optim.Adam(self.model.parameters(), lr=0.001),self.model_path)
    def press_keys(self):
        if self.pressed_keys[K_ESCAPE]:self.running=False
        if self.main==-1 and (self.mode_game["Player"] or self.mode_game["AI"]):
            if self.pressed_keys[self.config_keys["UP_W"]] and self.player_one.rect.top > 0:self.player_one.rect.y -= 5
            if self.pressed_keys[self.config_keys["DOWN_S"]] and self.player_one.rect.bottom < self.HEIGHT:self.player_one.rect.y += 5
        if self.main==-1 and self.mode_game["Player"]:
            if self.pressed_keys[self.config_keys["UP_ARROW"]] and self.player_two.rect.top > 0:self.player_two.rect.y -= 5
            if self.pressed_keys[self.config_keys["DOWN_ARROW"]] and self.player_two.rect.bottom < self.HEIGHT:self.player_two.rect.y += 5
        if self.main==1:
            if self.pressed_keys[K_r]:self.change_mains({"main":-1})
            if self.pressed_keys[K_e]:self.change_mains({"main":0,"run":True})
    def images_elements(self):
        self.screen.blit(self.spacecraft, (-77,self.player_one.rect.y-140))
        self.screen.blit(self.spacecraft2, (578,self.player_two.rect.y-140))
        for ball in self.balls:
            self.rotated_ball = pygame.transform.rotate(self.planet, ball.rect.x)
            self.screen.blit(self.rotated_ball, (ball.rect.x,ball.rect.y))
    def draw(self):
        self.screen.blit(self.image, (0, 0))
        if self.mode_game["Training AI"]:self.draw_generation()
        if self.mode_game["Training AI"] or self.mode_game["AI"]:self.draw_activations(),self.draw_model_data()
        self.images_elements()
        self.scores()
        self.name_players()
        self.mode_speed()
        self.menus()
    def update(self):
        def repeat(ball,reward):
            ball.move_x*=-1
            self.player_two.reward+=reward
            self.sound.play(loops=0)
        def reset(ball,reward,obj,score):
                ball.rect.x=300
                ball.rect.y=200
                repeat(ball,reward)
                setattr(obj,score,getattr(obj,score)+1)
        def collision(player,obj,reward=1):
            if player.check_collision(obj):
                if player.active:
                    repeat(obj,reward)
                    player.active=False
            else:player.active=True
        for ball in self.balls:
            ball.move_ball(self.WIDTH,self.HEIGHT)
            if ball.rect.x>=self.WIDTH-25:reset(ball,-1,self.player_one,"score")
            if ball.rect.x<=0:reset(ball,1,self.player_two,"score")
            collision(self.player_one,ball,-1,)
            collision(self.player_two,ball,1,)
    def scores(self):
        self.screen.blit(self.font.render(f"Score {self.player_one.score}", True, self.YELLOW),(45,380))
        self.screen.blit(self.font.render(f"Score {self.player_two.score}", True, self.YELLOW),(580,380))
    def IA_actions(self,action):
        if action[0]>0 and self.player_two.top > 0:self.player_two.y -= 5
        if action[0]<0 and self.player_two.bottom < self.HEIGHT:self.player_two.y += 5
    def restart(self):
        if self.mode_game["Training AI"] and (self.player_one.score==self.max_score or self.player_two.score==self.max_score):self.reset(running=False,fps=self.FPS,speed=self.speed,speed_up=self.speed_up,speed_down=self.speed_down)
        if (self.mode_game["Player"] or self.mode_game["AI"]) and (self.player_one.score==self.max_score or self.player_two.score==self.max_score):self.change_mains({"main":1,"command":self.reset})
    def player1_code(self):
        if self.player_one.rect.top > 0 or self.player_one.rect.bottom < self.HEIGHT:self.player_one.rect.y+=self.balls[0].move_y
        if self.player_one.rect.y>=310:self.player_one.rect.y=310
        if self.player_one.rect.y<=0:self.player_one.rect.y=0
    def draw_activations(self):
        if self.mode_game["AI"]:self.model=self.model_training
        if self.model!=None and (self.model.activations is not None):
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
        self.screen.blit(self.font.render(f"{self.input_player1.show_player()}", True, self.YELLOW),(45,360))
        self.screen.blit(self.font.render(f"{self.input_player2.show_player()}", True, self.YELLOW),(580,360))
    def mode_speed(self):
        self.screen.blit(self.font.render(f"Speed: {self.speed}", True, self.YELLOW),(self.WIDTH//2-40,360))
    def reset(self,running=True,fps=60,speed=0,speed_up=True,speed_down=True):
        self.player_one.reset(25,150,11,90)
        self.player_two.reset(665,150,11,90)
        for ball in self.balls:ball.reset(self.WIDTH//2-28,self.HEIGHT//2-29,36,36)
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
        while self.running:self.handle_keys(),self.draw(),self.item_repeat_run()
    def run_with_model(self):
        self.running=True
        self.player_two.reward=0
        while self.running and self.game_over==False:
            self.handle_keys(),self.draw()
            if self.main==-1:
                if self.mode_game["Training AI"] or self.mode_game["AI"]:self.type_game()
                self.update(),self.restart()
            self.item_repeat_run()
        return self.player_two.reward