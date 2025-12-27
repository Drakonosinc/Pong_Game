import pygame
class Visuals_items:
    def __init__(self, game): self.game = game
    def mode_speed(self): self.game.screen.blit(self.game.font.render(f"Speed: {self.game.speed}", True, self.game.YELLOW),(self.game.WIDTH//2-40,360))
    def name_players(self):
        self.game.screen.blit(self.game.font.render(f"{self.game.input_player1.show_player()}", True, self.game.YELLOW),(45,360))
        self.game.screen.blit(self.game.font.render(f"{self.game.input_player2.show_player()}", True, self.game.YELLOW),(580,360))
    def draw_generation(self):
        if self.game.config.config_AI["type_training"]["Q-learning"]: self.game.screen.blit(self.game.font2.render(f"Episode: {self.game.generation}", True, self.game.YELLOW), (10, 10))
        else: self.game.screen.blit(self.game.font2.render(f"Generation: {self.game.generation}", True, self.game.YELLOW), (10, 10))
    def scores(self):
        self.game.screen.blit(self.game.font.render(f"Score {self.game.player_one.score}", True, self.game.YELLOW),(45,380))
        self.game.screen.blit(self.game.font.render(f"Score {self.game.player_two.score}", True, self.game.YELLOW),(580,380))
    def draw_activations(self):
        if self.game.mode_game["AI"]: self.game.model = self.game.model_training
        if self.game.model!=None and (self.game.model.activations is not None):
            activations = self.game.model.activations
            num_activations = activations.shape[1]
            neuron_positions = [(self.game.WIDTH - 800 + i * 20, self.game.HEIGHT // 2) for i in range(num_activations)]
            for pos in neuron_positions:
                pygame.draw.circle(self.game.screen, self.game.WHITE, pos, 5)
                pygame.draw.line(self.game.screen, self.game.WHITE, (self.game.WIDTH - 210, self.game.HEIGHT // 2), pos, 1)
                pygame.draw.line(self.game.screen, self.game.WHITE, (self.game.WIDTH - 190, self.game.HEIGHT // 2), pos, 1)
            for i in range(num_activations):
                activation_value = activations[0][i]
                activation_value = max(0, min(activation_value, 1))
                color_intensity = int(activation_value * 255)
                color = (color_intensity, color_intensity, color_intensity)
                pygame.draw.circle(self.game.screen, color, neuron_positions[i], 5)
    def draw_model_data(self):
        if self.mode_game["AI"]: self.model = self.model_training
        if self.model is not None:
            try:
                weights_preview = None
                if hasattr(self.model, 'fc1'):
                    l = self.model.fc1
                    if hasattr(l, 'weight'): weights_preview = l.weight.detach().cpu().numpy().flatten()[:5]
                    elif hasattr(l, 'kernel'): weights_preview = l.kernel.numpy().flatten()[:5]
                if weights_preview is not None:
                    weights_text = self.font.render(f"Model Weights: {weights_preview}", True, self.YELLOW)
                    self.screen.blit(weights_text, (10, 50))
            except Exception: pass
            if getattr(self.model, 'activations', None) is not None:
