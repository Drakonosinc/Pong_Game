from .Base_Menu import BaseMenu
from Utils.States import GameState


class Pause(BaseMenu):
    def __init__(self, interface):
        super().__init__(interface)
        self.buttons = {}

    def setup_buttons(self):
        factory = self.interface.button_factory_f2_5
        self.buttons["exit"] = factory.create_TextButton({
            "text": "Exit",
            "color": self.interface.WHITE,
            "position": (self.WIDTH / 2 - 40, self.HEIGHT / 2 - 15),
            "color2": self.interface.SKYBLUE,
            "sound_touch": None,
            "command1": self.interface.event_quit,
        })
        self.buttons["reset"] = factory.create_TextButton({
            "text": "Reset",
            "color": self.interface.WHITE,
            "position": (self.WIDTH / 2 - 55, self.HEIGHT / 2 - 85),
            "color2": self.interface.SKYBLUE,
            "command1": lambda: self.change_mains({"main": GameState.PLAYING}),
            "command2": self.interface.reset,
        })
        self.buttons["menu"] = factory.create_TextButton({
            "text": "Menu",
            "color": self.interface.WHITE,
            "position": (self.WIDTH / 2 - 45, self.HEIGHT / 2 - 50),
            "color2": self.interface.SKYBLUE,
            "command1": lambda: self.change_mains({"main": GameState.MENU, "run": True}),
            "command2": self.interface.reset,
        })
        self.interface.exit_button = self.buttons["exit"]
        self.interface.reset_pause_button = self.buttons["reset"]
        self.interface.go_main_button = self.buttons["menu"]

    def execute_buttons(self):
        for button in self.buttons.values():
            button.draw()

    def render(self):
        self.filt(175)
        self.draw_hud_frame(
            (int(self.WIDTH / 2 - 145), int(self.HEIGHT / 2 - 165), 290, 195),
            accent_color=(56, 189, 248),
            bg_alpha=205,
            corner_size=14,
        )
        self.draw_neon_title(
            self.interface.font3,
            "Pause",
            (self.WIDTH / 2 - 105, self.HEIGHT / 2 - 150),
            color=self.interface.WHITE,
            glow_color=(56, 189, 248),
            accent_color=(168, 85, 247),
            underline=False,
        )
        self.execute_buttons()
        self.draw_post_overlay()
