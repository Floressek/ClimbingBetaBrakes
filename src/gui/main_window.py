# src/gui/main_window.py
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt
from .widgets.hold_viewer import HoldViewer
from .widgets.route_toolbar import RouteToolbar
from src.utils.logger import setup_logger
from src.utils.config import ProjectConfig
from src.core.movement_type import HoldType

logger = setup_logger("gui/main_window", ProjectConfig.get_log_file("gui"))


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

        # Ustawienia po utworzeniu hold_viewer
        self.hold_viewer.setAttribute(Qt.WA_OpaquePaintEvent)
        self.hold_viewer.setAttribute(Qt.WA_NoSystemBackground)

        main_layout.addWidget(self.hold_viewer, 1)
        # Initialize application state
        self.initialize_state()


    def initialize_state(self):
        """Initializes application state and connects signals to slots."""
        self.route_toolbar.new_route_button.clicked.connect(self.start_new_route)
        self.route_toolbar.save_route_button.clicked.connect(self.save_current_route)

        self.route_toolbar.hands_button.clicked.connect(lambda: self._set_hold_type(HoldType.HAND))
        self.route_toolbar.feet_button.clicked.connect(lambda: self._set_hold_type(HoldType.FEET))
        # self.route_toolbar.show_numbers.clicked.connect(self._toggle_numbers)
        # self.route_toolbar.edit_arrows.clicked.connect(self._toggle_arrows)

    def start_new_route(self):
        """Starts creating a new route."""
        self.logger.info("Starting new route creation")
        # Reset hold selection
        for hold in self.hold_viewer.holds:
            hold.is_hand_selected = False
            hold.is_foot_selected = False
            hold.hand_order = None
            hold.foot_order = None
            # hold.is_selected = False
            # hold.order_in_route = None
        self.hold_viewer.next_hand_order = 0
        self.hold_viewer.next_foot_order = 0
        self.hold_viewer.update()
        self.route_toolbar.enable_route_editing()

    def save_current_route(self):
        """Saves the currently created route."""
        self.logger.info("Saving current route")
        # TODO: Implement route saving functionality
        # selected_holds = [h for h in self.hold_viewer.holds if h.is_selected]
        hand_holds = [h for h in self.hold_viewer.holds if h.is_hand_selected]
        foot_holds = [h for h in self.hold_viewer.holds if h.is_foot_selected]
        if hand_holds or foot_holds:
            self.logger.info(f"Route has {len(hand_holds)} hand holds and {len(foot_holds)} foot holds")

    def _set_hold_type(self, hold_type: HoldType):
        self.hold_viewer.current_hold_type = hold_type
        logger.info(f"Set hold type to {hold_type.value}")

    def _toggle_numbers(self):
        self.hold_viewer.show_numbers = self.route_toolbar.show_numbers.isChecked()
        self.hold_viewer.update()

    def _toggle_arrows(self):
        self.hold_viewer.edit_arrows = self.route_toolbar.edit_arrows.isChecked()
        self.hold_viewer.update()


