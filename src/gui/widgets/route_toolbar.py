from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt

class RouteToolbar(QWidget):
    """
    Widget for displaying the toolbar for creating routes.

    Includes buttons for:
    1. Creating a new route
    2. Saving the current route
    3. Saving grade for the route
    4. Adding comments
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self) -> None:
        """
        Set up the user interface for the toolbar.
        """
        layout = QHBoxLayout(self)

        # Create a action buttons
        self.new_route_button = QPushButton("New Route")
        self.save_route_button = QPushButton("Save Route")
        self.save_route_button.setEnabled(False) # Disable the button initially

        # Adding new elements to the layout
        layout.addWidget(self.new_route_button)
        layout.addWidget(self.save_route_button)
        layout.addStretch() # Elastic spacer to push the next elements to the right

    def enable_route_editing(self):
        """
        Enable the route editing functionality.
        """
        self.save_route_button.setEnabled(True)