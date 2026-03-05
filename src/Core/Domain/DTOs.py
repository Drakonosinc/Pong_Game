from dataclasses import dataclass
import numpy as np
@dataclass(frozen=True)
class WorldStateDTO:
    p1_x: float
    p1_y: float
    p2_x: float
    p2_y: float
    ball_x: float
    ball_y: float
    def to_array(self) -> np.ndarray:
        return np.array([
            self.p1_x, self.p1_y, 
            self.p2_x, self.p2_y, 
