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
