# src/gui/main_window.py
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt
from .widgets.hold_viewer import HoldViewer
from .widgets.route_toolbar import RouteToolbar
from src.utils.logger import setup_logger
from src.utils.config import ProjectConfig


class MainWindow(QMainWindow):
    """
    Main window of the Climbing Route Creator application.
    Integrates all GUI components and manages interactions between them.
    """

    def __init__(self):
        super().__init__()
        self.logger = setup_logger("gui", ProjectConfig.get_log_file("gui"))
        self.logger.info("Initializing main application window")

        # Ustawiamy tytuł i domyślny rozmiar okna
        self.setWindowTitle("Climbing Route Creator")
        self.resize(1024, 768)  # Dodajemy domyślny rozmiar
        self.setup_ui()

        self.hold_viewer.setAttribute(Qt.WA_OpaquePaintEvent)
        self.hold_viewer.setAttribute(Qt.WA_NoSystemBackground)

    def setup_ui(self):
        """
        Configures the user interface layout.
        Main window is divided into:
        1. Top toolbar with action buttons
        2. Main area displaying the climbing wall with holds
        """
        # Create main widget and layouts
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Add the route toolbar
        self.route_toolbar = RouteToolbar(self)
        main_layout.addWidget(self.route_toolbar)

        # Add the main hold viewer widget
        self.hold_viewer = HoldViewer(self)
        self.hold_viewer.setMinimumSize(1200, 1300)
        main_layout.addWidget(self.hold_viewer, 1)

        # Initialize application state
        self.initialize_state()

    def initialize_state(self):
        """Initializes application state and connects signals to slots."""
        self.route_toolbar.new_route_button.clicked.connect(self.start_new_route)
        self.route_toolbar.save_route_button.clicked.connect(self.save_current_route)

    def start_new_route(self):
        """Starts creating a new route."""
        self.logger.info("Starting new route creation")
        # Reset hold selection
        for hold in self.hold_viewer.holds:
            hold.is_selected = False
            hold.order_in_route = None
        self.hold_viewer.next_hold_order = 0
        self.hold_viewer.update()
        self.route_toolbar.enable_route_editing()

    def save_current_route(self):
        """Saves the currently created route."""
        self.logger.info("Saving current route")
        # TODO: Implement route saving functionality
        selected_holds = [h for h in self.hold_viewer.holds if h.is_selected]
        if selected_holds:
            self.logger.info(f"Route has {len(selected_holds)} holds")