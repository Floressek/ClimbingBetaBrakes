from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from src.core.connection import Connection
from src.core.hold import Hold, logger
from src.storage.models.route_model import RouteModel
from src.utils.logger import setup_logger
from src.utils.config import ProjectConfig

logger = setup_logger("core/route", ProjectConfig.get_log_file("core"))


@dataclass
class Route:
    """
    Data class representing a climbing route. For business logic. The data goes to -> route_model.py in storage/models
    Attributes:
        hold_ids (List[UUID]): List of hold IDs associated with the route
        id (UUID): Unique identifier for the route
        created_at (datetime): Date and time when the route was created
        name (str): Route name
        grade (Optional[str]): Route grade
        description (Optional[str]): Route description
        author (Optional[str]): Route author
        hand_holds (List[Hold]): List of hand holds in the route
        foot_holds (List[Hold]): List of foot holds in the route
        connections (List[Connection]): List of connections between holds in the route
    """
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    name: str = "Unnamed Route"
    grade: Optional[str] = None
    description: Optional[str] = None
    author: Optional[str] = None

    hand_holds: List[Hold] = field(default_factory=list)
    foot_holds: List[Hold] = field(default_factory=list)
    connections: List[Connection] = field(default_factory=list)

    def to_model(self) -> 'RouteModel':
        """
        Convert the Route object to a RouteModel object.
        """

        # Collect all hold IDs
        hold_ids = [hold.id for hold in self.hand_holds]
        hold_ids.extend([hold.id for hold in self.foot_holds])

        return RouteModel(
            name=self.name,
            hold_ids=hold_ids,
            id=self.id,
            created_at=self.created_at,
            difficulty=self.grade,
            description=self.description,
            author=self.author
        )

    @classmethod
    def from_holds(cls, hand_holds: List[Hold], foot_holds: List[Hold], **kwargs) -> 'Route': # **kwargs is a dictionary
        """
        Create a Route object from a list of hand and foot holds.
        Args:
            hand_holds (List[Hold]): List of hand holds
            foot_holds (List[Hold]): List of foot holds
            **kwargs: Additional route attributes
        """
        hand_holds = sorted
