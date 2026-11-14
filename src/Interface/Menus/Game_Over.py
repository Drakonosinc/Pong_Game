from .Base_Menu import BaseMenu
from Utils.States import GameState


class GameOver(BaseMenu):
    def __init__(self, interface):
        super().__init__(interface)
        self.buttons = {}

    def setup_buttons(self):
        factory = self.interface.button_factory_f2_5
        self.buttons["main"] = factory.create_TextButton({
            "text": "Main Menu Press E",
            "color": self.interface.WHITE,
            "position": (self.WIDTH / 2 - 166, self.HEIGHT / 2 - 110),
            "command1": lambda: self.change_mains({"main": GameState.MENU, "run": True}),
        })
        self.buttons["reset"] = factory.create_TextButton({
            "text": "Reset Press R",
            "color": self.interface.WHITE,
            "position": (self.WIDTH / 2 - 130, self.HEIGHT / 2 - 80),
            "command1": self.interface.reset,
            "command2": lambda: self.change_mains({"main": GameState.PLAYING}),
        })
        self.interface.main_button = self.buttons["main"]
        self.interface.reset_button = self.buttons["reset"]

    def render(self):
        self.filt(145)
        self.draw_hud_frame(
            (int(self.WIDTH / 2 - 210), int(self.HEIGHT / 2 - 195), 420, 165),
            accent_color=(244, 63, 94),
            bg_alpha=210,
            corner_size=14,
        )
        self.draw_neon_title(
            self.interface.font3,
            "GAME OVER",
            (self.WIDTH / 2 - 178, self.HEIGHT / 2 - 180),
            color=(255, 245, 248),
            glow_color=(244, 63, 94),
            accent_color=(255, 199, 51),
            underline=False,
        )
        self.execute_buttons(self.buttons["main"], self.buttons["reset"])
        self.draw_post_overlay()
