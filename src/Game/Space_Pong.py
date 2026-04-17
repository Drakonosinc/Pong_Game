import queue
import threading
import pygame
from AI import *
from Events import *
from .GameLogic import *
from Utils import *
from States import *
from Core import *
from Loaders import *
from Interface import *
from src.Infrastructure.Services.PygameAudioService import PygameAudioService
class Space_pong_game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Space Pong")
        self.event_manager = EventManager()
        self.config_loader = Config()
        self.config_loader.load_config()
        self.config = self.config_loader
        self.WIDTH = self.config.config_visuals["WIDTH"]
        self.HEIGHT = self.config.config_visuals["HEIGHT"]
        self.window_manager = WindowManager("Space Pong AI", self.WIDTH, self.HEIGHT)
        self.asset_manager = AssetManager(self.config, self.window_manager)
        self.audio_service = PygameAudioService(self.asset_manager)
        self.context = GameContext(
            config=self.config,
            assets=self.asset_manager,
            event_manager=self.event_manager,
            window_manager=self.window_manager,)
        self.load_varials()
        self.input_handler = InputHandler(self, self.event_manager)
        self.game_logic = GameLogic(
            self.WIDTH,
            self.HEIGHT,
            self.config.config_game,
            self.mode_game,
            self.audio_service,
            self.event_manager,)
        self.ui = Interface(self.context)
        self.ui.bind_game(self)
        self.ui.game_logic = self.game_logic
        self.ui.mode_game = self.mode_game
        self.visuals_items = Visuals_items(self)
        self.ai_handler = AIHandler(self)
        self.model_training = None
        self.model = None
        self.ai_load_error = None
        self.ai_runtime_state = "idle"
        self.saved_model_state = "unknown"
        self.ai_preload_thread = None
        self.ai_preload_queue = queue.Queue()
        self.ai_preload_request_id = 0
        self._ai_preload_started = False
        self._first_frame_presented = False
        self.state_factory = StateFactory(self)
        self.state_manager = StateManager(self.state_factory)
        self._register_events()
        self.state_manager.change_state(GameState.MENU)
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
    def handle_pause_event(self, event): self.state_manager.change_state(GameState.PAUSE)
    def handle_resume_event(self, event): self.state_manager.change_state(GameState.PLAYING)
    def handle_speed_event(self, event): self.change_speed(event.fps_delta, event.speed_delta, event.limit, event.flag_name)
    def handle_save_model_event(self, event): self.ai_handler.manual_save_model()
    def handle_state_change_event(self, event):
        self.change_mains(event.new_state_data)
        target_main = event.new_state_data.get("main")
        if target_main: self.state_manager.change_state(target_main, params=event.new_state_data)
    def change_mains(self, data):
        if "main" in data: self.main = data["main"]
    def load_varials(self):
        self.running = False
        self.game_over = False
        self.exit = False
        self._shutdown_done = False
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.generation = 0
        self.main = GameState.MENU
        self.speed = 0
        self.speed_up = True
        self.speed_down = True
        self.mode_game = {"Training AI": False, "Player": False, "AI": False}
        sound_enabled = self.config.config_sounds["sound_main"]
        sound_status = "ON" if sound_enabled else "OFF"
        self.sound_type = {
            "sound": f"Sound {sound_status}",
            "color": self.context.assets.SKYBLUE if sound_enabled else self.context.assets.RED,
            "value": sound_enabled,}
        self.utils_keys = {"UP_W": False, "DOWN_S": False, "UP_ARROW": False, "DOWN_ARROW": False}
    def event_quit(self):
        if self.exit: return
        try: self.ui.sound_exitbutton.play(loops=0)
        except pygame.error: pass
        self.game_over, self.running, self.exit = True, False, True
    def shutdown(self):
        if self._shutdown_done: return
        self._shutdown_done = True
        self.running = False
        self.game_over = True
        self.exit = True
        if pygame.get_init(): pygame.quit()
    def _load_ai_in_background(self, request_id: int):
        result = AILoader(self.config).load_model_result()
        self.ai_preload_queue.put((request_id, result))
    def request_ai_preload(self, force: bool = False):
        if self.ai_preload_thread is not None and self.ai_preload_thread.is_alive(): return False
        if not force and self._ai_preload_started: return False
        self._ai_preload_started = True
        self.ai_preload_request_id += 1
        self.ai_runtime_state = "loading"
        self.saved_model_state = "loading"
        self.ai_load_error = None
        self.model_training = None
        self.ui.model_training = None
        self.ai_handler.clear_model()
        request_id = self.ai_preload_request_id
        self.ai_preload_thread = threading.Thread(
            target=self._load_ai_in_background,
            args=(request_id,),
            name="ai-preload",
            daemon=True,)
        self.ai_preload_thread.start()
        return True
    def poll_ai_preload_result(self):
        while True:
            try: request_id, result = self.ai_preload_queue.get_nowait()
            except queue.Empty: break
            if request_id != self.ai_preload_request_id: continue
            self.apply_loaded_ai_result(result)
    def apply_loaded_ai_result(self, result):
        self.model_training = result.model
        self.ui.model_training = result.model
        self.ai_load_error = result.error_message
        if result.error_message:
            self.ai_runtime_state = "error"
            self.saved_model_state = "error"
            self.ai_handler.clear_model()
            return
        self.ai_runtime_state = "ready"
        self.saved_model_state = "ready" if result.model_found and result.model is not None else "not_found"
        if result.model is not None: self.ai_handler.set_runtime_model(result.model)
        else: self.ai_handler.clear_model()
    def publish_runtime_model(self, model):
        if model is None: return
        self.model = model
        self.model_training = model
        self.ui.model_training = model
        self.ai_load_error = None
        self.ai_runtime_state = "ready"
        self.saved_model_state = "ready"
        self.ai_handler.set_runtime_model(model)
    def can_use_training_ai(self): return self.ai_runtime_state == "ready"
    def can_use_saved_model_ai(self): return self.ai_runtime_state == "ready" and self.saved_model_state == "ready" and self.model_training is not None
    def can_continue_selected_mode(self):
        if self.mode_game["Player"]: return True
        if self.mode_game["Training AI"]: return self.can_use_training_ai()
        if self.mode_game["AI"]: return self.can_use_saved_model_ai()
        return False
    def get_ai_status(self):
        if self.ai_runtime_state in ("idle", "loading"): return "AI: cargando...", self.context.assets.GOLDEN
        if self.ai_runtime_state == "error":
            message = self.ai_load_error or "Error cargando IA"
            if len(message) > 48: message = message[:45] + "..."
            return f"AI: {message}", self.context.assets.RED
        if self.saved_model_state == "not_found": return "AI: Modelo no encontrado", self.context.assets.YELLOW
        return "AI: lista", self.context.assets.SKYBLUE
    def _mark_first_frame_presented(self):
        if self._first_frame_presented:return
        self._first_frame_presented = True
        self.request_ai_preload()
    def change_speed(self, fps, speed, number, objet, speed_down=True, speed_up=True):
        self.FPS += fps
        self.speed += speed
        self.speed_down = speed_down
        self.speed_up = speed_up
        if self.speed == number: setattr(self, objet, False)
    def restart(self):
        p1_score = self.game_logic.player_one.score
        p2_score = self.game_logic.player_two.score
        max_score = self.config.config_game["max_score"]
        reached_limit = p1_score == max_score or p2_score == max_score
        if self.mode_game["Training AI"] and reached_limit:
            self.reset(running=False, fps=self.FPS, speed=self.speed, speed_up=self.speed_up, speed_down=self.speed_down)
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
        if hasattr(self, "_qlearning_state"): self.ai_handler.reset_qlearning_state()
    def type_game(self):
        if self.mode_game["Training AI"]: self.game_logic.auto_play_player1()
    def item_repeat_run(self):
        if not self.mode_game["Training AI"]:
            self.window_manager.update_display()
            self.clock.tick(self.FPS)
            self._mark_first_frame_presented()
            return
        if self.speed < 100:
            self.window_manager.update_display()
            self.clock.tick(self.FPS + self.speed)
            self._mark_first_frame_presented()
    def run(self):
        self.running = True
        dt = 0
        while self.running:
            self.input_handler.handle_input()
            self.poll_ai_preload_result()
            self.state_manager.update(dt)
            if not self.mode_game["Training AI"] or self.speed < 100: self.state_manager.draw(self.window_manager.canvas)
            self.item_repeat_run()
    def run_with_model(self):
        self.running = True
        self.game_logic.player_two.reward = 0
        self.state_manager.change_state(GameState.PLAYING)
        self.run()
        return self.game_logic.player_two.reward
    def events_buttons(self, event): self.ui.events_buttons(event)