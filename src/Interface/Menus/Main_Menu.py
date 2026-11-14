from .Base_Menu import BaseMenu
from Utils.States import GameState


class MainMenu(BaseMenu):
    def __init__(self, interface):
        super().__init__(interface)
        self.buttons = {}

    def setup_buttons(self):
        factory = self.interface.button_factory_f5
        self.buttons["play"] = factory.create_TextButton({
            "text": "Press To Start",
            "position": (self.WIDTH // 2 - 200, self.HEIGHT // 2 - 80),
            "command1": lambda: self.change_mains({"main": GameState.MODE_SELECT}),
        })
        self.buttons["quit"] = factory.create_TextButton({
            "text": "Press To Exit",
            "position": (self.WIDTH // 2 - 200, self.HEIGHT // 2 - 50),
            "sound_touch": None,
            "command1": self.interface.event_quit,
        })
        self.buttons["options"] = factory.create_TextButton({
            "text": "Options",
            "position": (self.WIDTH - 110, self.HEIGHT - 40),
            "command1": lambda: self.change_mains({"main": GameState.OPTIONS}),
        })
        self.interface.play_button = self.buttons["play"]
        self.interface.quit_button = self.buttons["quit"]
        self.interface.options_button = self.buttons["options"]

    def render(self):
        self.draw_retro_backdrop(show_grid=True, show_particles=True)
        card_w, card_h = 540, 215
        card_x = self.WIDTH // 2 - card_w // 2
        card_y = self.HEIGHT // 2 - 198
        self.draw_hud_frame(
            (card_x, card_y, card_w, card_h),
            accent_color=(56, 189, 248),
            bg_alpha=150,
            corner_size=14,
        )
        self.draw_neon_title(
            self.interface.font4,
            "Space Pong",
            (self.WIDTH // 2 - 245, self.HEIGHT // 2 - 180),
            color=self.interface.WHITE,
            glow_color=(56, 189, 248),
            accent_color=(168, 85, 247),
            underline=True,
        )
        self.execute_buttons(self.buttons["play"], self.buttons["quit"], self.buttons["options"])
        self.draw_post_overlay()
