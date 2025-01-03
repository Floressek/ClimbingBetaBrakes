from enum import Enum


class HoldType(Enum):
    """
    Enum class for movement types.

    Attributes:
        HANDS: Hands movement
        FEET: Feet movement
    """
    HAND = "hands"
    FEET = "feet"
