import os
from pathlib import Path
from utils.config import ProjectConfig
from utils.logger import setup_logger
from api.roboflow_client import RoboflowClient

def main():
    # Logger initialization
    logger = setup_logger("main", ProjectConfig.get_log_file("main"))
    logger.info("Starting the application...")

    try:
        # Project config initialization
        ProjectConfig.initialize()
        logger.info("Project configuration initialized successfully.")

        # Roboflow client initialization
        roboflow_config = ProjectConfig.get_roboflow_config()

        # Client initialization
        client = RoboflowClient(roboflow_config) # prolly gives that weird info about initialization
        logger.info("Roboflow client initialized successfully.")

        # Image path
        image_path = ProjectConfig.PROJECT_ROOT / "data" / "images" / "test_wall.jpg"
        if not image_path.exists():
            logger.error(f"Image not found: {image_path}")
            raise FileNotFoundError(f"Image not found: {image_path}")

        # Detect holds
        result = client.detect_holds(image_path)
        logger.info(f"Detected holds completed.")
        # logger.info(f"Detected holds: {len(result['predictions'])}")

        # Visualize detections
        output_path = ProjectConfig.EXPORTS_DIR / "detections.jpg"
        client.visualize_detections(image_path, result, output_path)
        logger.info(f"Detections saved to: {output_path}")

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    main()