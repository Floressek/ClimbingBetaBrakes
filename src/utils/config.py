from pathlib import Path
from typing import Optional, Union, Dict, Any
import os
from dataclasses import dataclass
from datetime import datetime

from .logger import setup_logger


@dataclass
class RoboflowConfig:
    """
    Configuration for the Roboflow API
    Attributes:
        api_key: API key for Roboflow
        project_id: Project ID for Roboflow
        model_version_id: Model version ID for Roboflow
        confidence_threshold: Confidence threshold for detection (0.0-1.0)
        overlap_threshold: Overlap threshold for detection (0.0-1.0)
    """
    api_key: str
    project_id: str = "hold-detection-rnvkl"
    model_version_id: int = 2
    confidence_threshold: float = 0.4
    overlap_threshold: float = 0.3

    def __post_init__(self):
        """Data validation after object creation."""
        if not 0 <= self.confidence_threshold <= 1:
            raise ValueError("Confidence threshold must be between 0.0 and 1.0.")
        if not 0 <= self.overlap_threshold <= 1:
            raise ValueError("Overlap threshold must be between 0.0 and 1.0.")


class ProjectConfig:
    """Main configuration for the project. Contains paths to directories and files."""

    # Project structure
    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent  # 3 levels up
    LOGS_DIR = PROJECT_ROOT / "logs"
    DATA_DIR = PROJECT_ROOT / "data"
    CACHE_DIR = DATA_DIR / "cache"
    ROUTES_DIR = DATA_DIR / "routes"
    IMAGES_DIR = DATA_DIR / "images"
    EXPORTS_DIR = DATA_DIR / "exports"

    # Application settings
    MAX_IMAGE_SIZE = 4096  # Maximum image size for display
    SUPPORTED_IMAGE_FORMATS = ["png", "jpg", "jpeg"]
    MAX_CACHE_SIZE = 500  # Maximum number of items in cache

    # Logger for the conf module
    logger = None  # not needed, but can be used for debugging

    @classmethod
    def initialize(cls) -> None:
        """
        Initialize the project configuration.
        Creates necessary directories and sets up the logger.

        Raises:
            ValueError: If the configuration is invalid.
        """
        cls.logger = setup_logger(
            "conf",
            cls.get_log_file("conf")
        )

        cls.logger.info("Initializing project configuration...")

        directories = [
            cls.LOGS_DIR,
            cls.DATA_DIR,
            cls.CACHE_DIR,
            cls.ROUTES_DIR,
            cls.IMAGES_DIR,
            cls.EXPORTS_DIR
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            cls.logger.info(f"Created directory: {directory}")

        cls._validate_environment()
        cls.logger.info("Project configuration initialized successfully.")

    @classmethod
    def get_log_file(cls, name) -> str:
        """
        Generate a log file path.
        Args:
            name: Name of the log file.

        Returns:
            str: Path to the log file.
        """
        return str(cls.LOGS_DIR / f"{name}.log")

    @classmethod
    def get_cache_path(cls, key) -> Path:
        """
        Generate a cache file path.
        Args:
            key: Key for the cache file.

        Returns:
            Path: Path to the cache file.
        """
        return cls.CACHE_DIR / f"{key}.cache"

    @classmethod
    def _validate_environment(cls) -> None:
        """
        Validate the project environment.

        Raises:
            ValueError: If the environment is invalid.
        """
        requried_env_vars = ["ROBOFLOW_API_KEY"]
        missing_vars = [var for var in requried_env_vars if var not in os.environ]

        if missing_vars:
            cls.logger.error(f"Missing environment variables: {missing_vars}")
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

    @classmethod
    def validate_image_path(cls, path: Union[str, Path]) -> Path:
        """
        Validate the image path and return a Path object.
        Args:
            path: Path to the image file.
        Returns:
            Path: Path to the image file.
        Raises:
            ValueError: If the path is invalid.
        """
        path = Path(path)
        if not path.exists():
            cls.logger.error(f"Image file not found: {path}")
            raise ValueError(f"Image file not found: {path}")

        if path.suffix.lower() not in cls.SUPPORTED_IMAGE_FORMATS:
            cls.logger.error(f"Unsupported image format: {path.suffix}")
            raise ValueError(
                f"Unsupported image format: {path.suffix}"
                f"Supported formats: {', '.join(cls.SUPPORTED_IMAGE_FORMATS)}"
            )
        return path
