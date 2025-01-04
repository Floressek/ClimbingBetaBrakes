from dataclasses import dataclass, field
from typing import List, Optional, Tuple
from uuid import UUID, uuid4
from .hold import Hold
from src.utils import ProjectConfig
from src.utils.logger import setup_logger

logger = setup_logger("core/connection", ProjectConfig.get_log_file("core"))

@dataclass
class Connection:
    """
    Represents a connection between two holds.

    Note:
       Can be either straight or curved. Benzian curve is used to represent the curve.

    Attributes:
        id (UUID): Unique identifier for the connection
        hold1 (Hold): First hold in the connection
        hold2 (Hold): Second hold in the connection
        is_curved (bool): Flag indicating whether the connection is curved
        order_in_route (Optional[int]): Order of the connection in the climbing route
        comment (Optional[str]): Comment for the connection
    """
    id: UUID
    hold1: Hold
    hold2: Hold
    is_curved: bool
    number: Optional[int] = None
    control_points: Optional[Tuple[float, float]] = None

    def __init__(self, hold1: Hold, hold2: Hold, number: Optional[int] = None):
        """
        Initializes a connection between two holds.
        :param hold1:
        :param hold2:
        :param number:
        """
        self.id = uuid4()
        self.hold1 = hold1
        self.hold2 = hold2
        self.is_curved = True
        self.control_points = None
        self.number = number

    @property
    def midpoint(self) -> Optional[Tuple[float, float]]:
        """
        Calculates the midpoint of the connection.
        :return:
        """
        if not (self.hold1 and self.hold2):
            logger.error("Cannot calculate midpoint without both holds.")
            return None
        return (self.hold1.x + self.hold2.x) / 2, (self.hold1.y + self.hold2.y) / 2