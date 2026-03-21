import pygame
from src.Events.GameEvents import GameStateChangedEvent
class Visuals_items:
    def __init__(self, game):
        self.game = game
        self.assets = game.context.assets
        self.ui = game.ui 
        self.current_state_dto = None
        self.p1_score = 0
        self.p2_score = 0
        self.game.event_manager.subscribe(GameStateChangedEvent, self.handle_state_changed)
    def handle_state_changed(self, event: GameStateChangedEvent):
        self.current_state_dto = event.state_dto
        self.p1_score = event.p1_score
        self.p2_score = event.p2_score
    def images_elements(self, screen):
        if not self.current_state_dto: return 
        screen.blit(self.assets.spacecraft, (-77, self.current_state_dto.p1_y - 140))
        screen.blit(self.assets.spacecraft2, (578, self.current_state_dto.p2_y - 140))
        self.rotated_ball = pygame.transform.rotate(self.assets.planet, self.current_state_dto.ball_x)
        screen.blit(self.rotated_ball, (self.current_state_dto.ball_x, self.current_state_dto.ball_y))
    def mode_speed(self, screen):
        screen.blit(self.assets.font.render(f"Speed: {self.game.speed}", True, self.assets.YELLOW), (self.game.WIDTH // 2 - 40, 360))
    def name_players(self, screen):
        if hasattr(self.ui, 'input_player1') and hasattr(self.ui, 'input_player2'):
            screen.blit(self.assets.font.render(f"{self.ui.input_player1.show_player()}", True, self.assets.YELLOW), (45, 360))
            screen.blit(self.assets.font.render(f"{self.ui.input_player2.show_player()}", True, self.assets.YELLOW), (580, 360))
    def draw_generation(self, screen):
        if self.game.config.config_AI["type_training"]["Q-learning"]: screen.blit(self.assets.font2.render(f"Episode: {self.game.generation}", True, self.assets.YELLOW), (10, 10))
        else: screen.blit(self.assets.font2.render(f"Generation: {self.game.generation}", True, self.assets.YELLOW), (10, 10))
    def scores(self, screen):
        screen.blit(self.assets.font.render(f"Score {self.p1_score}", True, self.assets.YELLOW), (45, 380))
        screen.blit(self.assets.font.render(f"Score {self.p2_score}", True, self.assets.YELLOW), (580, 380))
    def draw_activations(self, screen):
        if self.game.mode_game["AI"]: self.game.model = self.game.model_training
        if self.game.model != None and (getattr(self.game.model, 'activations', None) is not None):
            activations = self.game.model.activations
            num_activations = activations.shape[1]
            neuron_positions = [(self.game.WIDTH - 800 + i * 20, self.game.HEIGHT // 2) for i in range(num_activations)]
            for pos in neuron_positions:
                pygame.draw.circle(screen, self.assets.WHITE, pos, 5)
                pygame.draw.line(screen, self.assets.WHITE, (self.game.WIDTH - 210, self.game.HEIGHT // 2), pos, 1)
                pygame.draw.line(screen, self.assets.WHITE, (self.game.WIDTH - 190, self.game.HEIGHT // 2), pos, 1)
            for i in range(num_activations):
                activation_value = activations[0][i]
                activation_value = max(0, min(activation_value, 1))
                color_intensity = int(activation_value * 255)
                color = (color_intensity, color_intensity, color_intensity)
                pygame.draw.circle(screen, color, neuron_positions[i], 5)
    def draw_model_data(self, screen):
        if self.game.mode_game["AI"]: self.game.model = self.game.model_training
        if self.game.model is not None:
            try:
                weights_preview = None
                if hasattr(self.game.model, 'fc1'):
                    l = self.game.model.fc1
                    if hasattr(l, 'weight'): weights_preview = l.weight.detach().cpu().numpy().flatten()[:5]
                    elif hasattr(l, 'kernel'): weights_preview = l.kernel.numpy().flatten()[:5]
                if weights_preview is not None:
                    weights_text = self.assets.font.render(f"Model Weights: {weights_preview}", True, self.assets.YELLOW)
                    screen.blit(weights_text, (10, 50))
            except Exception: pass
            if getattr(self.game.model, 'activations', None) is not None:
                try:
