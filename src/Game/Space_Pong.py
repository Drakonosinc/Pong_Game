import pygame
from AI import *
from Events import *
from .GameLogic import *
from Utils import *
from States import *
from Core import *
from Loaders import *
from Interface import * 
class Space_pong_game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Space Pong")
        self.event_manager = EventManager()
        self.state_manager = StateManager()
        self.config_loader = Config()
        self.config_loader.load_config()
        self.config = self.config_loader
        w = self.config.config_visuals["WIDTH"]
        h = self.config.config_visuals["HEIGHT"]
        self.window_manager = WindowManager("Space Pong AI", w, h)
        self.asset_manager = AssetManager(self.config, self.window_manager)
        self.context = GameContext(
            config=self.config,
            assets=self.asset_manager,
            event_manager=self.event_manager,
            window_manager=self.window_manager)
        self.load_varials()
        self.input_handler = InputHandler(self, self.event_manager)
        self.game_logic = GameLogic(w, h, self.config.config_game, self.mode_game, self.asset_manager.sound, self.event_manager)
        self.ui = Interface(self.context)
        self.ui.game_logic = self.game_logic
        self.visuals_items = Visuals_items(self)
        self.ai_handler = AIHandler(self)
        self.state_factory = StateFactory(self)
        ai_loader = AILoader(self.context)
        self.model_training = ai_loader.load_model()
        self.model = None
        self._register_events()
        initial_state = self.state_factory.get_state(GameState.MENU)
        self.state_manager.push(initial_state)
    @property
    def sound(self): return self.context.assets
    @property
    def window(self): return self.window_manager
    def _register_events(self):
        self.event_manager.subscribe(QuitEvent, self.handle_quit_event)
        self.event_manager.subscribe(ToggleFullscreenEvent, self.handle_fullscreen_event)
        self.event_manager.subscribe(PauseGameEvent, self.handle_pause_event)
        self.event_manager.subscribe(ResumeGameEvent, self.handle_resume_event)
        self.event_manager.subscribe(ChangeSpeedEvent, self.handle_speed_event)
        self.event_manager.subscribe(ChangeStateEvent, self.handle_state_change_event)
        self.event_manager.subscribe(SaveModelEvent, self.handle_save_model_event)
    def handle_quit_event(self, event): self.event_quit()
    def handle_fullscreen_event(self, event): self.window_manager.toggle_fullscreen()
    def handle_pause_event(self, event): self.state_manager.change(self.state_factory.get_state(GameState.PAUSE))
    def handle_resume_event(self, event): self.state_manager.change(self.state_factory.get_state(GameState.PLAYING))
    def handle_speed_event(self, event): self.change_speed(event.fps_delta, event.speed_delta, event.limit, event.flag_name)
    def handle_save_model_event(self, event): self.ai_handler.manual_save_model()
    def handle_state_change_event(self, event):
        self.change_mains(event.new_state_data)
        target_main = event.new_state_data.get("main")
        new_state = self.state_factory.get_state(target_main)
        if new_state: self.state_manager.change(new_state, params=event.new_state_data)
    def change_mains(self, data):
        if "main" in data: self.main = data["main"]
    def load_varials(self):
        self.running = False
        self.game_over = False
        self.exit = False
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.generation = 0
        self.main = GameState.MENU
        self.speed = 0
        self.speed_up = True
        self.speed_down = True
        self.mode_game = {"Training AI":False,"Player":False,"AI":False}
        sound_status = "ON" if (x:=self.config.config_sounds["sound_main"]) else "OFF"
        self.sound_type = {"sound":f"Sound {sound_status}","color":self.context.assets.SKYBLUE if x else self.context.assets.RED,"value":x}
        self.utils_keys = {"UP_W":False,"DOWN_S":False,"UP_ARROW":False,"DOWN_ARROW":False}
    def event_quit(self):
        self.ui.sound_exitbutton.play(loops=0)
        self.type_game()
        self.game_over, self.running, self.exit = True, False, True
    def change_speed(self, fps, speed, number, objet, speed_down=True, speed_up=True):
        self.FPS += fps
        self.speed += speed
        self.speed_down = speed_down
        self.speed_up = speed_up
        if self.speed==number: setattr(self,objet,False)
    def restart(self):
        p1_score = self.game_logic.player_one.score
        p2_score = self.game_logic.player_two.score
        max_score = self.config.config_game["max_score"]
        reached_limit = (p1_score == max_score or p2_score == max_score)
        if self.mode_game["Training AI"] and reached_limit: self.reset(running=False, fps=self.FPS, speed=self.speed, speed_up=self.speed_up, speed_down=self.speed_down)
        if (self.mode_game["Player"] or self.mode_game["AI"]) and reached_limit:
            self.change_mains({"main": GameState.GAME_OVER})
            self.reset()
    def reset(self, running=True, fps=60, speed=0, speed_up=True, speed_down=True):
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
        self.window_manager.update_display()
        self.clock.tick(self.FPS)
    def run(self):
        self.running = True
        dt = 0 
        while self.running:
            self.input_handler.handle_input()
            self.state_manager.update(dt)
            self.state_manager.draw(self.window_manager.canvas) 
            self.item_repeat_run()
    def run_with_model(self):
        self.running = True
        self.game_logic.player_two.reward = 0
        self.state_manager.change(self.state_factory.get_state(GameState.PLAYING))
        self.run()
        return self.game_logic.player_two.reward
    def events_buttons(self, event): self.ui.events_buttons(event)