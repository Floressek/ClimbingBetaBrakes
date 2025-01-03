from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QButtonGroup, QComboBox, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt


class RouteToolbar(QWidget):
    """
    Widget for displaying the toolbar for creating routes.

    Includes buttons for:
    1. Creating a new route
    2. Saving the current route
    3. Switching between hands and feet modes
    4. Editing route properties like arrows and grades
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self) -> None:
        """
        Set up the user interface for the toolbar with even alignment.
        """
        # Main layout
        layout = QHBoxLayout(self)
        layout.setSpacing(10)  # Add spacing between elements
        layout.setContentsMargins(15, 15, 15, 15)

        # Section 1: Route controls
        self.new_route_button = QPushButton("New Route")
        self.save_route_button = QPushButton("Save Route")
        self.save_route_button.setEnabled(False)  # Initially disabled
        layout.addWidget(self.new_route_button)
        layout.addWidget(self.save_route_button)

        # Vertical divider (spacer to ensure equal spacing)
        layout.addSpacerItem(QSpacerItem(20, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Section 2: Mode selection (hands/feet)
        mode_group = QButtonGroup(self)
        self.hands_button = QPushButton("Hand")
        self.hands_button.setCheckable(True)
        self.feet_button = QPushButton("Feet")
        self.feet_button.setCheckable(True)
        mode_group.addButton(self.hands_button)
        mode_group.addButton(self.feet_button)
        self.hands_button.setChecked(True)  # Default to hands mode

        # Add mode buttons in a neat row
        layout.addWidget(self.hands_button)
        layout.addWidget(self.feet_button)

        # Vertical divider (spacer to ensure equal spacing)
        layout.addSpacerItem(QSpacerItem(20, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Section 3: Editing options
        self.show_numbers = QPushButton("Show Numbers")
        self.show_numbers.setCheckable(True)
        self.edit_arrows = QPushButton("Edit Arrows")
        self.edit_arrows.setCheckable(True)
        layout.addWidget(self.show_numbers)
        layout.addWidget(self.edit_arrows)

        # Vertical divider (spacer to ensure equal spacing)
        layout.addSpacerItem(QSpacerItem(20, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Section 4: Grade selector
        self.grade_selector = QComboBox()
        self.grade_selector.addItems(["4a", "4b", "4c", "5a", "5b", "5c", "6a", "6a+", "6b", "6b+", "6c", "6c+", "7a"])
        layout.addWidget(QLabel("Route Grade:"))
        layout.addWidget(self.grade_selector)

        # Final stretchable spacer to align everything to the left
        layout.addStretch()

        # Styling for consistency
        self.setStyleSheet("""
            QPushButton {
                padding: 5px 10px;
                font-size: 14px;
            }
            QLabel {
                font-weight: bold;
                font-size: 14px;
            }
            QComboBox {
                font-size: 14px;
                padding: 5px;
            }
        """)

    def enable_route_editing(self):
        """
        Enable the route editing functionality.
        """
        self.save_route_button.setEnabled(True)
