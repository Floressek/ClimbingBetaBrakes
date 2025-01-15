from PyQt5.QtCore import QThread, pyqtSignal
from src.core.hold import Hold
from src.utils.logger import setup_logger
from src.utils.config import ProjectConfig

logger = setup_logger("detection_worker", ProjectConfig.get_log_file("detection"))


class DetectionWorker(QThread):
    """
    Worker class for detecting holds on climbing routes.
    Allows for running the detection process in a separate thread.
    """

    detection_completed = pyqtSignal(list)  # when detection is completed
    error_occurred = pyqtSignal(str)  # if smth goes wrong

    def __init__(self, roboflow_client, image_path: str):
        super().__init__()
        self.roboflow_client = roboflow_client
        self.image_path = image_path

    def run(self):
        """
        Main worker method.
        :return:
        """
        try:
            logger.info(f"Starting hold detection for image {self.image_path}")

            detection_result = self.roboflow_client.detect_holds(self.image_path)

            holds = []
            for prediction in detection_result['predictions']:
                hold = Hold.from_detection(prediction)
                holds.append(hold)

            logger.info(f"Detected {len(holds)} holds in image {self.image_path}")
            self.detection_completed.emit(holds)

        except Exception as e:
            logger.error(f"Error during hold detection: {str(e)}")
            self.error_occurred.emit(str(e))
