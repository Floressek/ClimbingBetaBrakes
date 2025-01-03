from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QPoint
from typing import List, Optional
from src.core.hold import Hold


class HoldViewer(QWidget):
    """
    Widget for displaying pictures of climbing walls and that allows to interact with them.

    Responsible for:
    1. Displaying the image of a climbing wall
    2. Drawing detected holds on the image
    3. Highlighting holds on the image when selected
    4. Displaying the currently crated route on the image
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)  # Why super because it is a subclass of QWidget
        self.holds: List[Hold] = []
        self.next_hold_order = 0  # Counter for the order of the next hold in the route
        self.setMouseTracking(True)

    def paintEvent(self, event) -> None:
        """
        Draws the image and the holds on the widget.
        Method called by the Qt framework whenever the widget needs to be redrawn.
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw the image
        for hold in self.holds:
            self.draw_hold(painter, hold)

        # Draw the selected hold
        selected_holds = [h for h in self.holds if h.is_selected]
        selected_holds.sort(key=lambda h: h.order_in_route)
        if len(selected_holds) > 1:
            self.draw_route_connections(painter)

    def draw_hold(self, painter: QPainter, hold: Hold) -> None:
        """
        Draws a single hold on the widget.
        """
        # Set the color based on whether the hold is selected
        color = QColor(0, 255, 0) if hold in hold.is_selected else QColor(200, 200, 200)

        # Draw the hold contour
        pen = QPen(color, 2)
        painter.setPen(pen)

        if hold.contour_points:
            # Convert the hold points to QPoint objects from API data
            points = [QPoint(int(p.x), int(p.y)) for p in hold.contour_points]
            painter.drawPolyline(points)

    def draw_route_connections(self, painter: QPainter, selected_holds: List[Hold]) -> None:
        """
        Draws connections between the selected holds to represent the climbing route.
        """
        # Set the color for the route connections
        color = QColor(0, 255, 0)
        pen = QPen(color, 2)
        painter.setPen(pen)

        # Draw the connections between the selected holds
        for i in range(len(selected_holds) - 1):
            hold1 = selected_holds[i]
            hold2 = selected_holds[i + 1]
            painter.drawLine(int(hold1.x), int(hold1.y), int(hold2.x), int(hold2.y))

    def mousePressEvent(self, event) -> None:
        """
        Handles mouse click events - selecting and deselecting holds.
        When a user clicks on a hold:
        - if the hold wasn't selected - selects it and gives it the next order number
        - if the hold was selected - deselects it
        """
        click_pos = event.pos()

        for hold in self.holds:
            if hold.contains_point(click_pos.x(), click_pos.y()):
                if not hold.is_selected:
                    hold.is_selected = True
                    hold.order_in_route = self.next_hold_order
                    self.next_hold_order += 1
                else:
                    # Disable the hold selection
                    hold.is_selected = False
                    hold.order_in_route = None
                    # Update the order of the remaining holds
                    self._update_hold_order()

                self.update()
                break

    def _update_hold_order(self) -> None:
        """
        Updates the order of the holds in the route after a hold has been deselected.
        """
        selected_holds = [h for h in self.holds if h.is_selected]
        selected_holds.sort(key=lambda h: h.order_in_route if h.order_in_route is not None else float(
            'inf'))  # Sort the selected holds by their order in the route

        for i, hold in enumerate(selected_holds):
            hold.order_in_route = i

        self.next_hold_order = len(selected_holds)
