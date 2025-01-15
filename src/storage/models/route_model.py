from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4


@dataclass
class RouteModel:
    """
    Route model class.
    Attributes:
        name (str): Route name
        hold_ids (List[UUID]): List of hold IDs associated with the route
        id (UUID): Unique identifier for the route
        created_at (datetime): Date and time when the route was created
        difficulty (Optional[str]): Route difficulty
        description (Optional[str]): Route description
        author (Optional[str]): Route author
    """
    name: str
    hold_ids: List[UUID]  # Hold IDs associated with the route
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    difficulty: Optional[str] = None
    description: Optional[str] = None
    author: Optional[str] = None

    @classmethod
    def create(cls, name: str, hold_ids: List[UUID], difficulty: str, description: str, author: str):
        return cls(
            id=uuid4(),
            name=name,
            hold_ids=hold_ids,
            created_at=datetime.now(),
            difficulty=difficulty,
            description=description,
            author=author
        )
