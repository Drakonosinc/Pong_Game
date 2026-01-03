from Interface import *
from Entities import *
from AI import *
from Type_Training import *
from Events import *
from GameLogic import *
class Space_pong_game(interface):
    def __init__(self):
        super().__init__()
        self.model = None
        self.ai_handler = AIHandler(self)
        self.input_handler = InputHandler(self)
        self.visuals_items = Visuals_items(self)
        self.game_logic = GameLogic(self)
        self.load_AI()
        self.load_varials()
        self.objects()
        self.draw_buttons()
    def load_varials(self):
        self.running:bool = False
        self.game_over:bool = False
        self.exit:bool = False
        self.clock = pygame.time.Clock()
        self.FPS:int = 60
        self.generation:int = 0
        self.main:int = 0 # -1=game, 0=menu, 1=game over, 2=game mode, 3=pausa, 4=options, 5=visuals, 6=menu keys
        self.speed:int = 0
        self.speed_up:bool = True
        self.speed_down:bool = True
        self.mode_game:dict[str,bool] = {"Training AI":False,"Player":False,"AI":False}
        self.sound_type:dict = {"sound":f"Sound {"ON" if (x:=self.config.config_sounds["sound_main"]) else "OFF"}","color":self.SKYBLUE if x else self.RED,"value":x}
        self.utils_keys:dict[str,bool] = {"UP_W":False,"DOWN_S":False,"UP_ARROW":False,"DOWN_ARROW":False}
    def objects(self):
        self.balls = [ Ball(self.WIDTH//2-28,self.HEIGHT//2-29,36,36,4+i,4+i) for i in range(1 if self.mode_game["Training AI"] else self.config.config_game["number_balls"])]
        self.player_one = Player(25,150,11,90,[True] * len(self.balls))
        self.player_two = Player(665,150,11,90,[True] * len(self.balls))
    def event_quit(self):
        self.sound_exitbutton.play(loops=0)
        self.type_game()
        self.game_over, self.running, self.exit = True, False, True
    def change_speed(self, fps, speed, number, objet, speed_down=True, speed_up=True):
        self.FPS += fps
        self.speed += speed
        self.speed_down = speed_down
        self.speed_up = speed_up
        if self.speed==number: setattr(self,objet,False)
    def manual_save_model(self):
        if self.config.config_AI["type_training"]["Genetic"]: save_genetic_model(self.model, torch.optim.Adam(self.model.parameters(), lr=0.001), self.model_path)
        elif self.config.config_AI["type_training"]["Q-learning"]: save_qlearning_model(self.model, torch.optim.Adam(self.model.parameters(), lr=0.001), self.model_path)
    def update(self):
        def repeat(ball, reward):
            ball.handle_collision(self.player_two,reward)
            self.sound.play(loops=0)
        def reset(ball, reward, player):
            ball.rect = Rect(*ball.reset_position)
            repeat(ball,reward)
            player.update_score(1)
        def collision(player, ball, i, reward=1):
            if player.check_collision(ball):
                if player.active[i]:
                    repeat(ball,reward)
                    player.active[i] = False
            else: player.active[i] = True
        for i, ball in enumerate(self.balls):
            ball.move_ball(self.WIDTH,self.HEIGHT)
            if ball.rect.x>=self.WIDTH-25: reset(ball,-1,self.player_one)
            if ball.rect.x<=0: reset(ball,1,self.player_two)
            collision(self.player_one,ball,i,-1)
            collision(self.player_two,ball,i,1)
    def restart(self):
        if self.mode_game["Training AI"] and (self.player_one.score==self.config.config_game["max_score"] or self.player_two.score==self.config.config_game["max_score"]): self.reset(running=False,fps=self.FPS,speed=self.speed,speed_up=self.speed_up,speed_down=self.speed_down)
        if (self.mode_game["Player"] or self.mode_game["AI"]) and (self.player_one.score==self.config.config_game["max_score"] or self.player_two.score==self.config.config_game["max_score"]): self.change_mains({"main":1,"command":self.reset})
    def player1_code(self):
        if self.player_one.rect.top > 0 or self.player_one.rect.bottom < self.HEIGHT: self.player_one.rect.y+=self.balls[0].move_y
        if self.player_one.rect.y>=310: self.player_one.rect.y=310
        if self.player_one.rect.y<=0: self.player_one.rect.y=0
    def reset(self,running=True, fps=60, speed=0, speed_up=True, speed_down=True):
        self.player_one.reset()
        self.player_two.reset()
        for ball in self.balls: ball.reset()
        self.FPS = fps
        self.speed = speed
        self.speed_up = speed_up
        self.speed_down = speed_down
        self.running = running
        if hasattr(self, '_qlearning_state'): self.ai_handler.reset_qlearning_state()
    def type_game(self):
        if self.mode_game["Training AI"]: self.player1_code()
        self.ai_handler.actions_AI(self.model if self.mode_game["Training AI"] else self.model_training)
    def item_repeat_run(self):
        pygame.display.flip()
        self.clock.tick(self.FPS)
    def run(self):
        self.running = True
        while self.running: self.input_handler.handle_input(), self.draw(), self.item_repeat_run()
    def run_with_model(self):
        self.running = True
        self.player_two.reward = 0
        while self.running and self.game_over==False:
            self.input_handler.handle_input(), self.draw()
            if self.main==-1:
                if self.mode_game["Training AI"] or self.mode_game["AI"]: self.type_game()
                self.update(), self.restart()
            self.item_repeat_run()
        return self.player_two.reward