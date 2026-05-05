import os
from dataclasses import dataclass
from typing import Any
@dataclass(slots=True)
class AIModelLoadResult:
    model: Any = None
    model_found: bool = False
    error_message: str | None = None
class AILoader:
    def __init__(self, context_or_config):
        if hasattr(context_or_config, "base_dir") and hasattr(context_or_config, "config_AI"):
            self.config = context_or_config
        else: self.config = context_or_config.config
        self.base_dir = self.config.base_dir
    def _get_selected_training(self) -> str:
        training = next((key for key, value in self.config.config_AI["type_training"].items() if value), None)
        if training is None: raise ValueError("No se especifico un tipo de entrenamiento valido.")
        return training
    def _get_selected_model(self) -> str:
        model = next((key for key, value in self.config.config_AI["type_model"].items() if value), None)
        if model is None: raise ValueError("No se especifico un tipo de modelo valido.")
        return model
    def _get_hidden_architecture(self) -> list[int]:
        nn_cfg = self.config.config_AI.get("nn", {"hidden_layers": 2, "neurons_per_layer": 6})
        neurons = nn_cfg.get("neurons_per_layer", 6)
        layers = nn_cfg.get("hidden_layers", 2)
        return [neurons] * layers
    def _resolve_loader(self):
