from dataclasses import asdict
from pathlib import Path
from typing import List
from roboflow import Roboflow
import supervision as sv
import cv2
import numpy as np

from src.utils.config import ProjectConfig, RoboflowConfig
from src.utils.logger import setup_logger


class RoboflowClient:
    """
    Client for Roboflow API.

    Note:
        detecting holds (coordinates on the picture) on climbing routes.
    """

    def __init__(self, config: RoboflowConfig):
        """
        Initialize the Roboflow client.

        Args:
            config (RoboflowConfig): Configuration for the Roboflow API
        """

        # Set up logger
        self.logger = setup_logger("roboflow_client", ProjectConfig.get_log_file("roboflow"))
        self.logger.info("Initializing Roboflow client...")

        self.rf = Roboflow(api_key=config.api_key)  # Create Roboflow object
        self.project = self.rf.workspace().project(config.project_id)
        self.model = self.project.version(config.model_version_id).model
        self.config = config

        self.logger.info(f"Roboflow client initialized for the project: {config.project_id}")

    def detect_holds(self, image_path: Path) -> dict:
        """
        Detect holds on the climbing route image.

        Args:
            image_path (Path): Path to the image with the climbing route

        Returns:
            dict: Detected holds with their coordinates (API response)
        """
        self.logger.info(f"Detecting holds on the image: {image_path}")

        result = self.model.predict(
            str(image_path),
            confidence=self.config.confidence_threshold,
            # overlap=self.config.overlap_threshold # idk whether to leave this or not
        ).json()

        self.logger.info(f"Detected {len(result['predictions'])} holds on the image.")
        return result

    # def visualize_detections(self, image_path: Path, result: dict, output_path: Path) -> None:
    #     """
    #     Visualize the detected holds on the climbing route image.
    #
    #     Args:
    #         image_path (Path): Path to the image with the climbing route
    #         result (dict): Detected holds with their coordinates (API response)
    #         output_path (Path): Path to save the output image
    #     """
    #     self.logger.info(f"Visualizing detected holds on the image: {image_path}")
    #
    #     image = cv2.imread(str(image_path))
    #     detections = sv.Detections.from_inference(result) # yep the from_inference method works
    #
    #     # Annotators for labels and masks
    #     label_annotator = sv.LabelAnnotator()
    #     mask_annotator = sv.MaskAnnotator()
    #
    #     # Overlaping labels and masks on the image
    #     annotated_image = mask_annotator.annotate(scene=image, detections=detections)
    #     # labels = ["hold"] * len(result["predictions"])
    #     labels = [f"hold {i+1}" for i in range(len(result["predictions"]))] # numerated version of the labels
    #     annotated_image = label_annotator.annotate(
    #         scene=annotated_image,
    #         labels=labels,
    #         detections=detections
    #     )
    #
    #     # Save the output image
    #     cv2.imwrite(str(output_path), annotated_image)
    def visualize_detections(self, image_path: Path, result: dict, output_path: Path) -> None:
        """
        Visualize the detected holds on the climbing route image.

        Args:
             image_path (Path): Path to the image with the climbing route
             result (dict): Detected holds with their coordinates (API response)
             output_path (Path): Path to save the output image
        """
        image = cv2.imread(str(image_path))

        for pred in result['predictions']:
            # Makes a list of points from the prediction
            points = np.array([[p['x'], p['y']] for p in pred['points']], np.int32)
            points = points.reshape((-1, 1, 2))  # Reshape points to fit cv2.polylines

            # Draw the contour
            cv2.polylines(image, [points], True, (0, 255, 0), 2)

            # Add text with confidence
            cv2.putText(image,
                        f"hold {result['predictions'].index(pred) + 1}: {pred['confidence']:.2f}",
                        (int(pred['x']), int(pred['y'])),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (255, 255, 255),
                        2)

        cv2.imwrite(str(output_path), image)
        self.logger.info(f"Visualized image saved to: {output_path}")
