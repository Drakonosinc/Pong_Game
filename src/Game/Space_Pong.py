from Interface import *
from AI import *
from Events import *
from Events.EventManager import EventManager
from Events.GameEvents import *
from .GameLogic import *
from Utils.States import GameState
from States import *
class Space_pong_game(interface):
    def __init__(self):
        super().__init__()
        self.event_manager = EventManager()
        self.state_manager = StateManager()
        self.model = None
        self.load_varials()
        self.ai_handler = AIHandler(self)
        self.input_handler = InputHandler(self, self.event_manager)
        self.visuals_items = Visuals_items(self)
        self.game_logic = GameLogic(self.WIDTH, self.HEIGHT, self.config.config_game, self.mode_game, self.sound, self.event_manager)
        self.load_AI()
        self.draw_buttons()
        self._register_events()
        self.state_manager.push(MenuState(self))
    def _register_events(self):
        self.event_manager.subscribe(QuitEvent, self.handle_quit_event)
        self.event_manager.subscribe(ToggleFullscreenEvent, self.handle_fullscreen_event)
        self.event_manager.subscribe(PauseGameEvent, self.handle_pause_event)
        self.event_manager.subscribe(ResumeGameEvent, self.handle_resume_event)
        self.event_manager.subscribe(ChangeSpeedEvent, self.handle_speed_event)
        self.event_manager.subscribe(ChangeStateEvent, self.handle_state_change_event)
        self.event_manager.subscribe(SaveModelEvent, self.handle_save_model_event)
    def handle_quit_event(self, event): self.event_quit()
    def handle_fullscreen_event(self, event): self.window.toggle_fullscreen()
    def handle_pause_event(self, event): self.state_manager.change(PauseState(self))
    def handle_resume_event(self, event): self.state_manager.change(PlayingState(self))
    def handle_speed_event(self, event): self.change_speed(event.fps_delta, event.speed_delta, event.limit, event.flag_name)
    def handle_state_change_event(self, event):
        self.change_mains(event.new_state_data)
        target_main = event.new_state_data.get("main")
        state_map = {
            GameState.MENU: MenuState,
            GameState.PLAYING: PlayingState,
            GameState.GAME_OVER: GameOverState,

    def handle_save_model_event(self, event): self.ai_handler.manual_save_model()
    def load_varials(self):
        self.running:bool = False
        self.game_over:bool = False
        self.exit:bool = False
        self.clock = pygame.time.Clock()
        self.FPS:int = 60
        self.generation:int = 0
        self.main: GameState = GameState.MENU
        self.speed:int = 0
        self.speed_up:bool = True
        self.speed_down:bool = True
        self.mode_game:dict[str,bool] = {"Training AI":False,"Player":False,"AI":False}
        sound_status = "ON" if (x:=self.config.config_sounds["sound_main"]) else "OFF"
        self.sound_type:dict = {"sound":f"Sound {sound_status}","color":self.SKYBLUE if x else self.RED,"value":x}
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
        if (self.mode_game["Player"] or self.mode_game["AI"]) and (self.game_logic.player_one.score==self.config.config_game["max_score"] or self.game_logic.player_two.score==self.config.config_game["max_score"]): self.change_mains({"main": GameState.GAME_OVER ,"command":self.reset})
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
        dt = 0 
        while self.running:
            self.input_handler.handle_input()
            self.state_manager.update(dt)
            self.state_manager.draw(self.window.canvas) 
            self.item_repeat_run()
    def run_with_model(self):
        self.running = True
        self.game_logic.player_two.reward = 0
        self.state_manager.change(PlayingState(self))
        self.run()
        return self.game_logic.player_two.reward