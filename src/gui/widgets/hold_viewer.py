from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtGui import QPainter, QColor, QPen, QPixmap
from PyQt5.QtCore import Qt, QPoint, QSize
from typing import List, Optional
from src.core.hold import Hold
from src.utils.logger import setup_logger
from src.utils.config import ProjectConfig

logger = setup_logger("gui/widgets/hold_viewer", ProjectConfig.get_log_file("gui"))


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
        self.wall_image: Optional[QPixmap] = None  # Image of the climbing wall
        self.setMouseTracking(True)
        self.scale_factor = 1.0

    def load_image(self, image_path: str) -> None:
        """Loads the climbing wall image"""
        try:
            self.wall_image = QPixmap(image_path)
            if self.wall_image.isNull():
                logger.error(f"Failed to load image: {image_path}")
                return
            logger.info(f"Successfully loaded image: {image_path}")
            self.update()
        except Exception as e:
            logger.error(f"Error loading image: {e}")

    def sizeHint(self) -> QSize:
        """Sugerowany rozmiar widgetu"""
        if self.wall_image:
            return self.wall_image.size()
        return QSize(640, 480)

    # def paintEvent(self, event) -> None:
    #     """
    #     Draws the image and the holds on the widget.
    #     Method called by the Qt framework whenever the widget needs to be redrawn.
    #     """
    #     painter = QPainter(self)
    #     painter.setRenderHint(QPainter.Antialiasing)
    #
    #     # First draw the wall image if available
    #     if self.wall_image:
    #         # Skalujemy obraz do wymiarów widgetu zachowując proporcje
    #         scaled_image = self.wall_image.scaled(
    #             self.size(),
    #             Qt.KeepAspectRatio,
    #             Qt.SmoothTransformation
    #         )
    #         # Centrujemy obraz w widgecie
    #         x = (self.width() - scaled_image.width()) // 2
    #         y = (self.height() - scaled_image.height()) // 2
    #         painter.drawPixmap(x, y, scaled_image)
    #
    #     # Draw the holds
    #     for hold in self.holds:
    #         self.draw_hold(painter, hold)
    #
    #     # Draw route connections
    #     selected_holds = [h for h in self.holds if h.is_selected]
    #     selected_holds.sort(key=lambda h: h.order_in_route)
    #     if len(selected_holds) > 1:
    #         self.draw_route_connections(painter, selected_holds)

    def paintEvent(self, event) -> None:
        """
        Draws the image and the holds on the widget.
        Method called by the Qt framework whenever the widget needs to be redrawn.
        """
        logger.debug("paintEvent called")

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # First draw the wall image if available
        if self.wall_image:
            logger.debug("Wall image is available")
            # Skalujemy obraz do wymiarów widgetu zachowując proporcje
            scaled_image = self.wall_image.scaled(
                self.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            # Centrujemy obraz w widgecie
            x = (self.width() - scaled_image.width()) // 2
            y = (self.height() - scaled_image.height()) // 2
            logger.debug(f"Drawing wall image at position ({x}, {y})")
            painter.drawPixmap(x, y, scaled_image)
        else:
            logger.debug("No wall image to draw")

        # Draw the holds
        for hold in self.holds:
            logger.debug(f"Drawing hold: {hold}")
            self.draw_hold(painter, hold)

        # Draw route connections
        selected_holds = [h for h in self.holds if h.is_selected]
        selected_holds.sort(key=lambda h: h.order_in_route)
        logger.debug(f"Selected holds for route connections: {selected_holds}")
        if len(selected_holds) > 1:
            logger.debug("Drawing route connections")
            self.draw_route_connections(painter, selected_holds)
        else:
            logger.debug("Not enough holds selected to draw route connections")

    def get_image_coordinates(self, widget_x: float, widget_y: float) -> tuple[float, float]:
        """
        Converts widget coordinates to image coordinates.
        """
        if not self.wall_image:
            return widget_x, widget_y

        scaled_image = self.wall_image.scaled(
            self.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        # Calculate scale factors
        scale_x = self.wall_image.width() / scaled_image.width()
        scale_y = self.wall_image.height() / scaled_image.height()

        # Calculate offsets
        x_offset = (self.width() - scaled_image.width()) // 2
        y_offset = (self.height() - scaled_image.height()) // 2

        # Convert coordinates
        image_x = (widget_x - x_offset) * scale_x
        image_y = (widget_y - y_offset) * scale_y

        return image_x, image_y

    def get_scaled_coordinates(self, x: float, y: float) -> tuple[float, float]:
        """
        Scales the point coordinates based on the current scale factor.
        """
        if not self.wall_image:
            logger.warning("No wall image available for scaling")
            return x, y

        # Calculate the scaled point coordinates
        scaled_image = self.wall_image.scaled(
            self.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        scale_x = scaled_image.width() / self.wall_image.width()
        scale_y = scaled_image.height() / self.wall_image.height()

        # Offset the point to the center of the widget
        x_offset = (self.width() - scaled_image.width()) // 2
        y_offset = (self.height() - scaled_image.height()) // 2

        # Scale the point coordinates
        scaled_x = x * scale_x + x_offset
        scaled_y = y * scale_y + y_offset

        return scaled_x, scaled_y

    def draw_hold(self, painter: QPainter, hold: Hold) -> None:
        """
        Draws a single hold on the widget.
        """
        # Set the color based on whether the hold is selected
        color = QColor(0, 255, 0) if hold.is_selected else QColor(200, 200, 200)

        # Draw the hold contour
        pen = QPen(color, 2)
        painter.setPen(pen)

        # Draw the hold contour points
        if hold.contour_points:
            # Calculate the scaled coordinates of the hold points
            scaled_points = []
            for p in hold.contour_points:
                scaled_x, scaled_y = self.get_scaled_coordinates(p.x, p.y)
                scaled_points.append(QPoint(int(scaled_x), int(scaled_y))) # Close the polygon
            painter.drawPolyline(scaled_points)
            logger.debug(f"Drawing hold contour: {scaled_points}")
        else:
            logger.warning("No contour points available for hold")
            # Jeśli nie ma punktów konturu, narysuj okrąg
            scaled_x, scaled_y = self.get_scaled_coordinates(hold.x, hold.y)
            radius = 10  # możemy też przeskalować promień jeśli potrzeba
            painter.drawEllipse(QPoint(int(scaled_x), int(scaled_y)), radius, radius)
            logger.debug(f"Drawing hold circle at position ({scaled_x}, {scaled_y})")

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

            x1, y1 = self.get_scaled_coordinates(hold1.x, hold1.y)
            x2, y2 = self.get_scaled_coordinates(hold2.x, hold2.y)
            painter.drawLine(int(x1), int(y1), int(x2), int(y2))

    def mousePressEvent(self, event) -> None:
        """
        Handles mouse click events - selecting and deselecting holds.
        When a user clicks on a hold:
        - if the hold wasn't selected - selects it and gives it the next order number
        - if the hold was selected - deselects it
        """
        click_widget_x = event.pos().x()
        click_widget_y = event.pos().y()

        # Convert click coordinates to image coordinates
        click_x, click_y = self.get_image_coordinates(click_widget_x, click_widget_y)

        for hold in self.holds:
            if hold.contains_point(click_x, click_y):
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
