from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass, field
from pathlib import Path
import json
from uuid import UUID

from src.storage.models.route_model import RouteModel
from src.utils.logger import setup_logger
from src.utils import ProjectConfig

logger = setup_logger("storage/repositories/route", ProjectConfig.get_log_file("storage/route"))

class RouteRepository: #FIXME: TODO: Change it to actual database
    """
    Repository class for managing routes.
    Handles basic CRUD operations for routes.
    """
    def __init__(self, storage_path: Path):
        self.storage_path = storage_path
        self.storage_path.mkdir(parents=True, exist_ok=True)

    def save(self, route: RouteModel) -> None:
        """
        Save a route to the repository.
        Args:
            route (RouteModel): Route to save
        """
        route_path = self.storage_path / f"{route.id}.json"
        logger.info(f"Saving route to file: {route_path}")
        route_data = {
            "id": str(route.id),
            "name": route.name,
            "hold_ids": [str(hid) for hid in route.hold_ids],
            "created_at": route.created_at.isoformat(),
            "difficulty": route.difficulty,
            "description": route.description,
            "author": route.author
        }
        with open(route_path, 'w') as f:
            json.dump(route_data, f, indent=2)

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
        logger.info(f"Loading route from file: {route_path}")
        try:
            with open(route_path, 'r') as f:
                route_data = json.load(f)

            # Konwertujemy string daty na obiekt datetime
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
            return route
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Error loading route {route_id}: {str(e)}")
            return None

    def get_all(self) -> List[RouteModel] or None:
        """
        Retrieve all routes from the repository.
        Returns:
            List[RouteModel]: List of all routes
        """
        routes = []
        try:
            for route_file in self.storage_path.glob("*.json"):
                with open(route_file, 'r') as f:
                    route_data = json.load(f)
                route = RouteModel(
                    id=UUID(route_data["id"]),
                    name=route_data["name"],
                    hold_ids=[hold_id for hold_id in route_data["hold_ids"]],
                    created_at=route_data["created_at"],
                    difficulty=route_data["difficulty"],
                    description=route_data["description"],
                    author=route_data["author"]
                )
                routes.append(route)
            return routes
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Error loading all routes: {str(e)}")
            return None

