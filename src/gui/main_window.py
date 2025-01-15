# from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout
# from PyQt5.QtCore import Qt
# from .widgets.hold_viewer import HoldViewer
# from .widgets.route_toolbar import RouteToolbar
# from src.utils.logger import setup_logger
# from src.utils.config import ProjectConfig
# from src.core.movement_type import HoldType
#
# logger = setup_logger("gui/main_window", ProjectConfig.get_log_file("gui"))
#
#
# class MainWindow(QMainWindow):
#     """
#     Main window of the Climbing Route Creator application.
#     Integrates all GUI components and manages interactions between them.
#     """
#
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Climbing Route Creator")
#         self.resize(1024, 768)
#         self.setup_ui()
#         self.setAttribute(Qt.WA_DeleteOnClose)
#
#     def setup_ui(self):
#         main_widget = QWidget()
#         self.setCentralWidget(main_widget)
#         layout = QVBoxLayout(main_widget)
#         self.resize(1200, 1300)
#         layout.setContentsMargins(10, 10, 10, 10)
#
#         self.route_toolbar = RouteToolbar(self)
#         self.hold_viewer = HoldViewer(self)
#
#         layout.addWidget(self.route_toolbar)
#         layout.addWidget(self.hold_viewer, 1)
#
#         self.initialize_state()
#
#     def initialize_state(self):
#         self.route_toolbar.new_route_button.clicked.connect(self.start_new_route)
#         self.route_toolbar.save_route_button.clicked.connect(self.save_current_route)
#         self.route_toolbar.hands_button.clicked.connect(lambda: self._set_hold_type(HoldType.HAND))
#         self.route_toolbar.feet_button.clicked.connect(lambda: self._set_hold_type(HoldType.FEET))
#         self.route_toolbar.curve_edit_button.clicked.connect(
#             lambda checked: self.hold_viewer._set_mode("curve_edit" if checked else "normal")
#         )
#
#     def start_new_route(self):
#         """Starts creating a new route."""
#         logger.info("Starting new route creation")
#         # Reset hold selection
#         for hold in self.hold_viewer.holds:
#             hold.is_hand_selected = False
#             hold.is_foot_selected = False
#             hold.hand_order = None
#             hold.foot_order = None
#             # hold.is_selected = False
#             # hold.order_in_route = None
#         self.hold_viewer.next_hand_order = 0
#         self.hold_viewer.next_foot_order = 0
#         self.hold_viewer.update()
#         self.route_toolbar.enable_route_editing()
#
#     def save_current_route(self):
#         """Saves the currently created route."""
#         logger.info("Saving current route")
#         # TODO: Implement route saving functionality
#         # selected_holds = [h for h in self.hold_viewer.holds if h.is_selected]
#         hand_holds = [h for h in self.hold_viewer.holds if h.is_hand_selected]
#         foot_holds = [h for h in self.hold_viewer.holds if h.is_foot_selected]
#         if hand_holds or foot_holds:
#             logger.info(f"Route has {len(hand_holds)} hand holds and {len(foot_holds)} foot holds")
#
#     def _set_hold_type(self, hold_type: HoldType):
#         self.hold_viewer.current_hold_type = hold_type
#         logger.info(f"Set hold type to {hold_type.value}")
from pathlib import Path

from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QMessageBox, QDialog
from PyQt5.QtCore import Qt
from datetime import datetime
import os
import uuid

from .widgets.hold_viewer import HoldViewer
from .widgets.route_toolbar import RouteToolbar
from .widgets.route_info_dialog import RouteInfoDialog
from src.utils.logger import setup_logger
from src.utils.config import ProjectConfig
from src.core.movement_type import HoldType
from src.utils.route_image_processor import RouteImageProcessor
from src.storage.repositories.route_repository import RouteRepository
from src.storage.models.route_model import RouteModel

logger = setup_logger("gui/main_window", ProjectConfig.get_log_file("gui"))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Climbing Route Creator")
        self.resize(1024, 768)
        self.setup_ui()
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.route_image_processor = RouteImageProcessor()
        self.current_image_path = None

        # Initialize route repository
        self.route_repository = RouteRepository(ProjectConfig.ROUTES_DIR)

    def setup_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        self.resize(1200, 1300)
        layout.setContentsMargins(10, 10, 10, 10)

        self.route_toolbar = RouteToolbar(self)
        self.hold_viewer = HoldViewer(self)

        layout.addWidget(self.route_toolbar)
        layout.addWidget(self.hold_viewer, 1)

        self.initialize_state()

    def initialize_state(self):
        self.route_toolbar.new_route_button.clicked.connect(self.start_new_route)
        self.route_toolbar.save_route_button.clicked.connect(self.show_save_dialog)
        self.route_toolbar.hands_button.clicked.connect(lambda: self._set_hold_type(HoldType.HAND))
        self.route_toolbar.feet_button.clicked.connect(lambda: self._set_hold_type(HoldType.FEET))
        self.route_toolbar.curve_edit_button.clicked.connect(
            lambda checked: self.hold_viewer._set_mode("curve_edit" if checked else "normal")
        )

    def _set_hold_type(self, hold_type):
        self.hold_viewer.current_hold_type = hold_type

    def start_new_route(self):
        """Starts creating a new route."""
        logger.info("Starting new route creation")
        for hold in self.hold_viewer.holds:
            hold.is_hand_selected = False
            hold.is_foot_selected = False
            hold.hand_order = None
            hold.foot_order = None
        self.hold_viewer.next_hand_order = 0
        self.hold_viewer.next_foot_order = 0
        self.hold_viewer.update()
        self.route_toolbar.enable_route_editing()

    def show_save_dialog(self):
        """Show dialog for entering route information"""
        dialog = RouteInfoDialog(self, self.route_toolbar.grade_selector.currentText())
        if dialog.exec_() == QDialog.Accepted:
            self.save_current_route(dialog.get_route_info())

    def save_current_route(self, route_info):
        """Save the current route with provided information"""
        try:

            # Check if an image is loaded
            if self.current_image_path is None:
                raise ValueError("No image loaded")
            image_path = Path(self.current_image_path) # if exists
            if not image_path.exists():
                raise FileNotFoundError(f"Image file not found: {image_path}")

            # Get selected holds
            hand_holds = [h for h in self.hold_viewer.holds if h.is_hand_selected]
            foot_holds = [h for h in self.hold_viewer.holds if h.is_foot_selected]

            if not (hand_holds or foot_holds):
                QMessageBox.warning(self, "Warning", "No holds selected for the route.")
                return

            # Generate UUIDs for holds that don't have them
            hold_ids = []
            for hold in hand_holds + foot_holds:
                if not hasattr(hold, 'id'):
                    hold.id = uuid.uuid4()
                hold_ids.append(hold.id)

            # Create route model
            route = RouteModel.create(
                name=route_info["name"],
                hold_ids=hold_ids,
                difficulty=route_info["grade"],
                description=route_info["description"],
                author=route_info["author"]
            )

            # Save route to repository
            self.route_repository.save(route)

            # Create exports directory if it doesn't exist
            exports_dir = ProjectConfig.EXPORTS_DIR
            os.makedirs(exports_dir, exist_ok=True)

            # Generate filename based on route name and ID
            safe_name = "".join(x for x in route.name if x.isalnum() or x in (' ', '-', '_')).strip()
            output_filename = f"{safe_name}_{str(route.id)[:8]}.jpg"
            output_path = os.path.join(exports_dir, output_filename)

            logger.debug(f"Current image path: {self.current_image_path}")
            logger.debug(f"Output path: {output_path}")
            logger.debug(f"Route info: {route_info}")

            input_image_path = str(self.current_image_path)

            # Save image with overlay
            # self.route_image_processor.add_route_info_overlay(
            #     input_image_path,
            #     {
            #         "name": route.name,
            #         "author": route.author,
            #         "grade": route.difficulty,
            #         "description": route.description
            #     },
            #     str(output_path),
            #     hand_holds=hand_holds,  # selected holds
            #     foot_holds=foot_holds # selected holds
            # )

            # Approach with passing the whole widget and selected holds
            self.route_image_processor.add_route_info_overlay(
                self.hold_viewer,  # whole widget
                route_info,
                output_path
            )

            logger.info(f"Route saved successfully to {output_path}")
            QMessageBox.information(
                self,
                "Success",
                f"Route saved successfully!\n\nRoute ID: {route.id}\nImage: {output_path}"
            )

        except Exception as e:
            logger.error(f"Error saving route: {str(e)}")
            logger.exception("Detailed error info:")
            QMessageBox.critical(self, "Error", f"Failed to save route:\n{str(e)}")

    def load_route(self, route_id: str):
        """Load a route from the repository"""
        try:
            route = self.route_repository.get(route_id)
            if route:
                # Clear current selection
                self.start_new_route()

                # Find and select holds
                for hold in self.hold_viewer.holds:
                    if hasattr(hold, 'id') and hold.id in route.hold_ids:
                        # You might need additional logic here to determine if it's a hand or foot hold
                        hold.is_hand_selected = True  # or is_foot_selected depending on your needs

                # Update the toolbar grade
                self.route_toolbar.grade_selector.setCurrentText(route.difficulty)

                self.hold_viewer.update()
                logger.info(f"Route {route_id} loaded successfully")
            else:
                logger.warning(f"Route {route_id} not found")
                QMessageBox.warning(self, "Warning", f"Route {route_id} not found")

        except Exception as e:
            logger.error(f"Error loading route: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to load route:\n{str(e)}")
