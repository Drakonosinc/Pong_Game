from .Base_Menu import BaseMenu
from Utils.States import GameState


class VisualsMenu(BaseMenu):
    def __init__(self, interface):
        super().__init__(interface)
        self.buttons = {}

    def setup_buttons(self):
        factory_f5 = self.interface.button_factory_f5
        factory_f2_5 = self.interface.button_factory_f2_5
        self.buttons["back"] = factory_f5.create_PolygonButton({
            "position": ((50, 350), (50, 380), (25, 365)),
            "position2": ((50, 340), (50, 390), (10, 365)),
            "command1": lambda: self.change_mains({"main": GameState.OPTIONS}),
        })
        self.buttons["decrease_width"] = factory_f2_5.create_TextButton({
            "text": "<",
            "position": (self.WIDTH / 2 - 200, self.HEIGHT / 2 - 200),
            "command1": lambda: self._change_items("WIDTH", number=-10),
        })
        self.buttons["increase_width"] = factory_f2_5.create_TextButton({
            "text": ">",
            "position": (self.WIDTH / 2 - 40, self.HEIGHT / 2 - 200),
            "command1": lambda: self._change_items("WIDTH", number=10),
        })
        self.buttons["decrease_height"] = factory_f2_5.create_TextButton({
            "text": "<",
            "position": (self.WIDTH / 2 + 20, self.HEIGHT / 2 - 200),
            "command1": lambda: self._change_items("HEIGHT", number=-10),
        })
        self.buttons["increase_height"] = factory_f2_5.create_TextButton({
            "text": ">",
            "position": (self.WIDTH / 2 + 200, self.HEIGHT / 2 - 200),
            "command1": lambda: self._change_items("HEIGHT", number=10),
        })
        self.buttons["decrease_planet"] = factory_f2_5.create_TextButton({
            "text": "<",
            "position": (self.WIDTH / 2 - 40, self.HEIGHT / 2 - 22),
            "command1": lambda: self._change_items("value_planet", "planets", -1),
        })
        self.buttons["increase_planet"] = factory_f2_5.create_TextButton({
            "text": ">",
            "position": (self.WIDTH / 2 + 20, self.HEIGHT / 2 - 22),
            "command1": lambda: self._change_items("value_planet", "planets", 1),
        })
        self.buttons["decrease_back"] = factory_f2_5.create_TextButton({
            "text": "<",
            "position": (self.WIDTH / 2 - 80, self.HEIGHT / 2 + 160),
            "command1": lambda: self._change_items("value_background", "image_background", -1),
        })
        self.buttons["increase_back"] = factory_f2_5.create_TextButton({
            "text": ">",
            "position": (self.WIDTH / 2 + 65, self.HEIGHT / 2 + 160),
            "command1": lambda: self._change_items("value_background", "image_background", 1),
        })
        self.buttons["decrease_player1"] = factory_f2_5.create_TextButton({
            "font": self.interface.font3_5,
            "text": "Λ",
            "position": (self.WIDTH / 2 - 330, self.HEIGHT / 2 - 120),
            "command1": lambda: self._change_items("value_spacecraft1", "spacecrafts", -1),
        })
        self.buttons["increase_player1"] = factory_f2_5.create_TextButton({
            "font": self.interface.font3_8,
            "text": "v",
            "position": (self.WIDTH / 2 - 330, self.HEIGHT / 2 + 50),
            "command1": lambda: self._change_items("value_spacecraft1", "spacecrafts", 1),
        })
        self.buttons["decrease_player2"] = factory_f2_5.create_TextButton({
            "font": self.interface.font3_5,
            "text": "Λ",
            "position": (self.WIDTH / 2 + 310, self.HEIGHT / 2 - 120),
            "command1": lambda: self._change_items("value_spacecraft2", "spacecrafts", -1),
        })
        self.buttons["increase_player2"] = factory_f2_5.create_TextButton({
            "font": self.interface.font3_8,
            "text": "v",
            "position": (self.WIDTH / 2 + 310, self.HEIGHT / 2 + 50),
            "command1": lambda: self._change_items("value_spacecraft2", "spacecrafts", 1),
        })
        self.buttons["save_visual"] = factory_f5.create_TextButton({
            "text": "Save Config",
            "position": (self.WIDTH / 2 + 200, self.HEIGHT / 2 + 140),
            "command1": self.config.save_config,
        })
        self.buttons["default_visual"] = factory_f5.create_TextButton({
            "text": "Default config",
            "position": (self.WIDTH / 2 + 160, self.HEIGHT / 2 + 160),
            "command1": lambda: self.config.config(visuals=True),
            "command2": self.interface.config_screen,
        })

    def render(self):
        self.screen.blit(self.interface.image, (0, 0))
        if hasattr(self.interface, "visuals_items") and hasattr(self.interface.visuals_items, "starfield"):
            self.interface.visuals_items.starfield.update_and_draw(self.screen, 1.0 / 60.0)
        # Top resolution HUD bar
        self.draw_hud_frame(
            (int(self.WIDTH / 2 - 216), int(self.HEIGHT / 2 - 204), 444, 38),
            accent_color=(56, 189, 248),
            bg_alpha=175,
            corner_size=8,
        )
        # Bottom background selector HUD badge
        self.draw_hud_frame(
            (int(self.WIDTH / 2 - 96), int(self.HEIGHT / 2 + 156), 192, 38),
            accent_color=(168, 85, 247),
            bg_alpha=175,
            corner_size=8,
        )
        # Bottom-right Save/Default HUD card
        self.draw_hud_frame(
            (int(self.WIDTH / 2 + 150), int(self.HEIGHT / 2 + 134), 195, 56),
            accent_color=(56, 189, 248),
            bg_alpha=175,
            corner_size=8,
        )
        self.draw_styled_label(self.interface.font2_5, "WIDTH", (self.WIDTH / 2 - 163, self.HEIGHT / 2 - 200), color=self.interface.SKYBLUE, glow_color=(56, 189, 248))
        self.draw_styled_label(self.interface.font2_5, "HEIGHT", (self.WIDTH / 2 + 60, self.HEIGHT / 2 - 200), color=self.interface.SKYBLUE, glow_color=(56, 189, 248))
        self.draw_styled_label(self.interface.font2_5, "IMAGE", (self.WIDTH / 2 - 52, self.HEIGHT / 2 + 160), color=self.interface.SKYBLUE, glow_color=(168, 85, 247))
        self.interface.visuals_items.images_elements(self.screen)
        self.execute_buttons(*self.buttons.values())
        self.draw_post_overlay()

    def _change_items(self, item, background=None, number=0):
        if background is not None:
            current_value = self.config.config_visuals[item]
            options_length = len(self.config.config_visuals[background])
            self.config.config_visuals[item] = (current_value + number) % options_length
        else:
            self.config.config_visuals[item] = self.config.config_visuals[item] + number
        self.interface.config_screen()
        self.interface.setup_button_factories()
        self.setup_buttons()
