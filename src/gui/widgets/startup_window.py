import shutil
from pathlib import Path
from src.utils.config import ProjectConfig
from src.utils.logger import setup_logger

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox

logger = setup_logger("gui/startup_window", ProjectConfig.get_log_file("gui"))


class StartupWindow(QMainWindow):
    """
    Initial window for the Climbing Route Creator application.
    """
    image_uploaded = pyqtSignal(str)  # Signal to indicate that an image has been uploaded

    def __init__(self):
        """
        Initializes the startup window.
        """
        super().__init__()
        self.setWindowTitle("Climbing Route Creator")
        self.resize(1200, 1300)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(20)  # Add spacing between elements
        layout.setContentsMargins(40, 40, 40, 40)  # Top, left, bottom, right

        # Logo / Title
        title = QLabel("Climbing Route Creator")
        title.setFont(QFont("Arial", 34, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel("Create, share and discover climbing routes")
        subtitle.setFont(QFont("Arial", 16))
        subtitle.setAlignment(Qt.AlignCenter)

        layout.addStretch()  # Add stretchable space

        # Upload button
        self.upload_btn = QPushButton("Upload Wall Image")
        self.upload_btn.setFont(QFont("Arial", 16))
        self.upload_btn.clicked.connect(self.upload_image)
        layout.addWidget(self.upload_btn)

        layout.addStretch()

        # Style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QPushButton {
                background-color: #2196F3;
                color: white;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)

    def upload_image(self):
        """Opens a file dialog to upload an image and emits the image path."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Wall Image",  # Dialog title
            "",  # Default directory
            "Image files (*.jpg *.png *.jpeg)"  # File filter
        )

        if file_path:
            try:
                logger.info(f"Uploading image: {file_path}")
                validated_path = ProjectConfig.validate_image_path(file_path)
                logger.info(f"Validated image path: {validated_path}")
                destination = ProjectConfig.IMAGES_DIR / validated_path.name  # Copy the image to the project directory
                logger.info(f"Copying image to: {destination}")
                shutil.copy2(validated_path, destination)  # Copy the image to the project directory
                logger.info(f"Image uploaded successfully: {destination}")
                self.image_uploaded.emit(str(destination))  # Emit signal with the image path
            except ValueError as e:
                logger.error(f"Error uploading image: {str(e)}")
                QMessageBox.warning(self, "Error", str(e))
