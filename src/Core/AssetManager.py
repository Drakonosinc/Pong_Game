import pygame
import os
class AssetManager:
    def __init__(self, config, window_manager):
        self.config = config
        self.window_manager = window_manager
        self.WIDTH = window_manager.render_width
        self.HEIGHT = window_manager.render_height
        self.image_path = os.path.join(self.config.base_dir, "images")
        self.font_path = os.path.join(self.config.base_dir, "fonts")
