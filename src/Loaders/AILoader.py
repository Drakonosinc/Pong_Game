import os
from dataclasses import dataclass
from typing import Any
@dataclass(slots=True)
class AIModelLoadResult:
    model: Any = None
    model_found: bool = False
    error_message: str | None = None
class AILoader:
