from dataclasses import dataclass
from typing import Tuple, Iterator
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
        if not isinstance(other, Rectangle): return False
        return (self.x < other.x + other.width and
                self.x + self.width > other.x and
                self.y < other.y + other.height and
                self.y + self.height > other.y)
    def to_tuple(self) -> Tuple[float, float, float, float]: return (self.x, self.y, self.width, self.height)
    def __iter__(self) -> Iterator[float]:
        yield self.x
        yield self.y
        yield self.width
        yield self.height
    def __getitem__(self, index: int) -> float: return self.to_tuple()[index]
    def __len__(self) -> int: return 4