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
        if self.mode_game["AI"]: self.model = self.model_training
        if self.model!=None and (self.model.activations is not None):
            activations = self.model.activations
            num_activations = activations.shape[1]
            neuron_positions = [(self.WIDTH - 800 + i * 20, self.HEIGHT // 2) for i in range(num_activations)]
            for pos in neuron_positions:
                pygame.draw.circle(self.screen, self.WHITE, pos, 5)
            