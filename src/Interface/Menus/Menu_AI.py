import pygame
from .Base_Menu import BaseMenu
class AIMenu(BaseMenu):
    def __init__(self, interface):
        super().__init__(interface)
        self.buttons = {}
        self.network_buttons = []  # list[list[button]] by layer (including input/output)
        self.connections = []      # list[tuple[(x1,y1),(x2,y2)]]
        # Defaults if missing in config
        nn_cfg = self.interface.config.config_AI.setdefault("nn", {"hidden_layers": 2, "neurons_per_layer": 6})
        nn_cfg["hidden_layers"] = max(1, int(nn_cfg.get("hidden_layers", 2)))
        nn_cfg["neurons_per_layer"] = max(1, int(nn_cfg.get("neurons_per_layer", 6)))
        # Fixed IO sizes used by the current game
        self.input_size = 6
        self.output_size = 2
    def setup_buttons(self):
        f_big = self.interface.button_factory_f5
        f_med = self.interface.button_factory_f2_5
        # Navigation
        self.buttons['back'] = f_med.create_PolygonButton({"position": ((50, 350), (50, 380), (25, 365)),"position2": ((50, 340), (50, 390), (10, 365)),"command1": lambda: self.change_mains({"main": 2})})
        # Controls (+/- layers, +/- neurons)
        self.buttons['dec_layers'] = f_med.create_TextButton({"text": "-","position": (self.WIDTH//2-130, 60),"command1": lambda: self._change_layers(-1)})
        self.buttons['inc_layers'] = f_med.create_TextButton({"text": "+","position": (self.WIDTH//2-100, 60),"command1": lambda: self._change_layers(1)})
        self.buttons['dec_neurons'] = f_med.create_TextButton({"text": "-","position": (self.WIDTH//2+100, 60),"command1": lambda: self._change_neurons(-1)})
        self.buttons['inc_neurons'] = f_med.create_TextButton({"text": "+","position": (self.WIDTH//2+130, 60),"command1": lambda: self._change_neurons(1)})
        # Build first visual network
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
        # Small square button representing a neuron (non-interactive)
        size = 10
        rect_points = ((x - size, y - size), (x + size, y - size), (x + size, y + size), (x - size, y + size))
        return self.interface.button_factory_f5.create_PolygonButton({"position": rect_points, "detect_mouse": False, "pressed": False})
    def _rebuild_network_visual(self):
        self.network_buttons.clear()
        self.connections.clear()
        # Layout area
        left, right = 80, self.WIDTH - 80
        top, bottom = 110, self.HEIGHT - 60
        arch = self._architecture()
        layers_sizes = [self.input_size, *arch, self.output_size]
        num_layers = len(layers_sizes)
        # Compute x positions for each layer
        x_positions = [int(left + i * (right - left) / (num_layers - 1)) for i in range(num_layers)]
        # Build neuron buttons per layer and store their centers
        layer_centers = []
        for layer_idx, n_neurons in enumerate(layers_sizes):
            if n_neurons <= 0: n_neurons = 1
            y_gap = (bottom - top) / (n_neurons + 1)
            centers = [(x_positions[layer_idx], int(top + (i + 1) * y_gap)) for i in range(int(n_neurons))]
            layer_centers.append(centers)
            self.network_buttons.append([self._make_neuron_button(x, y) for x, y in centers])
        # Connections
        for li in range(num_layers - 1):
            for (x1, y1) in layer_centers[li]:
                for (x2, y2) in layer_centers[li + 1]: self.connections.append(((x1, y1), (x2, y2)))
    def _draw_network(self):
        # Draw connections first
        for (p1, p2) in self.connections: pygame.draw.line(self.screen, self.interface.SKYBLUE, p1, p2, 1)
        # Draw neuron buttons
        for layer in self.network_buttons:
            for btn in layer: btn.draw()
    def render(self):
        self.screen.fill(self.interface.BLACK)
        # Titles
        self.screen.blit(self.interface.font5.render("AI parameters", True, self.interface.WHITE), (10, 10))
        self.screen.blit(self.interface.font5.render("Layers", True, self.interface.SKYBLUE), (self.WIDTH//2-170, 35))
        self.screen.blit(self.interface.font5.render("Neurons/layer", True, self.interface.SKYBLUE), (self.WIDTH//2+30, 35))
        # Current values
        cfg = self.interface.config.config_AI["nn"]
        self.screen.blit(self.interface.font5.render(str(cfg["hidden_layers"]), True, self.interface.WHITE), (self.WIDTH//2-115, 62))
        self.screen.blit(self.interface.font5.render(str(cfg["neurons_per_layer"]), True, self.interface.WHITE), (self.WIDTH//2+85, 62))
        # Draw network visual
        self._draw_network()
        # Buttons
        for key in ['back','dec_layers','inc_layers','dec_neurons','inc_neurons']: self.buttons[key].draw()