from datetime import datetime

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QLabel, QComboBox
from src.utils.logger import setup_logger
from src.utils.config import ProjectConfig

logger = setup_logger("gui/widgets/route_info_panel", ProjectConfig.get_log_file("gui/widgets/route_info_panel"))


class RouteInfoPanel(QWidget):
    """
    Widget for displaying the information about the route.

    Includes fields for:
    1. Name of the route
    2. Grade of the route
    3. Author of the route
    4. Date of creation / date of sending it

    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)

        # Name of the route
        self.route_name = QLineEdit()
        self.route_name.setPlaceholderText("Route name")
        logger.debug("Route name input field created.")

        # Grade label
        self.grade_label = QLabel("Grade:")
        self.grade_selector = QComboBox()
        logger.debug("Grade combobox created.")

        # Author
        self.author = QLineEdit()
        self.author.setPlaceholderText("Author")
        logger.debug("Author input field created.")

        # Date of creation / date of sending it
        self.date_label = QLabel(f"Date: {datetime.now().strftime('%Y-%m-%d')}")
        logger.debug("Date label created.")

        layout.addWidget(self.route_name)
        layout.addWidget(self.grade_label)
        layout.addWidget(self.grade_selector)
        layout.addWidget(self.author)
        layout.addWidget(self.date_label)
