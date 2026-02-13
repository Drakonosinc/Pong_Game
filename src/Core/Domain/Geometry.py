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
    @property
    def right(self) -> float: return self.x + self.width
    @property
    def top(self) -> float: return self.y
    @property
    def bottom(self) -> float: return self.y + self.height
    @property
    def center(self) -> Tuple[float, float]: return (self.x + self.width / 2, self.y + self.height / 2)
