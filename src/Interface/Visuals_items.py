import pygame
class Visuals_items:
    def __init__(self, game): self.game = game
    def images_elements(self, screen):
        screen.blit(self.game.spacecraft, (-77,self.game.game_logic.player_one.rect.y-140))
        screen.blit(self.game.spacecraft2, (578,self.game.game_logic.player_two.rect.y-140))
        for ball in self.game.game_logic.balls:
            self.rotated_ball = pygame.transform.rotate(self.game.planet, ball.rect.x)
            screen.blit(self.rotated_ball, (ball.rect.x,ball.rect.y))
    def mode_speed(self, screen): screen.blit(self.game.font.render(f"Speed: {self.game.speed}", True, self.game.YELLOW),(self.game.WIDTH//2-40,360))
    def name_players(self, screen):
        screen.blit(self.game.font.render(f"{self.game.input_player1.show_player()}", True, self.game.YELLOW),(45,360))
        screen.blit(self.game.font.render(f"{self.game.input_player2.show_player()}", True, self.game.YELLOW),(580,360))
    def draw_generation(self, screen):
        if self.game.config.config_AI["type_training"]["Q-learning"]: screen.blit(self.game.font2.render(f"Episode: {self.game.generation}", True, self.game.YELLOW), (10, 10))
        else: screen.blit(self.game.font2.render(f"Generation: {self.game.generation}", True, self.game.YELLOW), (10, 10))
    def scores(self, screen):
        screen.blit(self.game.font.render(f"Score {self.game.game_logic.player_one.score}", True, self.game.YELLOW),(45,380))
        screen.blit(self.game.font.render(f"Score {self.game.game_logic.player_two.score}", True, self.game.YELLOW),(580,380))
    def draw_activations(self, screen):
        if self.game.mode_game["AI"]: self.game.model = self.game.model_training
        if self.game.model!=None and (self.game.model.activations is not None):
            activations = self.game.model.activations
            num_activations = activations.shape[1]
            neuron_positions = [(self.game.WIDTH - 800 + i * 20, self.game.HEIGHT // 2) for i in range(num_activations)]
            for pos in neuron_positions:
                pygame.draw.circle(screen, self.game.WHITE, pos, 5)
                pygame.draw.line(screen, self.game.WHITE, (self.game.WIDTH - 210, self.game.HEIGHT // 2), pos, 1)
                pygame.draw.line(screen, self.game.WHITE, (self.game.WIDTH - 190, self.game.HEIGHT // 2), pos, 1)
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
                    weights_text = self.game.font.render(f"Model Weights: {weights_preview}", True, self.game.YELLOW)
                    screen.blit(weights_text, (10, 50))
            except Exception: pass
            if getattr(self.game.model, 'activations', None) is not None:
                try:
                    activations_text = self.game.font.render(f"Activations: {self.game.model.activations.flatten()[:5]}", True, self.game.YELLOW)
                    screen.blit(activations_text, (10, 70))
                except Exception: pass
    def draw(self):
        screen = self.window.canvas
        screen.blit(self.game.image, (0, 0))
        if self.game.mode_game["Training AI"]: self.draw_generation(screen)
        if self.game.mode_game["Training AI"] or self.game.mode_game["AI"]: self.draw_activations(screen),self.draw_model_data(screen)
        self.images_elements(screen)
        self.scores(screen)
        self.name_players(screen)
        self.mode_speed(screen)
        self.game.menus()