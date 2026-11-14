import pygame
from pyforgeui import RetroVisualFX
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

    def _blit_hud_text(self, screen: pygame.Surface, font: pygame.font.Font, text: str, pos: tuple[int, int], color, glow_color=None):
        surf, (px, py), _, _ = RetroVisualFX.render_text_styled(
            font,
            text,
            color=color,
            shadow=True,
            glow=True,
            glow_color=glow_color if glow_color is not None else color,
            glow_radius=3,
        )
        screen.blit(surf, (int(pos[0]) - px, int(pos[1]) - py))

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
            screen.blit(p2_frame, (578 - 6 + ox, dto.p1_y if False else dto.p2_y - 140 - 6 + oy))
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
        self._blit_hud_text(
            screen,
            self.assets.font,
            f"Speed: {self.game.speed}",
            (self.game.WIDTH // 2 - 40, 360),
            self.assets.YELLOW,
            glow_color=(255, 199, 51),
        )

    def name_players(self, screen):
        if hasattr(self.ui, "input_player1") and hasattr(self.ui, "input_player2"):
            self._blit_hud_text(
                screen,
                self.assets.font,
                f"{self.ui.input_player1.show_player()}",
                (45, 360),
                self.assets.YELLOW,
                glow_color=(56, 189, 248),
            )
            self._blit_hud_text(
                screen,
                self.assets.font,
                f"{self.ui.input_player2.show_player()}",
                (580, 360),
                self.assets.YELLOW,
                glow_color=(168, 85, 247),
            )

    def draw_generation(self, screen):
        label = f"Episode: {self.game.generation}" if self.game.config.config_AI["type_training"]["Q-learning"] else f"Generation: {self.game.generation}"
        self._blit_hud_text(screen, self.assets.font2, label, (10, 10), self.assets.YELLOW, glow_color=(56, 189, 248))

    def scores(self, screen):
        self._blit_hud_text(screen, self.assets.font, f"Score {self.p1_score}", (45, 380), self.assets.YELLOW, glow_color=(56, 189, 248))
        self._blit_hud_text(screen, self.assets.font, f"Score {self.p2_score}", (580, 380), self.assets.YELLOW, glow_color=(168, 85, 247))

    def _get_live_model(self):
        if self.game.mode_game.get("AI"):
            self.game.model = self.game.model_training
        elif self.game.mode_game.get("Training AI") and self.game.model is None:
            trainer = getattr(self.game, "qlearning_trainer", None)
            if trainer is not None and hasattr(trainer, "agent") and hasattr(trainer.agent, "policy_net"):
                self.game.model = trainer.agent.policy_net
        model = self.game.model
        if model is not None and hasattr(model, "get_internal_model"):
            return model.get_internal_model()
        return model

    def draw_activations(self, screen):
        raw_model = self._get_live_model()
        layers_sizes = None
        if raw_model is not None:
            in_sz = getattr(raw_model, "input_size", None)
            hid_sz = getattr(raw_model, "hidden_sizes", None)
            out_sz = getattr(raw_model, "output_size", None)
            if in_sz is not None and hid_sz is not None and out_sz is not None:
                layers_sizes = [int(in_sz), *[int(h) for h in hid_sz], int(out_sz)]
            else:
                try:
                    from pyforgeai import infer_architecture
                    _, inf_in, inf_out, inf_hid = infer_architecture(raw_model)
                    layers_sizes = [int(inf_in), *[int(h) for h in inf_hid], int(inf_out)]
                except Exception:
                    layers_sizes = None

        if not layers_sizes:
            nn_cfg = self.game.config.config_AI.get("nn", {"hidden_layers": 2, "neurons_per_layer": 6})
            h_count = max(1, int(nn_cfg.get("hidden_layers", 2)))
            n_count = max(1, int(nn_cfg.get("neurons_per_layer", 6)))
            layers_sizes = [6, *([n_count] * h_count), 2]

        layer_activations = getattr(raw_model, "layer_activations", None) if raw_model is not None else None
        if layer_activations is None and raw_model is not None and getattr(raw_model, "activations", None) is not None:
            try:
                first_hidden = list(raw_model.activations.flatten())
                if self.current_state_dto is not None:
                    arr = self.current_state_dto.to_array()
                    span = float(arr.max() - arr.min())
                    inp_norm = list((arr - arr.min()) / span) if span > 1e-6 else [0.5] * len(arr)
                else:
                    inp_norm = [0.5] * layers_sizes[0]
                layer_activations = [inp_norm, first_hidden]
            except Exception:
                layer_activations = None

        net_rect = (82, 86, self.game.WIDTH - 164, self.game.HEIGHT - 138)
        RetroVisualFX.draw_live_neural_network(
            screen,
            net_rect,
            layers_sizes=layers_sizes,
            layer_activations=layer_activations,
            accent_color=(56, 189, 248),
            secondary_color=(168, 85, 247),
            pulse_color=(255, 199, 51),
            opacity=115,
            show_frame=True,
        )

    def draw_model_data(self, screen):
        raw_model = self._get_live_model()
        if raw_model is not None:
            try:
                weights_preview = None
                if hasattr(raw_model, "fc1"):
                    layer = raw_model.fc1
                    if hasattr(layer, "weight"):
                        weights_preview = layer.weight.detach().cpu().numpy().flatten()[:5]
                    elif hasattr(layer, "kernel"):
                        weights_preview = layer.kernel.numpy().flatten()[:5]
                if weights_preview is not None:
                    self._blit_hud_text(
                        screen,
                        self.assets.font,
                        f"Model Weights: {weights_preview}",
                        (10, 50),
                        self.assets.YELLOW,
                        glow_color=(56, 189, 248),
                    )
            except Exception:
                pass
            if getattr(raw_model, "activations", None) is not None:
                try:
                    self._blit_hud_text(
                        screen,
                        self.assets.font,
                        f"Activations: {raw_model.activations.flatten()[:5]}",
                        (10, 70),
                        self.assets.YELLOW,
                        glow_color=(168, 85, 247),
                    )
                except Exception:
                    pass

    def draw(self):
        dt = 1.0 / max(15.0, float(self.game.FPS))
        ox, oy = self.screen_shake.update(dt)
        screen = self.game.window_manager.canvas
        screen.blit(self.assets.image, (ox, oy))
        self.starfield.update_and_draw(screen, dt)
        if self.game.mode_game["Training AI"] or self.game.mode_game["AI"]:
            self.draw_activations(screen)
        self.images_elements(screen, dt=dt, offset=(ox, oy))
        self.particles.update_and_draw(screen, dt, offset=(ox, oy))
        self.shockwaves.update_and_draw(screen, dt, offset=(ox, oy))
        if self.game.mode_game["Training AI"]:
            self.draw_generation(screen)
        if self.game.mode_game["Training AI"] or self.game.mode_game["AI"]:
            self.draw_model_data(screen)
        self.scores(screen)
        self.name_players(screen)
        self.mode_speed(screen)
