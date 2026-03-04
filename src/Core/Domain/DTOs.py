from dataclasses import dataclass
import numpy as np
@dataclass(frozen=True)
class WorldStateDTO:
    p1_x: float
    p1_y: float
    p2_x: float
    p2_y: float
