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
    def _write_json(self, filename: str, data: dict) -> None:
        os.makedirs(self.config_dir, exist_ok=True)
        path = os.path.join(self.config_dir, filename)
        with open(path, "w", encoding="utf-8") as f: json.dump(data, f, indent=4)
    def _deep_update(self, target: dict, src: dict) -> dict:
        for k, v in src.items():
            if isinstance(v, dict) and isinstance(target.get(k), dict): self._deep_update(target[k], v)
            else: target[k] = v
        return target
    def load_config(self):
        self.config(alls=True)
        loaded_any = False
        try:
            visuals_data = self._read_json("visuals.json")
            self._load_visuals(visuals_data)
            loaded_any = True
        except Exception: pass
