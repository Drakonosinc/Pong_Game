import pygame
from pyforgeui import RetroVisualFX


class BaseMenu:
    def __init__(self, interface=None):
        self.interface = interface
        if interface:
            self.WIDTH = interface.WIDTH
            self.HEIGHT = interface.HEIGHT
            self.config = interface.config

    @property
    def screen(self):
        return self.interface.screen if self.interface else None

    def execute_buttons(self, *args):
        for button in args:
            button.draw()

    def draw_retro_backdrop(self, show_grid: bool = True, show_particles: bool = True):
        if self.interface and hasattr(self.interface, "backdrop"):
            self.interface.backdrop.draw_background(self.screen, show_grid=show_grid, show_particles=show_particles)
        else:
            self.screen.fill((8, 12, 24))

    def draw_post_overlay(self):
        if self.interface and hasattr(self.interface, "backdrop"):
            self.interface.backdrop.draw_post_overlay(self.screen)

    def draw_hud_frame(
        self,
        rect,
        accent_color=(56, 189, 248),
        bg_alpha: int = 160,
        header_line_y: int | None = None,
        corner_size: int = 10,
    ):
        RetroVisualFX.draw_hud_frame(
            self.screen,
            rect,
            accent_color=accent_color,
            bg_alpha=bg_alpha,
            header_line_y=header_line_y,
            corner_size=corner_size,
        )

    def draw_neon_title(
        self,
        font: pygame.font.Font,
        text: str,
        position: tuple[float, float],
        color=(255, 255, 255),
        glow_color=(56, 189, 248),
        accent_color=(168, 85, 247),
        underline: bool = True,
    ):
        return RetroVisualFX.draw_neon_title(
            self.screen,
            font,
            text,
            position,
            color=color,
            glow_color=glow_color,
            accent_color=accent_color,
            underline=underline,
        )

    def draw_styled_label(
        self,
        font: pygame.font.Font,
        text: str,
        position: tuple[float, float],
        color=(255, 255, 255),
        glow: bool = True,
        glow_color=None,
        highlight_second_line: bool = False,
    ):
        surf, (px, py), _, _ = RetroVisualFX.render_text_styled(
            font,
            str(text),
            color=color,
            shadow=True,
            glow=glow,
            glow_color=glow_color if glow_color is not None else color,
            glow_radius=3,
            highlight_second_line=highlight_second_line,
        )
        self.screen.blit(surf, (int(position[0]) - px, int(position[1]) - py))

    def filt(self, number):
        background = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        background.fill((4, 8, 18, number))
        self.screen.blit(background, (0, 0))

    def fade_transition(self, fade_in, color=(0, 0, 0), limit=255):
        overlay = pygame.Surface((self.WIDTH, self.HEIGHT))
        overlay.fill(color)
        alpha = 0 if not fade_in else 255
        while (not fade_in and alpha <= limit) or (fade_in and alpha >= limit):
            overlay.set_alpha(alpha)
            self.screen.blit(overlay, (0, 0))
            self.interface.window.update_display()
            self.interface.clock.tick(20)
            alpha += -15 if fade_in else 15

    def change_mains(self, config):
        if fade_in := config.get("fade_in", True):
            self.fade_transition(False, config.get("color", (0, 0, 0)), 255)
        if fade_out := config.get("fade_out", False):
            self.fade_transition(True, config.get("color2", (0, 0, 0)), 0)
        self.interface.main = config.get("main", None)
        if config.get("command", None):
            config["command"]()
        if config.get("run", False):
            setattr(self.interface, "running", False)
            setattr(self.interface, "game_over", True)
        if config.get("recursive", False):
            self.change_mains({"main": self.interface.main, "fade_in": fade_in, "fade_out": fade_out})

    def increase_decrease_variable(self, dic=None, variable="", length: int | float = None, number: int | float = 1, save: bool = True):
        if dic is not None and length is not None:
            dic[variable] = max(length, dic[variable] + number)
        elif dic is not None:
            dic[variable] += number
        else:
            setattr(self.interface, variable, getattr(self.interface, variable) + number)
        if save:
            self.config.save_config()

    def on_off(self, dic=None, variable=""):
        if dic:
            dic[variable] = not dic[variable]
        else:
            setattr(self.interface, variable, not getattr(self.interface, variable))

    def check_item(self, dic, is_true, is_false, item, **kwargs):
        for key, button in kwargs.items():
            val = is_true if dic[key] else is_false
            if hasattr(button, "change_item"):
                button.change_item({item: val})
            else:
                setattr(button, item, val)
