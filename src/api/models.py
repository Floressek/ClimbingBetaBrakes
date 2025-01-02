from dataclasses import dataclass
from typing import List, Optional
from pydantic import BaseModel

@dataclass()
class Point:
    """Represents a point in 2D space on our holds."""
    x: float
    y: float

    def __post_init__(self):
        """Data validation after object creation."""
        if not isinstance(self.x, (int, float)) or not isinstance(self.y, (int, float)):
            raise ValueError("Coordinates must be numbers.")