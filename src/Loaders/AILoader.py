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
