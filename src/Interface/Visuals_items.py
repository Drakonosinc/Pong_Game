import pygame
from pyforgefx import (
    ParticleEmitter,
    ScreenShake,
    ShockwaveManager,
    StarfieldParallax,
    TrailRenderer,
)
from src.Events.GameEvents import (
    BallBounceEvent,
    GameStateChangedEvent,
    GoalScoredEvent,
)


class Visuals_items:
    def __init__(self, game):
        self.game = game
        self.assets = game.context.assets
        self.ui = game.ui
        self.current_state_dto = None
        self.p1_score = 0
        self.p2_score = 0
        self._last_p1_y = None
        self._last_p2_y = None

        # PyForgeFX visual engines
        self.starfield = StarfieldParallax(self.game.WIDTH, self.game.HEIGHT, num_stars=55)
        self.particles = ParticleEmitter(max_particles=400)
        self.shockwaves = ShockwaveManager()
        self.ball_trail = TrailRenderer(
            max_points=14,
            start_radius=11.0,
            color=(56, 189, 248),
            tail_color=(168, 85, 247),
        )
        self.screen_shake = ScreenShake()

        self.game.event_manager.subscribe(GameStateChangedEvent, self.handle_state_changed)
        self.game.event_manager.subscribe(BallBounceEvent, self.handle_ball_bounce)
        self.game.event_manager.subscribe(GoalScoredEvent, self.handle_goal_scored)

    def handle_state_changed(self, event: GameStateChangedEvent):
        self.current_state_dto = event.state_dto
        self.p1_score = event.p1_score
        self.p2_score = event.p2_score

    def handle_ball_bounce(self, event: BallBounceEvent):
        if self.game.mode_game.get("Training AI") and self.game.speed >= 100:
            return
        self.particles.emit_preset(event.x, event.y, "sparks")
        ring_color = (56, 189, 248) if event.player_index == 1 else (249, 115, 22)
        self.shockwaves.spawn(event.x, event.y, max_radius=55.0, speed=250.0, color=ring_color)
        self.screen_shake.trigger(intensity=5.0, duration=0.15)
        if event.player_index == 1 and hasattr(self.assets, "p1_animator"):
            self.assets.p1_animator.play("hit", force_restart=True)
        elif event.player_index == 2 and hasattr(self.assets, "p2_animator"):
            self.assets.p2_animator.play("hit", force_restart=True)

    def handle_goal_scored(self, event: GoalScoredEvent):
        if self.game.mode_game.get("Training AI") and self.game.speed >= 100:
            return
        self.particles.emit_preset(event.x, event.y, "goal")
        self.shockwaves.spawn(event.x, event.y, max_radius=95.0, speed=280.0, color=(255, 199, 51), width=4)
        self.screen_shake.trigger(intensity=8.5, duration=0.25)
        self.ball_trail.clear()

    def _update_ship_state(self, animator, current_y: float, last_y: float | None, ship_x: float) -> None:
        if animator is None:
            return
        moving = last_y is not None and abs(current_y - last_y) > 0.5
        if animator.current_state != "hit":
            animator.play("thrust" if moving else "idle")
        if moving:
            self.particles.emit_preset(ship_x, current_y + 45, "thruster")

    def images_elements(self, screen, dt: float = 1.0 / 60.0, offset: tuple[int, int] = (0, 0)):
        if not self.current_state_dto:
            return
        ox, oy = offset
        dto = self.current_state_dto

        # Update & draw motion trail behind the ball
        self.ball_trail.push(dto.ball_x + 20, dto.ball_y + 20)
        self.ball_trail.draw(screen, offset=offset)

        # Update & draw animated spacecraft 1 & 2 via PyForgeFX Animator
        if hasattr(self.assets, "p1_animator") and hasattr(self.assets, "p2_animator"):
            self._update_ship_state(self.assets.p1_animator, dto.p1_y, self._last_p1_y, 28)
            self._update_ship_state(self.assets.p2_animator, dto.p2_y, self._last_p2_y, 670)
            self._last_p1_y = dto.p1_y
            self._last_p2_y = dto.p2_y

            p1_frame = self.assets.p1_animator.update(dt)
            p2_frame = self.assets.p2_animator.update(dt)
            screen.blit(p1_frame, (-77 - 6 + ox, dto.p1_y - 140 - 6 + oy))
            screen.blit(p2_frame, (578 - 6 + ox, dto.p2_y - 140 - 6 + oy))
        else:
            screen.blit(self.assets.spacecraft, (-77 + ox, dto.p1_y - 140 + oy))
            screen.blit(self.assets.spacecraft2, (578 + ox, dto.p2_y - 140 + oy))

        if hasattr(self.assets, "planet_animator"):
            ball_frame = self.assets.planet_animator.update(dt)
            screen.blit(ball_frame, (dto.ball_x + ox, dto.ball_y + oy))
        else:
            self.rotated_ball = pygame.transform.rotate(self.assets.planet, dto.ball_x)
            screen.blit(self.rotated_ball, (dto.ball_x + ox, dto.ball_y + oy))

    def mode_speed(self, screen):
        screen.blit(
            self.assets.font.render(f"Speed: {self.game.speed}", True, self.assets.YELLOW),
            (self.game.WIDTH // 2 - 40, 360),
        )

    def name_players(self, screen):
        if hasattr(self.ui, "input_player1") and hasattr(self.ui, "input_player2"):
            screen.blit(
                self.assets.font.render(f"{self.ui.input_player1.show_player()}", True, self.assets.YELLOW),
                (45, 360),
            )
            screen.blit(
                self.assets.font.render(f"{self.ui.input_player2.show_player()}", True, self.assets.YELLOW),
                (580, 360),
            )

    def draw_generation(self, screen):
        if self.game.config.config_AI["type_training"]["Q-learning"]:
            screen.blit(
                self.assets.font2.render(f"Episode: {self.game.generation}", True, self.assets.YELLOW),
                (10, 10),
            )
        else:
            screen.blit(
                self.assets.font2.render(f"Generation: {self.game.generation}", True, self.assets.YELLOW),
                (10, 10),
            )

    def scores(self, screen):
        screen.blit(self.assets.font.render(f"Score {self.p1_score}", True, self.assets.YELLOW), (45, 380))
        screen.blit(self.assets.font.render(f"Score {self.p2_score}", True, self.assets.YELLOW), (580, 380))

    def draw_activations(self, screen):
        if self.game.mode_game["AI"]:
            self.game.model = self.game.model_training
        if self.game.model is not None and (getattr(self.game.model, "activations", None) is not None):
            activations = self.game.model.activations
            num_activations = activations.shape[1]
            neuron_positions = [
                (self.game.WIDTH - 800 + i * 20, self.game.HEIGHT // 2) for i in range(num_activations)
            ]
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
        if self.game.mode_game["AI"]:
            self.game.model = self.game.model_training
        if self.game.model is not None:
            try:
                weights_preview = None
                if hasattr(self.game.model, "fc1"):
                    layer = self.game.model.fc1
                    if hasattr(layer, "weight"):
                        weights_preview = layer.weight.detach().cpu().numpy().flatten()[:5]
                    elif hasattr(layer, "kernel"):
                        weights_preview = layer.kernel.numpy().flatten()[:5]
                if weights_preview is not None:
                    weights_text = self.assets.font.render(
                        f"Model Weights: {weights_preview}", True, self.assets.YELLOW
                    )
                    screen.blit(weights_text, (10, 50))
            except Exception:
                pass
            if getattr(self.game.model, "activations", None) is not None:
                try:
                    activations_text = self.assets.font.render(
                        f"Activations: {self.game.model.activations.flatten()[:5]}", True, self.assets.YELLOW
                    )
                    screen.blit(activations_text, (10, 70))
                except Exception:
                    pass

    def draw(self):
        dt = 1.0 / max(15.0, float(self.game.FPS))
        ox, oy = self.screen_shake.update(dt)
        screen = self.game.window_manager.canvas
        screen.blit(self.assets.image, (ox, oy))
        self.starfield.update_and_draw(screen, dt)
        if self.game.mode_game["Training AI"]:
            self.draw_generation(screen)
        if self.game.mode_game["Training AI"] or self.game.mode_game["AI"]:
            self.draw_activations(screen)
            self.draw_model_data(screen)
        self.images_elements(screen, dt=dt, offset=(ox, oy))
        self.particles.update_and_draw(screen, dt, offset=(ox, oy))
        self.shockwaves.update_and_draw(screen, dt, offset=(ox, oy))
        self.scores(screen)
        self.name_players(screen)
        self.mode_speed(screen)
