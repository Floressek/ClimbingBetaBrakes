from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtGui import QPainter, QColor, QPen, QPixmap, QPainterPath
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
        self.scaled_points_cache = {}
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
        return QSize(1080, 880)

    def resizeEvent(self, event) -> None:
        """Clear cache and update the widget when resized."""
        self.scaled_points_cache.clear()
        super().resizeEvent(event)

    def paintEvent(self, event) -> None:
        """
        Draws the image and the holds on the widget.
        Method called by the Qt framework whenever the widget needs to be redrawn.
        """
        logger.debug("paintEvent called")

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        painter.setCompositionMode(QPainter.CompositionMode_SourceOver)

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

        # Similar setup as get_scaled_coordinates
        scaled_image = self.wall_image.scaled(
            self.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        x_offset = (self.width() - scaled_image.width()) // 2
        y_offset = (self.height() - scaled_image.height()) // 2

        # Remove offset
        image_x = widget_x - x_offset
        image_y = widget_y - y_offset

        # Convert back to original scale
        scale_x = self.wall_image.width() / scaled_image.width()
        scale_y = self.wall_image.height() / scaled_image.height()

        return image_x * scale_x, image_y * scale_y

    def get_scaled_coordinates(self, x: float, y: float) -> tuple[float, float]:
        """
        Scales the point coordinates based on the current scale factor.
        """
        if not self.wall_image:
            logger.warning("No wall image available for scaling")
            return x, y

        # Get original and scaled image dimensions
        orig_width = self.wall_image.width()
        orig_height = self.wall_image.height()

        scaled_image = self.wall_image.scaled(
            self.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        scaled_width = scaled_image.width()
        scaled_height = scaled_image.height()

        # Calculate scale factors
        scale_x = scaled_width / orig_width
        scale_y = scaled_height / orig_height

        # Calculate offsets for centering
        x_offset = (self.width() - scaled_width) // 2
        y_offset = (self.height() - scaled_height) // 2

        # Scale coordinates
        new_x = (x * scale_x) + x_offset
        new_y = (y * scale_y) + y_offset

        return new_x, new_y

    def get_scaled_points_for_hold(self, hold: Hold) -> List[QPoint]:
        """Get the scaled contour points for a hold."""
        # Id of the hold used as a key in the cache
        cache_key = hold.id
        if cache_key in self.scaled_points_cache:
            return self.scaled_points_cache[cache_key]

        scaled_points = []
        for p in hold.contour_points:
            x, y = self.get_scaled_coordinates(p.x, p.y)
            scaled_points.append(QPoint(int(x), int(y)))

        # Save the scaled points in the cache
        self.scaled_points_cache[cache_key] = scaled_points
        return scaled_points

    def draw_hold(self, painter: QPainter, hold: Hold) -> None:
        """Draws a single hold with antialiasing and optimized rendering."""
        color = QColor(0, 255, 0) if hold.is_selected else QColor(200, 200, 200)

        # Better quality rendering
        pen = QPen(color, 2, Qt.SolidLine)
        pen.setJoinStyle(Qt.RoundJoin)  # Round line corners
        pen.setCapStyle(Qt.RoundCap)  # Round line endings
        painter.setPen(pen)

        if hold.contour_points:
            # Used for drawing the hold contour buffer
            points = self.get_scaled_points_for_hold(hold)

            # Close the polygon
            path = QPainterPath()
            if points:
                path.moveTo(points[0])
                for point in points[1:]:
                    path.lineTo(point)
                path.lineTo(points[0])  # Close the polygon

            # Minor optimization - fill the path with a transparent color
            if hold.is_selected:
                painter.fillPath(path, QColor(152, 255, 0, 30))  # Clicked color
            else:
                painter.fillPath(path, QColor(200, 200, 200, 30))

            painter.drawPath(path)

    def draw_hold_old(self, painter: QPainter, hold: Hold) -> None:
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
        if not self.wall_image:
            return

        if not self.rect().contains(event.pos()):
            return  # Ignore clicks outside the widget

        widget_x = event.pos().x()
        widget_y = event.pos().y()

        # Convert click coordinates to image coordinates
        image_x, image_y = self.get_image_coordinates(widget_x, widget_y)

        for hold in self.holds:
            if hold.contains_point(image_x, image_y):
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
