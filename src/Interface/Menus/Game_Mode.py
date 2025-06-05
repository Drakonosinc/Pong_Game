from .Base_Menu import BaseMenu
class GameMode(BaseMenu):
    def __init__(self, interface):
        super().__init__(interface)
        self.buttons = {}
    def setup_buttons(self):
        self._setup_navigation_buttons()
        self._setup_mode_buttons()
    def _setup_navigation_buttons(self):
        factory = self.interface.button_factory_f5
        self.buttons['back'] = factory.create_PolygonButton({"position": ((50, 350), (50, 380), (25, 365)),"position2":((50, 340), (50, 390), (10, 365)),"command1":lambda:self.change_mains({"main":0})})
        self.buttons['continue'] = factory.create_PolygonButton({"position": ((650, 350), (650, 380), (675, 365)),"position2":((650, 340), (650, 390), (690, 365)),"command1":lambda:self.change_mains({"main":-1,"run":True,"command":self.interface.objects})})
        self.interface.back_button = self.buttons['back']
        self.interface.continue_button = self.buttons['continue']
    def _setup_mode_buttons(self):
        factory = self.interface.button_factory_f5
        self.buttons['training_ai'] = factory.create_TextButton({"text": "Training AI","position": (self.WIDTH/2-70, self.HEIGHT/2-136),"command1": lambda: self._set_game_mode(training_ai=True),"command2": lambda: self._update_mode_buttons("Training AI")})
        self.buttons['player'] = factory.create_TextButton({"text": "One Vs One","position": (self.WIDTH/2-64, self.HEIGHT/2-110),"command1": lambda: self._set_game_mode(player=True),"command2": lambda: self._update_mode_buttons("Player")})
        self.buttons['ai'] = factory.create_TextButton({"text": "One Vs Ai","position": (self.WIDTH/2-58, self.HEIGHT/2-84),"command1": lambda: self._set_game_mode(ai=True),"command2": lambda: self._update_mode_buttons("AI")})
        self.interface.training_ai_button = self.buttons['training_ai']
        self.interface.player_button = self.buttons['player']
        self.interface.ai_button = self.buttons['ai']
    def _set_game_mode(self, training_ai=False, player=False, ai=False):
        self.interface.mode_game["Training AI"] = training_ai
        self.interface.mode_game["Player"] = player
        if ai and self.interface.model_training is not None:self.interface.mode_game["AI"] = ai
        elif ai:self.interface.load_AI()
    def _update_mode_buttons(self, selected_mode):
        mode_buttons = {
            "Training AI": self.buttons['training_ai'],
            "Player": self.buttons['player'],
            "AI": self.buttons['ai']}
        self.check_item(
            self.interface.mode_game,
            self.interface.SKYBLUE,
            self.interface.WHITE,
            "color",
            **mode_buttons)
    
    def render(self):pass