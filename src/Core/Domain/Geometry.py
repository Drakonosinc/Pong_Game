from dataclasses import dataclass
from typing import Union, Tuple
@dataclass
class Rectangle:
    x: float
    y: float
    width: float
    height: float
    @property
    def left(self) -> float: return self.x
