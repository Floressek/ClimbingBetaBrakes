from dataclasses import dataclass, field
from typing import List, Optional, Tuple
from uuid import UUID, uuid4
from shapely.geometry import Polygon, Point

from src.utils import ProjectConfig
from src.utils.logger import setup_logger
from src.core.movement_type import HoldType

logger = setup_logger("core/hold", ProjectConfig.get_log_file("core"))


@dataclass
class HoldPoint:
    """
    Represents a point in 2D space on our holds.
    Note:
        Representation of points returned by API that comprises into a singular hold.
    """
    x: float
    y: float

    def __post_init__(self):
        """Data validation after object creation."""
        if not isinstance(self.x, (int, float)) or not isinstance(self.y, (int, float)):
            logger.error("Coordinates must be numbers.")
            raise ValueError("Coordinates must be numbers.")


@dataclass
class Hold:
    """
    Represents a climbing hold with exact coordinates contoured by a polygon.

    Note:
        Representation of holds returned by API.

    Attributes:
        id (UUID): Unique identifier for the hold
        x (float): X coordinate of the top-left corner of the bounding box
        y (float): Y coordinate of the top-left corner of the bounding box
        width (float): Width of the bounding box
        height (float): Height of the bounding box
        confidence (float): Confidence of the detection
        contour_points (List[HoldPoint]): List of points that make up the contour of the hold
        is_selected (bool): Flag indicating whether the hold is selected
        order_in_route (Optional[int]): Order of the hold in the climbing route
        comment (Optional[str]): Comment for the hold

    """
    id: UUID
    x: float
    y: float
    width: float
    height: float
    confidence: float
    contour_points: List[HoldPoint] = field(
        default_factory=list)  # default_factory=list creates a new list for each instance not one shared among all instances!!!
    is_selected: bool = False
    order_in_route: Optional[int] = None
    comment: Optional[str] = None
    hold_type: HoldType = HoldType.HAND # Default to hands

    @classmethod
    def from_detection(cls, detection: dict) -> 'Hold':
        """
        Create a Hold object from the detection dictionary.

        Args:
            detection (dict): Detection dictionary from the API

        Returns:
            Hold: Hold object created from the detection
        """

        # Transform points from API to HoldPoint objects
        contour_points_data = detection.get('points', [])
        contour_points = [
            HoldPoint(point['x'], point['y'])
            for point in contour_points_data
        ]
        return cls(
            id=uuid4(),
            x=detection['x'],
            y=detection['y'],
            width=detection['width'],
            height=detection['height'],
            confidence=detection['confidence'],
            contour_points=contour_points
        )

    @property
    def bounds(self) -> Tuple[float, float, float, float]:
        """
        Get the bounding box coordinates of the hold.

        Returns:
            Tuple[float, float, float, float]: Tuple of (x, y, width, height) of the bounding box
        """
        half_width = self.width / 2
        half_height = self.height / 2
        x_min = self.x - half_width
        y_min = self.y - half_height
        y_max = self.y + half_height
        x_max = self.x + half_width
        return x_min, y_min, x_max, y_max

    @property
    def polygon(self) -> Optional[Polygon]:
        """
        Get the polygon representation of the hold.

        Returns:
            Polygon: Shapely Polygon object representing the hold
        """

        if not self.contour_points:
            logger.warning("No contour points available for hold.")
            return None

        # Making a polygon from the contour points
        points = [(p.x, p.y) for p in self.contour_points]
        return Polygon(points)

    def contains_point(self, px: float, py: float) -> bool:
        """
        Check if the hold contains a given point.

        Args:
            px (float): X coordinate of the point
            py (float): Y coordinate of the point

        Returns:
            bool: True if the point is contained within the hold, False otherwise
        """
        point = Point(px, py)
        polygon = self.polygon

        if polygon:
            logger.debug("Checking if point is within the hold.")
            return polygon.contains(point)
        else:
            # If no polygon is available, we use brute rectangle check
            logger.warning("No polygon available, using bounding box check.")
            x_min, y_min, x_max, y_max = self.bounds
            return x_min <= px <= x_max and y_min <= py <= y_max  # check if point is within the bounding box
