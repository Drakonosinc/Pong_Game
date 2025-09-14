import os, pygame
from .Base_Menu import BaseMenu
class GameMode(BaseMenu):
    def __init__(self, interface):
        super().__init__(interface)
        self.buttons = {}
        self.inputs = {}
        self.config_buttons = {}
        self.config_genetic_buttons = {}
        self.config_qlearning_buttons = {}
        self.training_genetic_elements = {}
        self.training_qlearning_elements = {}
    def setup_buttons(self):
        self._setup_navigation_buttons()
        self._setup_mode_buttons()
        self._setup_score_buttons()
        self._setup_input_fields()
        self._setup_type_training_buttons()
        self._setup_training_genetic_elements()
        self._setup_training_qlearning_elements()
        self._setup_scroll_bar()
        self._setup_config_game_buttons()
    def _setup_navigation_buttons(self):
        factory = self.interface.button_factory_f5
        self.buttons['back'] = factory.create_PolygonButton({"position": ((50, 350), (50, 380), (25, 365)),"position2":((50, 340), (50, 390), (10, 365)),"command1":lambda:self.change_mains({"main":0})})
        self.buttons['continue'] = factory.create_PolygonButton({"position": ((650, 350), (650, 380), (675, 365)),"position2":((650, 340), (650, 390), (690, 365)),"command1":lambda:self.change_mains({"main":-1,"run":True,"command":self.interface.objects})})
        self.interface.back_button = self.buttons['back']
        self.interface.continue_button = self.buttons['continue']
    def _setup_mode_buttons(self):
        factory = self.interface.button_factory_f5
        self.buttons['training_ai'] = factory.create_TextButton({"text": "Training AI","position": (self.WIDTH/2-70, self.HEIGHT/2-136),"command1": lambda: self._set_game_mode(training_ai=True),"command2": lambda: self._update_mode_buttons()})
        self.buttons['player'] = factory.create_TextButton({"text": "One Vs One","position": (self.WIDTH/2-64, self.HEIGHT/2-110),"command1": lambda: self._set_game_mode(player=True),"command2": lambda: self._update_mode_buttons()})
        self.buttons['ai'] = factory.create_TextButton({"text": "One Vs Ai","position": (self.WIDTH/2-58, self.HEIGHT/2-84),"command1": lambda: self._set_game_mode(ai=True),"command2": lambda: self._update_mode_buttons()})
        self.interface.training_ai_button = self.buttons['training_ai']
        self.interface.player_button = self.buttons['player']
        self.interface.ai_button = self.buttons['ai']
    def _set_game_mode(self, training_ai=False, player=False, ai=False):
        self.interface.mode_game["Training AI"] = training_ai
        self.interface.mode_game["Player"] = player
        if self.interface.model_training is not None:self.interface.mode_game["AI"] = ai
        elif ai:self.interface.load_AI()
    def _update_mode_buttons(self):
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
    def _setup_training_genetic_elements(self):
        self._setup_training_genetic_buttons()
        self._setup_training_genetic_texts()
    def _setup_training_qlearning_elements(self):
        self._setup_training_qlearning_buttons()
        self._setup_training_qlearning_texts()
    def _setup_type_training_buttons(self):
        factory = self.interface.button_factory_f5
        self.buttons['box_type_training'] = factory.create_ComboBox({"text": "Training","position": (5, self.HEIGHT/2-136)})
        self.buttons['box_type_training'].charge_elements({"Genetic":lambda:(self._update_type_training("Genetic"),self._setup_scroll_bar()),"Q-learning":lambda:(self._update_type_training("Q-learning"),self._setup_scroll_bar())})
        self._update_type_training("Genetic")
        self.buttons['box_type_model'] = factory.create_ComboBox({"text": "Model","position": (self.WIDTH/2+120, self.HEIGHT/2+139)})
        self.buttons['box_type_model'].charge_elements({"Pytorch":lambda:self._update_model_ai("Pytorch"), "Tensorflow":lambda:self._update_model_ai("Tensorflow")})
        self._update_model_ai("Pytorch")
        self.buttons['save_model'] = factory.create_TextButton({"text": "OFF","color": self.interface.SKYBLUE,"position": (self.WIDTH-85, self.HEIGHT/2+84),"command1": lambda: self.on_off(self.config.config_AI["genetic"], "model_save"),"command2": self.config.save_config})
        self.interface.save_model_button = self.buttons['save_model']
        self.interface.box_type_training = self.buttons['box_type_training']
        self.interface.box_type_model = self.buttons['box_type_model']
    def _update_type_training(self,button):
        type_training = {"Genetic": self.buttons['box_type_training'].return_buttons("Genetic"),"Q-learning": self.buttons['box_type_training'].return_buttons("Q-learning")}
        for b in self.config.config_AI["type_training"].keys():self.config.config_AI["type_training"][b] = False if b != button else True
        self.check_item(self.config.config_AI["type_training"],self.interface.RED,self.interface.WHITE,"color",**type_training)
        self.config.save_config()
    def _update_model_ai(self,button):
        model_ai = {"Pytorch": self.buttons['box_type_model'].return_buttons("Pytorch"),"Tensorflow": self.buttons['box_type_model'].return_buttons("Tensorflow")}
        for b in self.config.config_AI["type_model"].keys():self.config.config_AI["type_model"][b] = False if b != button else True
        self.check_item(self.config.config_AI["type_model"],self.interface.RED,self.interface.WHITE,"color",**model_ai)
        self.config.save_config()
    def _setup_training_genetic_buttons(self):
        factory = self.interface.button_factory_f5
        self.config_genetic_buttons['increase_generation'] = factory.create_TextButton({"text": ">","position": (self.WIDTH-100, self.HEIGHT/2-55),"command1": lambda: self.increase_decrease_variable(self.config.config_AI["genetic"], 'generation_value'),"command2": self._update_training_genetic_texts})
        self.config_genetic_buttons['decrease_generation'] = factory.create_TextButton({"text": "<","position": (self.WIDTH-178, self.HEIGHT/2-55),"command1": lambda: self.increase_decrease_variable(self.config.config_AI["genetic"], 'generation_value', 1, -1),"command2": self._update_training_genetic_texts})
        self.config_genetic_buttons['increase_population'] = factory.create_TextButton({"text": ">","position": (self.WIDTH-100, self.HEIGHT/2),"command1": lambda: self.increase_decrease_variable(self.config.config_AI["genetic"], 'population_value'),"command2": self._update_training_genetic_texts})
        self.config_genetic_buttons['decrease_population'] = factory.create_TextButton({"text": "<","position": (self.WIDTH-178, self.HEIGHT/2),"command1": lambda: self.increase_decrease_variable(self.config.config_AI["genetic"], 'population_value', 1, -1),"command2": self._update_training_genetic_texts})
        self.config_genetic_buttons['increase_try_for_ai'] = factory.create_TextButton({"text": ">","position": (self.WIDTH-100, self.HEIGHT/2+55),"command1": lambda: self.increase_decrease_variable(self.config.config_AI["genetic"], 'try_for_ai'),"command2": self._update_training_genetic_texts})
        self.config_genetic_buttons['decrease_try_for_ai'] = factory.create_TextButton({"text": "<","position": (self.WIDTH-178, self.HEIGHT/2+55),"command1": lambda: self.increase_decrease_variable(self.config.config_AI["genetic"], 'try_for_ai', 1, -1),"command2": self._update_training_genetic_texts})
        for key, button in self.config_genetic_buttons.items():setattr(self.interface, key, button)
    def _setup_training_genetic_texts(self):
        factory = self.interface.button_factory_f5
        self.training_genetic_elements['text_C'] = factory.create_Text({"text": f"Config Training\n{'AI':^26}","position": (self.WIDTH/2+120, self.HEIGHT/2-136),"detect_mouse": False})
        self.training_genetic_elements['text_G'] = factory.create_Text({"text": f"Generation Size\n{self.config.config_AI["genetic"]['generation_value']:^26}","position": (self.WIDTH/2+120, self.HEIGHT/2-81),"detect_mouse": False})
        self.training_genetic_elements['text_P'] = factory.create_Text({"text": f"Population Size\n{self.config.config_AI["genetic"]['population_value']:^26}","position": (self.WIDTH/2+120, self.HEIGHT/2-26),"detect_mouse": False})
        self.training_genetic_elements['text_A'] = factory.create_Text({"text": f"Attempts By AI\n{self.config.config_AI["genetic"]['try_for_ai']:^{28 if self.config.config_AI["genetic"]['try_for_ai']<10 else 26}}","position": (self.WIDTH/2+120, self.HEIGHT/2+29),"detect_mouse": False})
        self.training_genetic_elements['text_S'] = factory.create_Text({"text": "Save model","position": (self.WIDTH/2+120, self.HEIGHT/2+84),"detect_mouse": False})
        self.interface.text_in_training_ai = list(self.training_genetic_elements.values())
    def _setup_training_qlearning_buttons(self):
        factory = self.interface.button_factory_f5
        self.config_qlearning_buttons["episodes_increase"] = factory.create_TextButton({"text": ">","position": (self.WIDTH-100, self.HEIGHT/2-55),"command1": lambda: self.increase_decrease_variable(self.config.config_AI["q_learning"], 'episodes'),"command2": self._update_training_qlearning_texts})
        self.config_qlearning_buttons["episodes_decrease"] = factory.create_TextButton({"text": "<","position": (self.WIDTH-178, self.HEIGHT/2-55),"command1": lambda: self.increase_decrease_variable(self.config.config_AI["q_learning"], 'episodes', True, -1),"command2": self._update_training_qlearning_texts})
        self.config_qlearning_buttons["learning_rate_increase"] = factory.create_TextButton({"text": ">","position": (self.WIDTH-100, self.HEIGHT/2),"command1": lambda: self.increase_decrease_variable(self.config.config_AI["q_learning"], 'learning_rate', False, 0.001),"command2": self._update_training_qlearning_texts})
        self.config_qlearning_buttons["learning_rate_decrease"] = factory.create_TextButton({"text": "<","position": (self.WIDTH-178, self.HEIGHT/2),"command1": lambda: self.increase_decrease_variable(self.config.config_AI["q_learning"], 'learning_rate', 0.001, -0.001),"command2": self._update_training_qlearning_texts})
        self.config_qlearning_buttons["gamma_increase"] = factory.create_TextButton({"text": ">","position": (self.WIDTH-100, self.HEIGHT/2+55),"command1": lambda: self.increase_decrease_variable(self.config.config_AI["q_learning"], 'gamma', False, 0.01),"command2": self._update_training_qlearning_texts})
        self.config_qlearning_buttons["gamma_decrease"] = factory.create_TextButton({"text": "<","position": (self.WIDTH-178, self.HEIGHT/2+55),"command1": lambda: self.increase_decrease_variable(self.config.config_AI["q_learning"], 'gamma', 0.01, -0.01),"command2": self._update_training_qlearning_texts})
        self.config_qlearning_buttons["epsilon_start_increase"] = factory.create_TextButton({"text": ">","position": (self.WIDTH-100, self.HEIGHT/2+110),"command1": lambda: self.increase_decrease_variable(self.config.config_AI["q_learning"], 'epsilon_start', False, 0.01),"command2": self._update_training_qlearning_texts})
        self.config_qlearning_buttons["epsilon_start_decrease"] = factory.create_TextButton({"text": "<","position": (self.WIDTH-178, self.HEIGHT/2+110),"command1": lambda: self.increase_decrease_variable(self.config.config_AI["q_learning"], 'epsilon_start', 0.01, -0.01),"command2": self._update_training_qlearning_texts})
        self.config_qlearning_buttons["epsilon_end_increase"] = factory.create_TextButton({"text": ">","position": (self.WIDTH-100, self.HEIGHT/2+165),"command1": lambda: self.increase_decrease_variable(self.config.config_AI["q_learning"], 'epsilon_end', False, 0.01),"command2": self._update_training_qlearning_texts})
        self.config_qlearning_buttons["epsilon_end_decrease"] = factory.create_TextButton({"text": "<","position": (self.WIDTH-178, self.HEIGHT/2+165),"command1": lambda: self.increase_decrease_variable(self.config.config_AI["q_learning"], 'epsilon_end', 0.01, -0.01),"command2": self._update_training_qlearning_texts})
        self.config_qlearning_buttons["epsilon_decay_increase"] = factory.create_TextButton({"text": ">","position": (self.WIDTH-100, self.HEIGHT/2+220),"command1": lambda: self.increase_decrease_variable(self.config.config_AI["q_learning"], 'epsilon_decay', False, 0.001),"command2": self._update_training_qlearning_texts})
        self.config_qlearning_buttons["epsilon_decay_decrease"] = factory.create_TextButton({"text": "<","position": (self.WIDTH-178, self.HEIGHT/2+220),"command1": lambda: self.increase_decrease_variable(self.config.config_AI["q_learning"], 'epsilon_decay', 0.001, -0.001),"command2": self._update_training_qlearning_texts})
    def _setup_training_qlearning_texts(self):
        factory = self.interface.button_factory_f5
        self.training_qlearning_elements["text_C"] = factory.create_Text({"text": f"Config Training\n{'AI':^26}","position": (self.WIDTH/2+120, self.HEIGHT/2-136),"detect_mouse": False})
        self.training_qlearning_elements["text_E"] = factory.create_Text({"text": f"Episodes Size\n{self.config.config_AI['q_learning']['episodes']:^26}","position": (self.WIDTH/2+120, self.HEIGHT/2-81),"detect_mouse": False})
        self.training_qlearning_elements["text_LR"] = factory.create_Text({"text": f"Learning Rate\n{self.config.config_AI['q_learning']['learning_rate']:^25.3f}","position": (self.WIDTH/2+120, self.HEIGHT/2-26),"detect_mouse": False})
        self.training_qlearning_elements["text_G"] = factory.create_Text({"text": f"Gamma Size\n{self.config.config_AI['q_learning']['gamma']:^25.2f}","position": (self.WIDTH/2+120, self.HEIGHT/2+29),"detect_mouse": False})
        self.training_qlearning_elements["text_ES"] = factory.create_Text({"text": f"Epsilon Start\n{self.config.config_AI['q_learning']['epsilon_start']:^25.3f}","position": (self.WIDTH/2+120, self.HEIGHT/2+84),"detect_mouse": False})
        self.training_qlearning_elements["text_EE"] = factory.create_Text({"text": f"Epsilon End\n{self.config.config_AI['q_learning']['epsilon_end']:^25.3f}","position": (self.WIDTH/2+120, self.HEIGHT/2+139),"detect_mouse": False})
        self.training_qlearning_elements["text_ED"] = factory.create_Text({"text": f"Epsilon Decay\n{self.config.config_AI['q_learning']['epsilon_decay']:^25.3f}","position": (self.WIDTH/2+120, self.HEIGHT/2+194),"detect_mouse": False})
    def _setup_scroll_bar(self):
        factory = self.interface.button_factory_f5
        self.config_buttons['scroll'] = factory.create_ScrollBar({"position": (self.WIDTH-30, 100, 20, self.HEIGHT-200),"thumb_height": 20})
        buttons_list = list(self.config_genetic_buttons.values() if self.interface.config.config_AI["type_training"]["Genetic"] else self.config_qlearning_buttons.values())
        text_list = list(self.training_genetic_elements.values() if self.interface.config.config_AI["type_training"]["Genetic"] else self.training_qlearning_elements.values())
        self.config_buttons["scroll"].update_elements([*text_list, *buttons_list])
        self.interface.scroll = self.config_buttons['scroll']
    def _setup_config_game_buttons(self):
        factory = self.interface.button_factory_f5
        self.config_buttons['increase_balls'] = factory.create_TextButton({"text": ">","position": (self.WIDTH-100, self.HEIGHT/2-55),"command1": lambda: self.increase_decrease_variable(self.config.config_game, 'number_balls'),"command2": self.interface.objects()})
        self.config_buttons['decrease_balls'] = factory.create_TextButton({"text": "<","position": (self.WIDTH-178, self.HEIGHT/2-55),"command1": lambda: self.increase_decrease_variable(self.config.config_game, 'number_balls', True, -1),"command2": self.interface.objects()})
        self.interface.increase_balls = self.config_buttons['increase_balls']
        self.interface.decrease_balls = self.config_buttons['decrease_balls']
    def _update_training_genetic_texts(self):
        if 'text_G' in self.training_genetic_elements:self.training_genetic_elements['text_G'].change_item({"text": f"Generation Size\n{self.config.config_AI["genetic"]['generation_value']:^26}"})
        if 'text_P' in self.training_genetic_elements:self.training_genetic_elements['text_P'].change_item({"text": f"Population Size\n{self.config.config_AI["genetic"]['population_value']:^26}"})
        if 'text_A' in self.training_genetic_elements:self.training_genetic_elements['text_A'].change_item({"text": f"Attempts By AI\n{self.config.config_AI["genetic"]['try_for_ai']:^{28 if self.config.config_AI["genetic"]['try_for_ai'] < 10 else 26}}"})
    def _update_training_qlearning_texts(self):
        if "text_E" in self.training_qlearning_elements:self.training_qlearning_elements["text_E"].change_item({"text": f"Episodes Size\n{self.config.config_AI['q_learning']['episodes']:^26}"})
        if "text_LR" in self.training_qlearning_elements:self.training_qlearning_elements["text_LR"].change_item({"text": f"Learning Rate\n{self.config.config_AI['q_learning']['learning_rate']:^25.3f}"})
        if "text_G" in self.training_qlearning_elements:self.training_qlearning_elements["text_G"].change_item({"text": f"Gamma Size\n{self.config.config_AI['q_learning']['gamma']:^25.2f}"})
        if "text_ES" in self.training_qlearning_elements:self.training_qlearning_elements["text_ES"].change_item({"text": f"Epsilon Start\n{self.config.config_AI['q_learning']['epsilon_start']:^25.3f}"})
        if "text_EE" in self.training_qlearning_elements:self.training_qlearning_elements["text_EE"].change_item({"text": f"Epsilon End\n{self.config.config_AI['q_learning']['epsilon_end']:^25.3f}"})
        if "text_ED" in self.training_qlearning_elements:self.training_qlearning_elements["text_ED"].change_item({"text": f"Epsilon Decay\n{self.config.config_AI['q_learning']['epsilon_decay']:^25.3f}"})
    def _update_score_button_state(self):
        can_decrease = self.config.config_game["max_score"] > 1
        self.buttons['decrease_score'].change_item({"pressed": can_decrease,"detect_mouse": can_decrease})
    def update_training_ai_save_model(self):
        self.config_genetic_buttons['save_model'].change_item({"color": self.interface.SKYBLUE if self.config.config_AI["genetic"]["model_save"] else self.interface.RED,"text": "ON" if self.config.config_AI["genetic"]["model_save"] else "OFF"})
    def render(self):
        self.screen.fill(self.interface.BLACK)
        font_modegame = pygame.font.Font(os.path.join(self.interface.font_path, "8bitOperatorPlusSC-Bold.ttf"), 22)
        self._render_main_texts(font_modegame)
        if self.interface.mode_game["Training AI"]:
            if self.interface.config.config_AI["type_training"]["Genetic"]:self._render_training_genetic()
            elif self.interface.config.config_AI["type_training"]["Q-learning"]:self._render_training_qlearning()
        elif self.interface.mode_game["Player"] or self.interface.mode_game["AI"]:self._render_game_options()
        self.execute_buttons()
        self._update_score_button_state()
    def _render_main_texts(self, font_modegame):
        self.screen.blit(font_modegame.render("Game Mode", True, "white"), (self.WIDTH/2-70, self.HEIGHT/2-162))
        self.screen.blit(self.interface.font5.render("Enter Player Name One", True, "white"), (7, 10))
        self.screen.blit(self.interface.font5.render("Enter Player Name Two", True, "white"), (416, 10))
        self.screen.blit(font_modegame.render("Max Score", True, "white"), (self.WIDTH/2-68, self.HEIGHT/2-50))
        self.screen.blit(font_modegame.render(f"{self.config.config_game['max_score']}", True, "white"), (self.WIDTH/2-8, self.HEIGHT/2-20))
    def _render_training_genetic(self):
        for text_element in self.training_genetic_elements.values():text_element.draw()
        self.update_training_ai_save_model()
    def _render_training_qlearning(self):
        for text_element in self.training_qlearning_elements.values():text_element.draw()
        self.update_training_ai_save_model()
    def _render_game_options(self):
        self.screen.blit(self.interface.font5.render(f"Configuration of\n{'Gameplay':^23}", True, "White"),(self.WIDTH/2+120, self.HEIGHT/2-136))
        self.screen.blit(self.interface.font5.render(f"Number of Balls\n{self.config.config_game['number_balls']:^{28 if self.config.config_game['number_balls']<10 else 26}}", True, "White"),(self.WIDTH/2+120, self.HEIGHT/2-81))
    def execute_buttons(self):
        common_buttons = [self.buttons['back'], self.buttons['continue'], self.buttons['training_ai'], self.buttons['player'], self.buttons['ai'],self.buttons['decrease_score'], self.buttons['increase_score'],self.inputs['player1'], self.inputs['player2']]
        if self.interface.mode_game["Training AI"]: common_buttons.append(self.buttons['box_type_training'], self.buttons['box_type_model'])
        for button in common_buttons:button.draw()
        if self.interface.mode_game["Training AI"]:
            if self.interface.config.config_AI["type_training"]["Genetic"]:self._execute_training_genetic_buttons()
            elif self.interface.config.config_AI["type_training"]["Q-learning"]:self._execute_training_qlearning_buttons()
            self.config_buttons["scroll"].draw()
        elif self.interface.mode_game["Player"] or self.interface.mode_game["AI"]:self._execute_game_config_buttons()
    def _execute_training_genetic_buttons(self):
        for button in self.config_genetic_buttons.values():button.draw()
    def _execute_training_qlearning_buttons(self):
        for button in self.config_qlearning_buttons.values():button.draw()
    def _execute_game_config_buttons(self):
        config_buttons = [self.config_buttons['increase_balls'],self.config_buttons['decrease_balls']]
        for button in config_buttons:button.draw()