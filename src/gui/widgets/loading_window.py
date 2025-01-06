from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

from src.utils.config import ProjectConfig
from src.utils.logger import setup_logger

setup_logger("gui/loading_window", ProjectConfig.get_log_file("gui"))


class LoadingWindow(QWidget):
    """
    Loading window that is displayed while the application is starting up.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Loading...") # FIXME if gif with text is used, remove this line
        self.resize(300, 200)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)  # Remove window frame

        layout = QVBoxLayout(self) # layout for the window

        # Loading spinner
        self.spinner_label = QLabel() # Qlabel(self) consider
        self.movie = QMovie("src/gui/resources/loading.gif") # loading gif change to ProjectConfig.get_loading_gif() later
        self.spinner_label.setMovie(self.movie)
        layout.addWidget(self.spinner_label, alignment=Qt.AlignCenter)

        # Loading text
        self.loading_label = QLabel("Detecting holds...") # text to be displayed
        self.loading_label.setStyleSheet("font-size: 16px;") # style for the text
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