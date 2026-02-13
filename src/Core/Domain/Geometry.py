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
    def colliderect(self, other: 'Rectangle') -> bool:
        if not isinstance(other, Rectangle): raise TypeError("Collision check requires a Rectangle instance.")
        return (self.x < other.x + other.width and
                self.x + self.width > other.x and
