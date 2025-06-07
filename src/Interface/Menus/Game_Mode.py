import os, pygame
from .Base_Menu import BaseMenu
class GameMode(BaseMenu):
    def __init__(self, interface):
        super().__init__(interface)
        self.buttons = {}
        self.inputs = {}
        self.config_buttons = {}
        self.training_ai_elements = {}
    def setup_buttons(self):
        self._setup_navigation_buttons()
        self._setup_mode_buttons()
        self._setup_score_buttons()
        self._setup_input_fields()
        self._setup_training_ai_elements()
        self._setup_config_game_buttons()
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
        mode_buttons = {"Training AI": self.buttons['training_ai'],"Player": self.buttons['player'],"AI": self.buttons['ai']}
        self.check_item(self.interface.mode_game,self.interface.SKYBLUE,self.interface.WHITE,"color",**mode_buttons)
    def _setup_score_buttons(self):
        factory = self.interface.button_factory_f5
        self.buttons['decrease_score'] = factory.create_PolygonButton({"color": self.interface.BLACK,"position": ((320, 185), (320, 205), (300, 195)),"color2": self.interface.WHITE,"command1": lambda: self.increase_decrease_variable(self.config.config_game, "max_score", True, -1)})
        self.buttons['increase_score'] = factory.create_PolygonButton({"color": self.interface.BLACK,"position": ((380, 185), (380, 205), (400, 195)),"color2": self.interface.WHITE,"command1": lambda: self.increase_decrease_variable(self.config.config_game, "max_score")})
        self.interface.decrease_score_button = self.buttons['decrease_score']
        self.interface.increase_score_button = self.buttons['increase_score']
    def _setup_input_fields(self):
        factory = self.interface.button_factory_f5
        self.inputs['player1'] = factory.create_InputText({"text": "Player","color":(0,0,0),"position": (8,40,271,25)})
        self.inputs['player2'] = factory.create_InputText({"text": "PC","color":(0,0,0),"position": (418,40,275,25)})
        self.interface.input_player1 = self.inputs['player1']
        self.interface.input_player2 = self.inputs['player2']
    def _setup_training_ai_elements(self):
        self._setup_training_ai_buttons()
        self._setup_training_ai_texts()
        self._setup_scroll_bar()
    def _setup_training_ai_buttons(self):
        factory = self.interface.button_factory_f5
        self.config_buttons['increase_generation'] = factory.create_TextButton({"text": ">","position": (self.WIDTH-100, self.HEIGHT/2-55),"command1": lambda: self.increase_decrease_variable(self.config.config_AI, 'generation_value'),"command2": self._update_training_ai_texts})
        self.config_buttons['decrease_generation'] = factory.create_TextButton({"text": "<","position": (self.WIDTH-178, self.HEIGHT/2-55),"command1": lambda: self.increase_decrease_variable(self.config.config_AI, 'generation_value', True, -1),"command2": self._update_training_ai_texts})
        self.config_buttons['increase_population'] = factory.create_TextButton({"text": ">","position": (self.WIDTH-100, self.HEIGHT/2),"command1": lambda: self.increase_decrease_variable(self.config.config_AI, 'population_value'),"command2": self._update_training_ai_texts})
        self.config_buttons['decrease_population'] = factory.create_TextButton({"text": "<","position": (self.WIDTH-178, self.HEIGHT/2),"command1": lambda: self.increase_decrease_variable(self.config.config_AI, 'population_value', True, -1),"command2": self._update_training_ai_texts})
        self.config_buttons['increase_try_for_ai'] = factory.create_TextButton({"text": ">","position": (self.WIDTH-100, self.HEIGHT/2+55),"command1": lambda: self.increase_decrease_variable(self.config.config_AI, 'try_for_ai'),"command2": self._update_training_ai_texts})
        self.config_buttons['decrease_try_for_ai'] = factory.create_TextButton({"text": "<","position": (self.WIDTH-178, self.HEIGHT/2+55),"command1": lambda: self.increase_decrease_variable(self.config.config_AI, 'try_for_ai', True, -1),"command2": self._update_training_ai_texts})
        self.config_buttons['save_model'] = factory.create_TextButton({"text": "OFF","color": self.interface.SKYBLUE,"position": (self.WIDTH-85, self.HEIGHT/2+84),"command1": lambda: self.on_off(self.config.config_AI, "model_save"),"command2": self.config.save_config})
        self.config_buttons['box_type_model'] = factory.create_ComboBox({"text": "Model","position": (self.WIDTH/2+120, self.HEIGHT/2+139)})
        for key, button in self.config_buttons.items():setattr(self.interface, key, button)
    def _setup_training_ai_texts(self):
        factory = self.interface.button_factory_f5
        self.training_ai_elements['text_C'] = factory.create_Text({"text": f"Config Training\n{'AI':^26}","position": (self.WIDTH/2+120, self.HEIGHT/2-136),"detect_mouse": False})
        self.training_ai_elements['text_G'] = factory.create_Text({"text": f"Generation Size\n{self.config.config_AI['generation_value']:^26}","position": (self.WIDTH/2+120, self.HEIGHT/2-81),"detect_mouse": False})
        self.training_ai_elements['text_P'] = factory.create_Text({"text": f"Population Size\n{self.config.config_AI['population_value']:^26}","position": (self.WIDTH/2+120, self.HEIGHT/2-26),"detect_mouse": False})
        self.training_ai_elements['text_A'] = factory.create_Text({"text": f"Attempts By AI\n{self.config.config_AI['try_for_ai']:^{28 if self.config.config_AI['try_for_ai']<10 else 26}}","position": (self.WIDTH/2+120, self.HEIGHT/2+29),"detect_mouse": False})
        self.training_ai_elements['text_S'] = factory.create_Text({"text": "Save model","position": (self.WIDTH/2+120, self.HEIGHT/2+84),"detect_mouse": False})
        self.interface.text_in_training_ai = list(self.training_ai_elements.values())
    def _setup_scroll_bar(self):
        factory = self.interface.button_factory_f5
        self.config_buttons['scroll'] = factory.create_ScrollBar({"position": (self.WIDTH-30, 100, 20, self.HEIGHT-200),"thumb_height": 20})
        self.interface.scroll = self.config_buttons['scroll']
    def _setup_config_game_buttons(self):
        factory = self.interface.button_factory_f5
        self.config_buttons['increase_balls'] = factory.create_TextButton({"text": ">","position": (self.WIDTH-100, self.HEIGHT/2-55),"command1": lambda: self.increase_decrease_variable(self.config.config_game, 'number_balls'),"command2": self.interface.objects()})
        self.config_buttons['decrease_balls'] = factory.create_TextButton({"text": "<","position": (self.WIDTH-178, self.HEIGHT/2-55),"command1": lambda: self.increase_decrease_variable(self.config.config_game, 'number_balls', True, -1),"command2": self.interface.objects()})
        self.interface.increase_balls = self.config_buttons['increase_balls']
        self.interface.decrease_balls = self.config_buttons['decrease_balls']
    def _update_training_ai_texts(self):
        if 'text_G' in self.training_ai_elements:self.training_ai_elements['text_G'].change_item({"text": f"Generation Size\n{self.config.config_AI['generation_value']:^26}"})
        if 'text_P' in self.training_ai_elements:self.training_ai_elements['text_P'].change_item({"text": f"Population Size\n{self.config.config_AI['population_value']:^26}"})
        if 'text_A' in self.training_ai_elements:self.training_ai_elements['text_A'].change_item({"text": f"Attempts By AI\n{self.config.config_AI['try_for_ai']:^{28 if self.config.config_AI['try_for_ai'] < 10 else 26}}"})
    def _update_score_button_state(self):
        self.buttons['decrease_score'].change_item({"pressed": can_decrease,"detect_mouse": can_decrease})
    def render(self):
        self.screen.fill(self.interface.BLACK)
        font_modegame = pygame.font.Font(os.path.join(self.interface.font_path, "8bitOperatorPlusSC-Bold.ttf"), 22)
        self._render_main_texts(font_modegame)
        if self.interface.mode_game["Training AI"]:self._render_training_ai()
        else:self._render_game_options()
        self._render_main_buttons()
        self._update_score_button_state()
    def _render_main_texts(self, font_modegame):
        self.screen.blit(font_modegame.render("Game Mode", True, "white"), (self.WIDTH/2-70, self.HEIGHT/2-162))
        self.screen.blit(self.interface.font5.render("Enter Player Name One", True, "white"), (7, 10))
        self.screen.blit(self.interface.font5.render("Enter Player Name Two", True, "white"), (416, 10))
        self.screen.blit(font_modegame.render("Max Score", True, "white"), (self.WIDTH/2-68, self.HEIGHT/2-50))
        self.screen.blit(font_modegame.render(f"{self.config.config_game['max_score']}", True, "white"), (self.WIDTH/2-8, self.HEIGHT/2-20))
    def _render_training_ai(self):pass