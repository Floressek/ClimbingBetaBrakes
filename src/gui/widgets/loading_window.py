from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMovie, QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

from src.utils.config import ProjectConfig
from src.utils.logger import setup_logger

logger = setup_logger("gui/loading_window", ProjectConfig.get_log_file("gui"))


class LoadingWindow(QWidget):
    """
    Loading window that is displayed while the application is starting up.
    """

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)

        layout = QVBoxLayout(self)

        # Używamy pełnej ścieżki do GIFa
        gif_path = str(ProjectConfig.PROJECT_ROOT / "src" / "gui" / "resources" / "loading.gif")
        if not gif_path:
            logger.error(f"GIF not found at: {gif_path}")
            raise FileNotFoundError(f"GIF not found at: {gif_path}")

        self.spinner_label = QLabel()
        self.movie = QMovie(gif_path)
        self.update()
        self.movie.start()
        self.update()
        self.spinner_label.setMovie(self.movie)
        layout.addWidget(self.spinner_label)

        self.loading_label = QLabel("Detecting holds...")
        layout.addWidget(self.loading_label)
        self.loading_label.setFont(QFont("Segoe UI", 16))
        layout.addWidget(self.loading_label, alignment=Qt.AlignCenter)

        self.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 10px;
            }
        """)

    def start_animation(self):
        self.movie.start()

    def stop_animation(self):
        self.movie.stop()
