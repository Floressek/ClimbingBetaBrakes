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


import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from src.core.hold import Hold
from src.api.roboflow_client import RoboflowClient
from src.gui.main_window import MainWindow
from src.gui.widgets.startup_window import StartupWindow
from src.gui.widgets.loading_window import LoadingWindow

from src.utils.logger import setup_logger
from src.utils.config import ProjectConfig

logger = setup_logger("main", ProjectConfig.get_log_file("main"))


class ClimbingApp:
    """
    Main application class for the Climbing Route Creator.
    """

    def __init__(self):
        logger.info("Initializing ClimbingApp...")
        self.app = QApplication(sys.argv)

        logger.info("Initializing project configuration...")
        ProjectConfig.initialize()

        # Initialize windows
        logger.info("Creating StartupWindow...")
        self.startup_window = StartupWindow()

        logger.info("Creating LoadingWindow...")
        self.loading_window = LoadingWindow()

        self.main_window = None  # Main window will be initialized later
        logger.info("Initializing RoboflowClient...")
        self.roboflow_client = RoboflowClient(ProjectConfig.get_roboflow_config())

        # Connect signals
        logger.info("Connecting signals for StartupWindow...")
        self.startup_window.image_uploaded.connect(self.handle_image_upload)

    def run(self):
        """
        Starts the application.
        :return: Exit code of the application.
        """
        logger.info("Starting application...")
        self.startup_window.show()
        return self.app.exec_()

    def handle_image_upload(self, image_path):
        """
        Handles the image upload event.
        :param image_path: Path to the uploaded image.
        """
        logger.info(f"Image uploaded: {image_path}. Showing LoadingWindow...")
        self.startup_window.hide()
        self.loading_window.start_animation()
        self.loading_window.show()

        # Simulating processing delay for loading window
        logger.info("Starting image processing simulation...")
        QTimer.singleShot(5000, lambda: self.init_main_window(image_path))

    def init_main_window(self, image_path):
        """
        Initializes the main window with the given image path.
        :param image_path: Path to the uploaded image.
        """
        try:
            logger.info("Loading detection results from Roboflow...")
            detection_result = self.roboflow_client.detect_holds(image_path)

            logger.info("Initializing MainWindow...")
            self.main_window = MainWindow()

            logger.info(f"Loading image into MainWindow: {image_path}")
            self.main_window.hold_viewer.load_image(image_path)

            logger.info("Adding detected holds to HoldViewer...")
            for pred in detection_result['predictions']:
                hold = Hold.from_detection(pred)
                # logger.debug(f"Detected hold: {hold}")
                self.main_window.hold_viewer.holds.append(hold)

            logger.info("Stopping LoadingWindow animation and hiding it...")
            self.loading_window.stop_animation()
            self.loading_window.hide()

            logger.info("Showing MainWindow and updating HoldViewer...")
            self.main_window.show()
            self.main_window.hold_viewer.update()

        except Exception as e:
            logger.error(f"Error initializing MainWindow: {e}")
            self.loading_window.stop_animation()
            raise


if __name__ == "__main__":
    logger.info("Launching Climbing Route Creator...")
    app = ClimbingApp()
    sys.exit(app.run())




