import pygame
class Visuals_items:
    def __init__(self, game):
        self.game = game
        self.assets = game.context.assets
        self.ui = game.ui
    def images_elements(self, screen):
        screen.blit(self.assets.spacecraft, (-77, self.game.game_logic.player_one.rect.y - 140))
        screen.blit(self.assets.spacecraft2, (578, self.game.game_logic.player_two.rect.y - 140))
        for ball in self.game.game_logic.balls:
            self.rotated_ball = pygame.transform.rotate(self.assets.planet, ball.rect.x)
            screen.blit(self.rotated_ball, (ball.rect.x, ball.rect.y))
    def mode_speed(self, screen):
        screen.blit(self.assets.font.render(f"Speed: {self.game.speed}", True, self.assets.YELLOW), (self.game.WIDTH // 2 - 40, 360))
    def name_players(self, screen):
        screen.blit(self.assets.font.render(f"{self.ui.input_player1.show_player()}", True, self.assets.YELLOW), (45, 360))
        screen.blit(self.assets.font.render(f"{self.ui.input_player2.show_player()}", True, self.assets.YELLOW), (580, 360))
    def draw_generation(self, screen):
        if self.game.config.config_AI["type_training"]["Q-learning"]: screen.blit(self.assets.font2.render(f"Episode: {self.game.generation}", True, self.assets.YELLOW), (10, 10))
        else: screen.blit(self.assets.font2.render(f"Generation: {self.game.generation}", True, self.assets.YELLOW), (10, 10))
