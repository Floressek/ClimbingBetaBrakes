# import shutil
# from pathlib import Path
# from src.utils.config import ProjectConfig
# from src.utils.logger import setup_logger
#
# from PyQt5.QtCore import pyqtSignal, Qt
# from PyQt5.QtGui import QFont
# from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox
#
# logger = setup_logger("gui/startup_window", ProjectConfig.get_log_file("gui"))
#
#
# class StartupWindow(QMainWindow):
#     """
#     Initial window for the Climbing Route Creator application.
#     """
#     image_uploaded = pyqtSignal(str)  # Signal to indicate that an image has been uploaded
#
#     def __init__(self):
#         """
#         Initializes the startup window.
#         """
#         super().__init__()
#         self.setWindowTitle("Climbing Route Creator")
#         self.resize(1200, 1300)
#
#         main_widget = QWidget()
#         self.setCentralWidget(main_widget)
#         layout = QVBoxLayout(main_widget)
#         layout.setSpacing(20)  # Add spacing between elements
#         layout.setContentsMargins(40, 40, 40, 40)  # Top, left, bottom, right
#
#         # Logo / Title
#         title = QLabel("Climbing Route Creator")
#         title.setFont(QFont("Arial", 34, QFont.Bold))
#         title.setAlignment(Qt.AlignCenter)
#         layout.addWidget(title)
#
#         subtitle = QLabel("Create, share and discover climbing routes")
#         subtitle.setFont(QFont("Arial", 16))
#         subtitle.setAlignment(Qt.AlignCenter)
#
#         layout.addStretch()  # Add stretchable space
#
#         # Upload button
#         self.upload_btn = QPushButton("Upload Wall Image")
#         self.upload_btn.setFont(QFont("Arial", 16))
#         self.upload_btn.clicked.connect(self.upload_image)
#         layout.addWidget(self.upload_btn)
#
#         layout.addStretch()
#
#         # Style
#         self.setStyleSheet("""
#             QMainWindow {
#                 background-color: #f0f0f0;
#             }
#             QPushButton {
#                 background-color: #2196F3;
#                 color: white;
#                 border-radius: 5px;
#                 padding: 10px;
#             }
#             QPushButton:hover {
#                 background-color: #1976D2;
#             }
#         """)
#
#     def upload_image(self):
#         """Opens a file dialog to upload an image and emits the image path."""
#         file_path, _ = QFileDialog.getOpenFileName(
#             self,
#             "Select Wall Image",  # Dialog title
#             "",  # Default directory
#             "Image files (*.jpg *.png *.jpeg)"  # File filter
#         )
#
#         if file_path:
#             try:
#                 logger.info(f"Uploading image: {file_path}")
#                 validated_path = ProjectConfig.validate_image_path(file_path)
#                 logger.info(f"Validated image path: {validated_path}")
#                 destination = ProjectConfig.IMAGES_DIR / validated_path.name  # Copy the image to the project directory
#                 logger.info(f"Copying image to: {destination}")
#                 shutil.copy2(validated_path, destination)  # Copy the image to the project directory
#                 logger.info(f"Image uploaded successfully: {destination}")
#                 self.image_uploaded.emit(str(destination))  # Emit signal with the image path
#             except ValueError as e:
#                 logger.error(f"Error uploading image: {str(e)}")
#                 QMessageBox.warning(self, "Error", str(e))

import shutil
from pathlib import Path

try:
    from PyQt5.QtCore import pyqtSignal, Qt, QUrl
    from PyQt5.QtGui import QFont, QDragEnterEvent, QDropEvent
    from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox, QHBoxLayout
    from PyQt5.QtGui import QDesktopServices
except ModuleNotFoundError as e:
    print("PyQt5 module is not installed. Please install it using 'pip install PyQt5' and try again.")
    raise e

from src.utils.config import ProjectConfig
from src.utils.logger import setup_logger

logger = setup_logger("gui/startup_window", ProjectConfig.get_log_file("gui"))


class StartupWindow(QMainWindow):
    """
    Enhanced Startup Window for the Climbing Route Creator application.
    Includes drag-and-drop functionality and improved UI.
    """
    image_uploaded = pyqtSignal(str)  # Signal to indicate that an image has been uploaded

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Climbing Route Creator")
        self.resize(1200, 800)
        self.setAcceptDrops(True)  # Enable drag-and-drop

        self.dark_mode = False  # State for dark mode

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        # Title
        title = QLabel("Climbing Route Creator")
        title.setFont(QFont("Arial", 34, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel("Create, share and discover climbing routes")
        subtitle.setFont(QFont("Arial", 16))
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)

        layout.addStretch()

        # Upload button
        self.upload_btn = QPushButton("Upload Wall Image")
        self.upload_btn.setFont(QFont("Arial", 16))
        self.upload_btn.clicked.connect(self.upload_image)
        layout.addWidget(self.upload_btn, alignment=Qt.AlignCenter)

        # Drop area
        self.drop_label = QLabel("Drag and drop your image here")
        self.drop_label.setFont(QFont("Arial", 14))
        self.drop_label.setAlignment(Qt.AlignCenter)
        self.drop_label.setStyleSheet("""
            color: #666;
            border: 2px dashed #aaa;
            padding: 20px;
            border-radius: 10px;
        """)
        layout.addWidget(self.drop_label)

        layout.addStretch()

        # Bottom buttons
        bottom_layout = QHBoxLayout()
        layout.addLayout(bottom_layout)

        self.doc_btn = QPushButton("Open Documentation")
        self.doc_btn.setFont(QFont("Arial", 12))
        self.doc_btn.clicked.connect(self.open_documentation)
        bottom_layout.addWidget(self.doc_btn, alignment=Qt.AlignLeft)

        self.theme_btn = QPushButton("Toggle Dark Mode")
        self.theme_btn.setFont(QFont("Arial", 12))
        self.theme_btn.clicked.connect(self.toggle_theme)
        bottom_layout.addWidget(self.theme_btn, alignment=Qt.AlignRight)

        self.set_light_theme()

    def upload_image(self):
        """Opens a file dialog to upload an image and emits the image path."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Wall Image",  # Dialog title
            "",  # Default directory
            "Image files (*.jpg *.png *.jpeg)"  # File filter
        )

        if file_path:
            self._process_uploaded_file(file_path)

    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handles drag enter events."""
        if event.mimeData().hasUrls():
            self.drop_label.setStyleSheet("color: #2196F3; border: 2px solid #2196F3; background-color: #e3f2fd; padding: 20px; border-radius: 10px;")
            event.accept()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        """Handles drag leave events."""
        self.drop_label.setStyleSheet("color: #666; border: 2px dashed #aaa; padding: 20px; border-radius: 10px;")

    def dropEvent(self, event: QDropEvent):
        """Handles file drop events."""
        self.drop_label.setStyleSheet("color: #666; border: 2px dashed #aaa; padding: 20px; border-radius: 10px;")
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            self._process_uploaded_file(file_path)

    def _process_uploaded_file(self, file_path: str):
        """Validates and processes the uploaded file."""
        try:
            logger.info(f"Uploading image: {file_path}")
            validated_path = ProjectConfig.validate_image_path(file_path)
            destination = ProjectConfig.IMAGES_DIR / validated_path.name
            shutil.copy2(validated_path, destination)  # Copy the image to the project directory
            logger.info(f"Image uploaded successfully: {destination}")
            self.image_uploaded.emit(str(destination))
        except ValueError as e:
            logger.error(f"Error uploading image: {str(e)}")
            QMessageBox.warning(self, "Error", str(e))

    def toggle_theme(self):
        """Toggles between light and dark mode."""
        if self.dark_mode:
            self.set_light_theme()
        else:
            self.set_dark_theme()
        self.dark_mode = not self.dark_mode

    def set_light_theme(self):
        """Sets the light theme."""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
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
            QLabel {
                color: #333;
            }
        """)

    def set_dark_theme(self):
        """Sets the dark theme."""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #333;
            }
            QPushButton {
                background-color: #555;
                color: white;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #777;
            }
            QLabel {
                color: #eee;
            }
        """)

    def open_documentation(self):
        """Opens the documentation in a web browser."""
        QMessageBox.information(self, "Documentation", "Opening the user documentation...")
        QDesktopServices.openUrl(QUrl("https://github.com/Floressek/ClimbingBetaBrakes"))


