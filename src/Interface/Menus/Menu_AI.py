import pygame
from pyforgeui import RetroVisualFX
from .Base_Menu import BaseMenu
from Utils.States import GameState


class AIMenu(BaseMenu):
    def __init__(self, interface):
        super().__init__(interface)
        self.buttons = {}
        self.network_buttons = []
        self.connections = []
        nn_cfg = self.interface.config.config_AI.setdefault("nn", {"hidden_layers": 2, "neurons_per_layer": 6})
        nn_cfg["hidden_layers"] = max(1, int(nn_cfg.get("hidden_layers", 2)))
        nn_cfg["neurons_per_layer"] = max(1, int(nn_cfg.get("neurons_per_layer", 6)))
        self.input_size = 6
        self.output_size = 2

    def setup_buttons(self):
        factory = self.interface.button_factory_f2_5
        self.buttons["back"] = factory.create_PolygonButton({
            "position": ((50, 350), (50, 380), (25, 365)),
            "position2": ((50, 340), (50, 390), (10, 365)),
            "command1": lambda: self.change_mains({"main": GameState.MODE_SELECT}),
        })
        self.buttons["dec_layers"] = factory.create_TextButton({
            "text": "-",
            "position": (self.WIDTH // 2 - 130, 60),
            "command1": lambda: self._change_layers(-1),
        })
        self.buttons["inc_layers"] = factory.create_TextButton({
            "text": "+",
            "position": (self.WIDTH // 2 - 100, 60),
            "command1": lambda: self._change_layers(1),
        })
        self.buttons["dec_neurons"] = factory.create_TextButton({
            "text": "-",
            "position": (self.WIDTH // 2 + 100, 60),
            "command1": lambda: self._change_neurons(-1),
        })
        self.buttons["inc_neurons"] = factory.create_TextButton({
            "text": "+",
            "position": (self.WIDTH // 2 + 130, 60),
            "command1": lambda: self._change_neurons(1),
        })
        self._rebuild_network_visual()

    def _architecture(self):
        cfg = self.interface.config.config_AI["nn"]
        return [cfg["neurons_per_layer"]] * cfg["hidden_layers"]

    def _change_layers(self, delta: int):
        cfg = self.interface.config.config_AI["nn"]
        cfg["hidden_layers"] = max(1, cfg["hidden_layers"] + delta)
        self.interface.config.save_config()
        self._rebuild_network_visual()

    def _change_neurons(self, delta: int):
        cfg = self.interface.config.config_AI["nn"]
        cfg["neurons_per_layer"] = max(1, cfg["neurons_per_layer"] + delta)
        self.interface.config.save_config()
        self._rebuild_network_visual()

    def _make_neuron_button(self, x: int, y: int):
        size = 10
        rect_points = ((x - size, y - size), (x + size, y - size), (x + size, y + size), (x - size, y + size))
        return self.interface.button_factory_f5.create_PolygonButton({"position": rect_points, "pressed": False})

    def _rebuild_network_visual(self):
        self.network_buttons.clear()
        self.connections.clear()
        left, right = 80, self.WIDTH - 80
        top, bottom = 110, self.HEIGHT - 60
        arch = self._architecture()
        layers_sizes = [self.input_size, *arch, self.output_size]
        num_layers = len(layers_sizes)
        x_positions = [int(left + i * (right - left) / (num_layers - 1)) for i in range(num_layers)]
        layer_centers = []
        for layer_idx, n_neurons in enumerate(layers_sizes):
            if n_neurons <= 0:
                n_neurons = 1
            y_gap = (bottom - top) / (n_neurons + 1)
            centers = [(x_positions[layer_idx], int(top + (i + 1) * y_gap)) for i in range(int(n_neurons))]
            layer_centers.append(centers)
            self.network_buttons.append([self._make_neuron_button(x, y) for x, y in centers])
        for li in range(num_layers - 1):
            for (x1, y1) in layer_centers[li]:
                for (x2, y2) in layer_centers[li + 1]:
                    self.connections.append(((x1, y1), (x2, y2)))

    def _draw_network(self):
        RetroVisualFX.draw_synapse_network(
            self.screen,
            self.connections,
            self.network_buttons,
            accent_color=(56, 189, 248),
            secondary_color=(168, 85, 247),
            pulse_color=(255, 199, 51),
        )

    def render(self):
        self.draw_retro_backdrop(show_grid=True, show_particles=True)
        # Top control bar HUD frame
        self.draw_hud_frame(
            (int(self.WIDTH // 2 - 190), 28, 430, 64),
            accent_color=(56, 189, 248),
            bg_alpha=155,
            corner_size=10,
        )
        # Neural network viewport HUD frame
        self.draw_hud_frame(
            (55, 100, self.WIDTH - 110, self.HEIGHT - 155),
            accent_color=(168, 85, 247),
            bg_alpha=125,
            corner_size=14,
        )
        self.draw_styled_label(self.interface.font5, "AI parameters", (10, 10), color=self.interface.WHITE, glow_color=(56, 189, 248))
        self.draw_styled_label(self.interface.font5, "Layers", (self.WIDTH // 2 - 170, 35), color=self.interface.SKYBLUE, glow_color=(56, 189, 248))
        self.draw_styled_label(self.interface.font5, "Neurons/layer", (self.WIDTH // 2 + 30, 35), color=self.interface.SKYBLUE, glow_color=(56, 189, 248))
        cfg = self.interface.config.config_AI["nn"]
        self.draw_styled_label(self.interface.font5, str(cfg["hidden_layers"]), (self.WIDTH // 2 - 115, 62), color=(255, 199, 51), glow_color=(255, 199, 51))
        self.draw_styled_label(self.interface.font5, str(cfg["neurons_per_layer"]), (self.WIDTH // 2 + 116, 62), color=(255, 199, 51), glow_color=(255, 199, 51))
        self._draw_network()
        for key in ["back", "dec_layers", "inc_layers", "dec_neurons", "inc_neurons"]:
            self.buttons[key].draw()
        self.draw_post_overlay()
