import json, os
from pygame.locals import *
class Config:
    def __init__(self):
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
        self.config_dir = os.path.join(self.base_dir, "Config")
    def _read_json(self, filename: str) -> dict:
        path = os.path.join(self.config_dir, filename)
        with open(path, "r", encoding="utf-8") as f: data = json.load(f)
        return data if isinstance(data, dict) else {}
