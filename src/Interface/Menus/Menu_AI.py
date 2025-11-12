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
