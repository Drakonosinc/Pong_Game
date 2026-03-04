from dataclasses import dataclass
import numpy as np
@dataclass(frozen=True)
class WorldStateDTO:
    p1_x: float
