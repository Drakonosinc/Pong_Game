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
        try:
            keys_data = self._read_json("keybindings.json")
            keys_block = keys_data.get("config_keys", keys_data)
            if isinstance(keys_block, dict):
                self.config_keys.update(keys_block)
                loaded_any = True
        except Exception: pass
        try:
            settings_data = self._read_json("settings.json")
            sounds_block = settings_data.get("config_sounds")
            game_block = settings_data.get("config_game")
            if isinstance(sounds_block, dict):
                self.config_sounds.update(sounds_block)
                loaded_any = True
            if isinstance(game_block, dict):
                self.config_game.update(game_block)
                loaded_any = True
        except Exception: pass
        try:
            ai_data = self._read_json("ai_config.json")
            ai_block = ai_data.get("config_AI", ai_data)
            if isinstance(ai_block, dict):
                self._deep_update(self.config_AI, ai_block)
                loaded_any = True
        except Exception: pass
        self._validate_and_normalize()
        if not loaded_any or not self._all_config_files_exist(): self.save_config()
    def _all_config_files_exist(self) -> bool:
        return all(os.path.exists(os.path.join(self.config_dir, name))
            for name in ("visuals.json", "keybindings.json", "settings.json", "ai_config.json"))
    def save_config(self):
        self._validate_and_normalize()
        visuals_out = {
            "window": {
                "width": self.config_visuals["WIDTH"],
                "height": self.config_visuals["HEIGHT"],},
            "assets": {
                "background": self.config_visuals["image_background"],
                "value_background": self.config_visuals["value_background"],
                "planets": self.config_visuals["planets"],
                "value_planet": self.config_visuals["value_planet"],
                "spacecrafts": self.config_visuals["spacecrafts"],
                "value_spacecraft1": self.config_visuals["value_spacecraft1"],
                "value_spacecraft2": self.config_visuals["value_spacecraft2"],},}
        self._write_json("visuals.json", visuals_out)
        self._write_json("keybindings.json", {"config_keys": self.config_keys})
        self._write_json("settings.json", {"config_sounds": self.config_sounds, "config_game": self.config_game},)
        self._write_json("ai_config.json", {"config_AI": self.config_AI})
    def _load_visuals(self, data: dict) -> None:
        if not isinstance(data, dict): return
        if isinstance(data.get("config_visuals"), dict):
            self.config_visuals.update(data["config_visuals"])
            return
        window = data.get("window", {})
        assets = data.get("assets", {})
        if isinstance(window, dict):
            if "width" in window: self.config_visuals["WIDTH"] = window["width"]
            if "height" in window: self.config_visuals["HEIGHT"] = window["height"]
        if isinstance(assets, dict):
            if "background" in assets: self.config_visuals["image_background"] = assets["background"]
            elif "image_background" in assets: self.config_visuals["image_background"] = assets["image_background"]
            for k in (
                "value_background",
                "planets",
                "value_planet",
                "spacecrafts",
                "value_spacecraft1",
                "value_spacecraft2",):
                if k in assets: self.config_visuals[k] = assets[k]
    def config(self, visuals=False, keys=False, sounds=False, AI=False, game=False, alls=False):
        if visuals or alls:
            self.config_visuals = {
                "WIDTH": 700,
                "HEIGHT": 400,
                "image_background": [
                    "background1.jpg",
                    "background2.jpg",
                    "background3.jpg",
                    "background4.jpg",
                    "background5.jpg",
                    "background6.jpg",
                    "background7.jpg",
                    "background8.jpg",],
                "value_background": 0,
                "planets": ["Mars.png", "Mars1.png", "meteorite.png", "Saturn.png", "earth.png"],
                "value_planet": 0,
                "spacecrafts": ["spaceship.png", "spaceship2.png", "spaceship3.png"],
                "value_spacecraft1": 0,
                "value_spacecraft2": 0,}
        if keys or alls:
            self.config_keys = {
                "UP_W": K_w,
                "Name_key1": "W",
                "DOWN_S": K_s,
                "Name_key2": "S",
                "UP_ARROW": K_UP,
                "Name_key3": "↑",
                "DOWN_ARROW": K_DOWN,
                "Name_key4": "↓",}
        if sounds or alls:
            self.config_sounds = {"sound_main": True}
        if AI or alls:
            self.config_AI = {
                "model_save": False,
                "type_training": {"Genetic": True, "Q-learning": False},
                "type_model": {"Pytorch": True, "Tensorflow": False},
                "genetic": {"generation_value": 100, "population_value": 20, "try_for_ai": 3},
                "q_learning": {
                    "episodes": 500,
                    "learning_rate": 0.001,
                    "gamma": 0.99,
                    "epsilon_start": 1.0,
                    "epsilon_end": 0.01,
                    "epsilon_decay": 0.995,
                    "memory_size": 10000,
                    "batch_size": 32,
                    "target_update": 100,},
                "nn": {"hidden_layers": 2, "neurons_per_layer": 6},}
        if game or alls:
            self.config_game = {"number_balls": 1, "max_score": 5}
    def _validate_and_normalize(self):
        if not hasattr(self, "config_visuals") or not isinstance(self.config_visuals, dict): self.config(visuals=True)
        if not hasattr(self, "config_keys") or not isinstance(self.config_keys, dict): self.config(keys=True)
        if not hasattr(self, "config_sounds") or not isinstance(self.config_sounds, dict): self.config(sounds=True)
        if not hasattr(self, "config_AI") or not isinstance(self.config_AI, dict): self.config(AI=True)
        if not hasattr(self, "config_game") or not isinstance(self.config_game, dict): self.config(game=True)
        def as_int(v, default: int) -> int:
            if isinstance(v, bool): return default
            try: return int(v)
            except Exception: return default
        self.config_visuals["WIDTH"] = max(1, as_int(self.config_visuals.get("WIDTH"), 700))
        self.config_visuals["HEIGHT"] = max(1, as_int(self.config_visuals.get("HEIGHT"), 400))
        default_lists = {
            "image_background": [
                "background1.jpg",
                "background2.jpg",
                "background3.jpg",
                "background4.jpg",
                "background5.jpg",
                "background6.jpg",
                "background7.jpg",
                "background8.jpg",],
            "planets": ["Mars.png", "Mars1.png", "meteorite.png", "Saturn.png", "earth.png"],
            "spacecrafts": ["spaceship.png", "spaceship2.png", "spaceship3.png"],}
        for list_key, idx_key in (
            ("image_background", "value_background"),
            ("planets", "value_planet"),
            ("spacecrafts", "value_spacecraft1"),
            ("spacecrafts", "value_spacecraft2"),):
            items = self.config_visuals.get(list_key)
            if not isinstance(items, list) or len(items) == 0:
                items = list(default_lists[list_key])
                self.config_visuals[list_key] = items
            idx = as_int(self.config_visuals.get(idx_key), 0)
            self.config_visuals[idx_key] = idx % len(items)
        default_keycodes = {
            "UP_W": K_w,
            "DOWN_S": K_s,
            "UP_ARROW": K_UP,
            "DOWN_ARROW": K_DOWN,}
        default_keynames = {
            "Name_key1": "W",
            "Name_key2": "S",
            "Name_key3": "↑",
            "Name_key4": "↓",}
        for k, dv in default_keycodes.items(): self.config_keys[k] = as_int(self.config_keys.get(k), int(dv))
        for nk, dv in default_keynames.items():
            v = self.config_keys.get(nk, dv)
            self.config_keys[nk] = v if isinstance(v, str) else str(v)
        self.config_sounds["sound_main"] = bool(self.config_sounds.get("sound_main", True))
        nb = self.config_game.get("number_balls", 1)
        if isinstance(nb, bool): nb = 1 if nb else 0
        nb = max(1, as_int(nb, 1))
        self.config_game["number_balls"] = nb
        self.config_game["max_score"] = max(1, as_int(self.config_game.get("max_score", 5), 5))
        self.config_AI["model_save"] = bool(self.config_AI.get("model_save", False))
        tt = self.config_AI.get("type_training")
        if not isinstance(tt, dict): tt = {"Genetic": True, "Q-learning": False}
        if "genetic" in tt and "Genetic" not in tt: tt["Genetic"] = bool(tt.get("genetic"))
        if ("q-learning" in tt or "q_learning" in tt) and "Q-learning" not in tt: tt["Q-learning"] = bool(tt.get("q-learning", tt.get("q_learning")))
        tt.setdefault("Genetic", True)
        tt.setdefault("Q-learning", False)
        if not any(bool(v) for v in tt.values()): tt["Genetic"] = True
        self.config_AI["type_training"] = {"Genetic": bool(tt.get("Genetic")), "Q-learning": bool(tt.get("Q-learning"))}
        tm = self.config_AI.get("type_model")
        if not isinstance(tm, dict): tm = {"Pytorch": True, "Tensorflow": False}
        tm.setdefault("Pytorch", True)
        tm.setdefault("Tensorflow", False)
        if not any(bool(v) for v in tm.values()): tm["Pytorch"] = True
        self.config_AI["type_model"] = {"Pytorch": bool(tm.get("Pytorch")), "Tensorflow": bool(tm.get("Tensorflow"))}
        genetic = self.config_AI.get("genetic")
        if not isinstance(genetic, dict): genetic = {}
        genetic.setdefault("generation_value", as_int(self.config_AI.get("generation_value", 100), 100))
        genetic.setdefault("population_value", as_int(self.config_AI.get("population_value", 20), 20))
        genetic.setdefault("try_for_ai", as_int(self.config_AI.get("try_for_ai", 3), 3))
        genetic["generation_value"] = max(1, as_int(genetic.get("generation_value"), 100))
        genetic["population_value"] = max(1, as_int(genetic.get("population_value"), 20))
        genetic["try_for_ai"] = max(1, as_int(genetic.get("try_for_ai"), 3))
        self.config_AI["genetic"] = genetic
        ql = self.config_AI.get("q_learning")
        if not isinstance(ql, dict): ql = {}
        defaults_ql = {
            "episodes": 500,
            "learning_rate": 0.001,
            "gamma": 0.99,
            "epsilon_start": 1.0,
            "epsilon_end": 0.01,
            "epsilon_decay": 0.995,
            "memory_size": 10000,
            "batch_size": 32,
            "target_update": 100,}
        for k, dv in defaults_ql.items(): ql.setdefault(k, dv)
        ql["episodes"] = max(1, as_int(ql.get("episodes"), 500))
        ql["memory_size"] = max(1, as_int(ql.get("memory_size"), 10000))
        ql["batch_size"] = max(1, as_int(ql.get("batch_size"), 32))
        ql["target_update"] = max(1, as_int(ql.get("target_update"), 100))
        for fk, dv in (
            ("learning_rate", 0.001),
            ("gamma", 0.99),
            ("epsilon_start", 1.0),
            ("epsilon_end", 0.01),
            ("epsilon_decay", 0.995),):
            try: ql[fk] = float(ql.get(fk, dv))
            except Exception: ql[fk] = float(dv)
        self.config_AI["q_learning"] = ql
        nn = self.config_AI.get("nn")
        if not isinstance(nn, dict): nn = {}
