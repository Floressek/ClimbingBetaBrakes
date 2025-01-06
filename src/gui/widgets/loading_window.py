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
# from PyQt5.QtGui import QFont
# from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
# from PyQt5.QtCore import Qt, QTimer
#
# class LoadingWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
#         self.resize(400, 200)
#
#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(20, 20, 20, 20)
#
#         self.progress = QProgressBar()
#         self.progress.setTextVisible(False)
#         self.progress.setStyleSheet("""
#             QProgressBar {
#                 border: none;
#                 background-color: #e9ecef;
#                 border-radius: 10px;
#                 height: 8px;
#             }
#             QProgressBar::chunk {
#                 background-color: #2196F3;
#                 border-radius: 10px;
#             }
#         """)
#
#         self.text = QLabel("Detecting holds...")
#         self.text.setFont(QFont("Segoe UI", 16))
#         self.text.setAlignment(Qt.AlignCenter)
#
#         layout.addWidget(self.text)
#         layout.addWidget(self.progress)
#
#         self.setStyleSheet("""
#             QWidget {
#                 background-color: rgb(248, 249, 250);
#                 border: 1px solid #e9ecef;
#                 border-radius: 12px;
#             }
#             QLabel { color: #495057; }
#         """)
#
#         self.timer = QTimer()
#         self.timer.timeout.connect(self.updateProgress)
#         self.timer.start(30)
#         self.progress_value = 0
#
#     def updateProgress(self):
#         self.progress_value = (self.progress_value + 1) % 100
#         self.progress.setValue(self.progress_value)