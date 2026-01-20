from Interface import *
from AI import *
from Events import *
from .GameLogic import *
from Utils import *
class Space_pong_game(interface):
    def __init__(self):
        super().__init__()
        self.model = None
        self.load_varials()
        self.ai_handler = AIHandler(self)
        self.input_handler = InputHandler(self)
        self.visuals_items = Visuals_items(self)
        self.game_logic = GameLogic(self.WIDTH, self.HEIGHT, self.config.config_game, self.mode_game, self.sound)
        self.load_AI()
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
    def restart(self):
        if self.mode_game["Training AI"] and (self.game_logic.player_one.score==self.config.config_game["max_score"] or self.game_logic.player_two.score==self.config.config_game["max_score"]): self.reset(running=False,fps=self.FPS,speed=self.speed,speed_up=self.speed_up,speed_down=self.speed_down)
        if (self.mode_game["Player"] or self.mode_game["AI"]) and (self.game_logic.player_one.score==self.config.config_game["max_score"] or self.game_logic.player_two.score==self.config.config_game["max_score"]): self.change_mains({"main":1,"command":self.reset})
    def reset(self,running=True, fps=60, speed=0, speed_up=True, speed_down=True):
        self.game_logic.reset_game()
        self.FPS = fps
        self.speed = speed
        self.speed_up = speed_up
        self.speed_down = speed_down
        self.running = running
        if hasattr(self, '_qlearning_state'): self.ai_handler.reset_qlearning_state()
    def type_game(self):
        if self.mode_game["Training AI"]: self.game_logic.auto_play_player1()
        self.ai_handler.actions_AI(self.model if self.mode_game["Training AI"] else self.model_training)
    def item_repeat_run(self):
        self.window.update_display()
        self.clock.tick(self.FPS)
    def run(self):
        self.running = True
        while self.running: self.input_handler.handle_input(), self.visuals_items.draw(), self.item_repeat_run()
    def run_with_model(self):
        self.running = True
        self.game_logic.player_two.reward = 0
        while self.running and self.game_over==False:
            self.input_handler.handle_input(), self.visuals_items.draw()
            if self.main==-1:
                if self.mode_game["Training AI"] or self.mode_game["AI"]: self.type_game()
                self.game_logic.update(), self.restart()
            self.item_repeat_run()
        return self.game_logic.player_two.reward