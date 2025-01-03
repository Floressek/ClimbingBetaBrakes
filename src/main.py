# src/main.py
import sys
from PyQt5.QtWidgets import QApplication

from src.core.hold import Hold
from utils.config import ProjectConfig
from utils.logger import setup_logger
from api.roboflow_client import RoboflowClient
from gui.main_window import MainWindow


def run_application():
    """Runs the main GUI application."""
    # Initialize logging
    logger = setup_logger("main", ProjectConfig.get_log_file("main"))
    logger.info("Starting Climbing Route Creator")

    try:
        # Initialize project configuration
        ProjectConfig.initialize()

        # Initialize Roboflow client
        roboflow_config = ProjectConfig.get_roboflow_config()
        client = RoboflowClient(roboflow_config)

        # Create Qt application
        app = QApplication(sys.argv)
        window = MainWindow()

        # Load and detect holds in example image
        image_path = ProjectConfig.PROJECT_ROOT / "data" / "images" / "test_wall_2.jpg"

        # First load the image into HoldViewer
        window.hold_viewer.load_image(str(image_path))

        # Then detect and add holds
        detection_result = client.detect_holds(image_path)

        # Convert detections to Hold objects and pass them to the viewer
        for pred in detection_result['predictions']:
            hold = Hold.from_detection(pred)
            window.hold_viewer.holds.append(hold)

        # Force update of the hold viewer to display everything
        window.hold_viewer.update()

        # Show the window
        window.show()

        # Start the application event loop
        sys.exit(app.exec_())

    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        raise

if __name__ == "__main__":
    run_application()
# from pathlib import Path
# from utils.config import ProjectConfig, RoboflowConfig
# from utils.logger import setup_logger
# from api.roboflow_client import RoboflowClient
# from core.hold import Hold
#
#
# def analyze_climbing_wall():
#     """
#     Main function demonstrating the full process of analyzing a climbing wall:
#     1. Detect holds in an image
#     2. Convert API data into business objects
#     3. Perform basic analysis of the detected holds
#     4. Visualize the results
#     """
#     # Initialize the logger to display program progress
#     logger = setup_logger("main", ProjectConfig.get_log_file("main"))
#     logger.info("Starting climbing wall analysis")
#
#     try:
#         # First, initialize the project configuration
#         # This will create necessary directories and validate environment variables
#         ProjectConfig.initialize()
#         logger.info("Project configuration initialized")
#
#         # Retrieve Roboflow configuration from environment variables
#         roboflow_config = ProjectConfig.get_roboflow_config()
#         logger.info("Roboflow configuration retrieved")
#
#         # Create a Roboflow API client to communicate with the service
#         client = RoboflowClient(roboflow_config)
#         logger.info("Roboflow client created")
#
#         # Define the path to the test image
#         image_path = ProjectConfig.PROJECT_ROOT / "data" / "images" / "test_wall_2.jpg"
#
#         # Check if the image exists
#         if not image_path.exists():
#             raise FileNotFoundError(f"Test image not found: {image_path}")
#
#         # Perform hold detection on the image
#         logger.info(f"Starting hold detection on image: {image_path}")
#         detection_result = client.detect_holds(image_path)
#
#         # Transform raw API data into business objects
#         holds = []
#         for prediction in detection_result['predictions']:
#             hold = Hold.from_detection(prediction)
#             holds.append(hold)
#
#             # # Log details about each detected hold #FIXME: logger.info
#             # logger.info(
#             #     f"Detected hold: "
#             #     f"position=({hold.x:.1f}, {hold.y:.1f}), "
#             #     f"dimensions={hold.width:.1f}x{hold.height:.1f}, "
#             #     f"confidence={hold.confidence:.2f}"
#             # )
#
#         # Perform basic analysis on the detected holds
#         logger.info(f"\nAnalysis summary:")
#         logger.info(f"Total number of detected holds: {len(holds)}")
#
#         # Identify holds with the highest and lowest detection confidence
#         most_confident = max(holds, key=lambda h: h.confidence)
#         least_confident = min(holds, key=lambda h: h.confidence)
#
#         logger.info(
#             f"Hold with highest detection confidence: "
#             f"{most_confident.confidence:.2f} at position ({most_confident.x:.1f}, {most_confident.y:.1f})"
#         )
#         logger.info(
#             f"Hold with lowest detection confidence: "
#             f"{least_confident.confidence:.2f} at position ({least_confident.x:.1f}, {least_confident.y:.1f})"
#         )
#
#         # Save visualization of the results
#         output_path = ProjectConfig.EXPORTS_DIR / "detected_holds_2.jpg"
#         # output_path = ProjectConfig.EXPORTS_DIR
#         client.visualize_detections(image_path, detection_result, output_path)
#         logger.info(f"\nVisualization saved to: {output_path}")
#
#     except Exception as e:
#         logger.error(f"An error occurred during analysis: {str(e)}")
#         raise
#
#
# if __name__ == "__main__":
#     analyze_climbing_wall()

