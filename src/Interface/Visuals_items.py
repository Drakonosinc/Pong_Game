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
