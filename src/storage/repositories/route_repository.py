from datetime import datetime
from typing import List, Optional, Union
from pathlib import Path
import json
from uuid import UUID

from src.storage.models.route_model import RouteModel
from src.utils.logger import setup_logger
from src.utils.config import ProjectConfig

logger = setup_logger("storage/repositories/route", ProjectConfig.get_log_file("storage/route"))


class RouteRepository:
    """
    Repository class for managing routes.
    Handles basic CRUD operations for routes.
    """

    def __init__(self, storage_path: Union[Path, str]):
        # Convert to Path object if string is passed
        self.storage_path = Path(storage_path)
        # Create directory if it doesn't exist
        self.storage_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Initialized RouteRepository with storage path: {self.storage_path}")

    def save(self, route: RouteModel) -> None:
        """
        Save a route to the repository.
        Args:
            route (RouteModel): Route to save
        """
        # Ensure route_id is converted to string
        route_id = str(route.id)
        route_path = self.storage_path / f"{route_id}.json"

        logger.info(f"Saving route to file: {route_path}")

        # Prepare route data
        route_data = {
            "id": route_id,
            "name": route.name,
            "hold_ids": [str(hid) for hid in route.hold_ids],
            "created_at": route.created_at.isoformat(),
            "difficulty": route.difficulty,
            "description": route.description,
            "author": route.author
        }

        try:
            # Ensure the directory exists
            route_path.parent.mkdir(parents=True, exist_ok=True)

            # Write the file
            with route_path.open('w', encoding='utf-8') as f:
                json.dump(route_data, f, indent=2)

            logger.info(f"Successfully saved route {route_id} to {route_path}")

        except Exception as e:
            logger.error(f"Failed to save route {route_id}: {str(e)}")
            raise

    def get(self, route_id: str) -> Optional[RouteModel]:
        """
        Retrieve a route from the repository.
        Args:
            route_id (str): ID of the route to retrieve
        Returns:
            RouteModel: Route object if found, None otherwise
        """
        route_path = self.storage_path / f"{route_id}.json"

        if not route_path.exists():
            logger.warning(f"Route not found: {route_id}")
            return None

        try:
            logger.info(f"Loading route from file: {route_path}")
            with route_path.open('r', encoding='utf-8') as f:
                route_data = json.load(f)

            # Convert string date to datetime object
            created_at = datetime.fromisoformat(route_data["created_at"])

            return RouteModel(
                id=UUID(route_data["id"]),
                name=route_data["name"],
                hold_ids=[UUID(hold_id) for hold_id in route_data["hold_ids"]],
                created_at=created_at,
                difficulty=route_data["difficulty"],
                description=route_data["description"],
                author=route_data["author"]
            )

        except Exception as e:
            logger.error(f"Error loading route {route_id}: {str(e)}")
            return None

    def get_all(self) -> List[RouteModel]:
        """
        Retrieve all routes from the repository.
        Returns:
            List[RouteModel]: List of all routes
        """
        routes = []
        try:
            # Use glob() to find all .json files
            for route_file in self.storage_path.glob("*.json"):
                try:
                    with route_file.open('r', encoding='utf-8') as f:
                        route_data = json.load(f)

                    created_at = datetime.fromisoformat(route_data["created_at"])

                    route = RouteModel(
                        id=UUID(route_data["id"]),
                        name=route_data["name"],
                        hold_ids=[UUID(hold_id) for hold_id in route_data["hold_ids"]],
                        created_at=created_at,
                        difficulty=route_data["difficulty"],
                        description=route_data["description"],
                        author=route_data["author"]
                    )
                    routes.append(route)

                except Exception as e:
                    logger.error(f"Error loading route from {route_file}: {str(e)}")
                    continue

            return routes

        except Exception as e:
            logger.error(f"Error loading routes: {str(e)}")
            return []