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
