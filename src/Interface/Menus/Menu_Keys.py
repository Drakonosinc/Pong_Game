from pygame.locals import KEYDOWN
from pyforgeui import RetroVisualFX
from .Base_Menu import BaseMenu
from Utils.States import GameState


class KeysMenu(BaseMenu):
    def __init__(self, interface):
        super().__init__(interface)
        self.buttons = {}
        self.key = None
        self.key_name = None
        self.button_key = None

    def setup_buttons(self):
        factory_f5 = self.interface.button_factory_f5
        self.buttons["back"] = factory_f5.create_PolygonButton({
            "position": ((50, 350), (50, 380), (25, 365)),
            "position2": ((50, 340), (50, 390), (10, 365)),
            "command1": lambda: self.change_mains({"main": GameState.OPTIONS}),
        })
        self.buttons["up_w"] = factory_f5.create_TextButton({
            "font": self.interface.font4_5,
            "text": self.config.config_keys["Name_key1"],
            "hover_bg": False,
            "position": (self.WIDTH / 2 - 240, self.HEIGHT / 2 - 170),
            "command1": lambda: self._change_keys("UP_W", "Name_key1", self.buttons["up_w"]),
        })
        self.buttons["down_s"] = factory_f5.create_TextButton({
            "font": self.interface.font4_5,
            "text": self.config.config_keys["Name_key2"],
            "hover_bg": False,
            "position": (self.WIDTH / 2 - 217, self.HEIGHT / 2 - 20),
            "command1": lambda: self._change_keys("DOWN_S", "Name_key2", self.buttons["down_s"]),
        })
        self.buttons["up_arrow"] = factory_f5.create_TextButton({
            "font": self.interface.font4_5,
            "text": self.config.config_keys["Name_key3"],
            "hover_bg": False,
            "position": (self.WIDTH / 2 + 200, self.HEIGHT / 2 - 170),
            "command1": lambda: self._change_keys("UP_ARROW", "Name_key3", self.buttons["up_arrow"]),
        })
        self.buttons["down_arrow"] = factory_f5.create_TextButton({
            "font": self.interface.font4_5,
            "text": self.config.config_keys["Name_key4"],
            "hover_bg": False,
            "position": (self.WIDTH / 2 + 200, self.HEIGHT / 2 - 20),
            "command1": lambda: self._change_keys("DOWN_ARROW", "Name_key4", self.buttons["down_arrow"]),
        })
        self.buttons["save"] = factory_f5.create_TextButton({
            "text": "Save Config",
            "position": (self.WIDTH / 2 + 200, self.HEIGHT / 2 + 140),
            "command1": self.config.save_config,
        })
        self.buttons["default"] = factory_f5.create_TextButton({
            "text": "Default config",
            "position": (self.WIDTH / 2 + 160, self.HEIGHT / 2 + 160),
            "command1": lambda: (
                self.config.config(keys=True),
                self.change_mains({"main": GameState.KEYS, "command": self.setup_buttons}),
            ),
        })

    def render(self):
        self.draw_retro_backdrop(show_grid=True, show_particles=True)
        # Player 1 & Player 2 keycap HUD cards
        self.draw_hud_frame(
            (int(self.WIDTH / 2 - 295), int(self.HEIGHT / 2 - 190), 170, 275),
            accent_color=(56, 189, 248),
            bg_alpha=145,
            corner_size=12,
        )
        self.draw_hud_frame(
            (int(self.WIDTH / 2 + 135), int(self.HEIGHT / 2 - 190), 170, 275),
            accent_color=(168, 85, 247),
            bg_alpha=145,
            corner_size=12,
        )
        key_map = (
            ("UP_W", self.buttons["up_w"]),
            ("DOWN_S", self.buttons["down_s"]),
            ("UP_ARROW", self.buttons["up_arrow"]),
            ("DOWN_ARROW", self.buttons["down_arrow"]),
        )
        for k_id, btn in key_map:
            is_rebinding = bool(self.interface.utils_keys.get(k_id, False))
            is_hovered = bool(btn.states.get("is_hovered", False))
            RetroVisualFX.draw_keycap(
                self.screen,
                btn.get_visual_rect() if hasattr(btn, "get_visual_rect") else btn.rect,
                is_rebinding=is_rebinding,
                is_hovered=is_hovered,
                accent_color=(56, 189, 248),
                hover_color=(255, 199, 51),
            )
        self.execute_buttons(*self.buttons.values())
        self.draw_post_overlay()

    def _change_keys(self, key, key_name, button=None):
        self.key = key
        self.key_name = key_name
        self.button_key = button
        for k in self.interface.utils_keys.keys():
            self.interface.utils_keys[k] = False if k != self.key else not self.interface.utils_keys[self.key]
        self.check_item(
            self.interface.utils_keys,
            self.interface.SKYBLUE,
            self.interface.WHITE,
            "color",
            UP_W=self.buttons["up_w"],
            DOWN_S=self.buttons["down_s"],
            UP_ARROW=self.buttons["up_arrow"],
            DOWN_ARROW=self.buttons["down_arrow"],
        )

    def event_keys(self, event):
        if self.key is not None and self.interface.utils_keys[self.key] and event.type == KEYDOWN:
            self.config.config_keys[self.key] = event.key
            self.config.config_keys[self.key_name] = event.unicode.upper()
            self.check_item(
                self.config.config_keys,
                self.config.config_keys[self.key_name],
                self.interface.WHITE,
                "text",
                **{self.key: self.button_key},
            )
            self._change_keys(self.key, self.key_name)
