from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QPen, QPixmap, QPainterPath
from PyQt5.QtCore import Qt, QPoint, QSize
from typing import List, Optional

from src.core.connection import Connection
from src.core.hold import Hold
from src.core.movement_type import HoldType
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
        self.next_hand_order = 0  # Counter for the order of the next hand in the route
        self.next_foot_order = 0  # Counter for the order of the next hand in the route
        self.next_hold_order = 0  # Counter for the order of the next hold in the route, old
        self.scale_factor = 1.0
        self.current_hold_type = HoldType.HAND  # Default hold type
        self.holds: List[Hold] = []
        self.scaled_points_cache = {}
        self.arrow_points = {}  # Arrow ID -> dict that contains control points, not used
        self.wall_image: Optional[QPixmap] = None  # Image of the climbing wall
        self.setMouseTracking(True)
        self.arrow_edit_mode = False
        self.show_numbers = False
        self.selected_arrow = None

        self.current_mode = "normal"  # Default mode
        self.dragged_connection = None # Connection being dragged
        self.drag_point = None  # Point on the connection being dragged
        self.active_connection = None  # Connection being edited

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
            # logger.debug(f"Drawing hold: {hold}")
            self.draw_hold(painter, hold)

        # # Draw route connections
        # selected_holds = [h for h in self.holds if h.is_selected]
        # selected_holds.sort(key=lambda h: h.order_in_route)
        # logger.debug(f"Selected holds for route connections: {selected_holds}") #TODO add for hands and feet selected holds
        self.draw_route_connections(painter, self.holds)

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
        if hold.is_hand_selected:
            color = QColor(255, 165, 0)  # Orange dla rąk
        elif hold.is_foot_selected:
            color = QColor(255, 0, 0)  # Red dla nóg
        else:
            color = QColor(200, 200, 200)  # szary dla niezaznaczonych

        # Better quality rendering
        pen = QPen(color, 2, Qt.SolidLine)
        pen.setJoinStyle(Qt.RoundJoin)  # Round line corners
        pen.setCapStyle(Qt.RoundCap)  # Round line endings
        painter.setPen(pen)

        if hold.contour_points:
            points = self.get_scaled_points_for_hold(hold)
            path = QPainterPath()
            if points:
                path.moveTo(points[0])
                for point in points[1:]:
                    path.lineTo(point)
                path.lineTo(points[0])

            # Filler color for selected holds
            if hold.is_hand_selected:  # new color for hands
                painter.fillPath(path, QColor(255, 165, 0, 30))  # Orange with transparency
            elif hold.is_foot_selected:
                painter.fillPath(path, QColor(255, 0, 0, 30))  # Red with transparency
            else:
                painter.fillPath(path, QColor(200, 200, 200, 30))  # Default color

            painter.drawPath(path)


    def draw_route_connections(self, painter: QPainter, selected_holds: List[Hold]) -> None:
        """
        Draws connections between the selected holds to represent the climbing route.
        """

        # Draw connections between the selected hand holds
        hand_holds = [h for h in self.holds if h.is_hand_selected]
        hand_holds.sort(key=lambda h: h.hand_order if h.hand_order is not None else float('inf'))

        if len(hand_holds) >= 2:
            painter.setPen(QPen(QColor(255, 165, 0), 2))  # orange
            for i in range(len(hand_holds) - 1):
                hold1, hold2 = hand_holds[i], hand_holds[i + 1]
                if hold1.hand_order is not None and hold2.hand_order is not None:  # check if they have order
                    connection = Connection(hold1, hold2)
                    self.draw_single_connection(painter, connection)

                    # x1, y1 = self.get_scaled_coordinates(hold1.x, hold1.y)
                    # x2, y2 = self.get_scaled_coordinates(hold2.x, hold2.y)
                    # painter.drawLine(int(x1), int(y1), int(x2), int(y2))

        # Draw connections between the selected foot holds
        foot_holds = [h for h in self.holds if h.is_foot_selected]
        foot_holds.sort(key=lambda h: h.foot_order if h.foot_order is not None else float('inf'))

        if len(foot_holds) >= 2:
            painter.setPen(QPen(QColor(255, 0, 0), 2))  # red
            for i in range(len(foot_holds) - 1):
                hold1, hold2 = foot_holds[i], foot_holds[i + 1]
                if hold1.foot_order is not None and hold2.foot_order is not None:  # check if they have order
                    connection = Connection(hold1, hold2)
                    self.draw_single_connection(painter, connection)

                    # x1, y1 = self.get_scaled_coordinates(hold1.x, hold1.y)
                    # x2, y2 = self.get_scaled_coordinates(hold2.x, hold2.y)
                    # painter.drawLine(int(x1), int(y1), int(x2), int(y2))

    def draw_single_connection(self, painter: QPainter, connection: Connection) -> None:
        """
        Draws a single connection between two holds.
        """
        x1, y1 = self.get_scaled_coordinates(connection.hold1.x, connection.hold1.y)
        x2, y2 = self.get_scaled_coordinates(connection.hold2.x, connection.hold2.y)

        if connection.is_curved:
            if not connection.control_points:
                # Calculate the scaled control point perpendicularly to the line between the holds
                mid_x = (x1 + x2) / 2
                mid_y = (y1 + y2) / 2
                dx = -(y2 - y1) * 0.2  # perpendicularly placed vector
                dy = (x2 - x1) * 0.2
                connection.control_points = (mid_x + dx, mid_y + dy)


            # Get the scaled control point
            control_x, control_y = connection.control_points

            # Draw the curved connection Bezier curve
            path = QPainterPath()
            path.moveTo(x1, y1)
            path.quadTo(control_x, control_y, x2, y2)
            painter.drawPath(path)

            # Draw control point if in edit mode
            if self.current_mode == "curve_edit":
                painter.setPen(QPen(Qt.red, 1))
                painter.drawEllipse(
                    int(control_x - 5),
                    int(control_y - 5),
                    10, 10
                )
        else:
            # Draw straight line
            painter.drawLine(int(x1), int(y1), int(x2), int(y2))

        # Draw number if exists
        if connection.number is not None:
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            painter.drawText(
                int(mid_x - 10),
                int(mid_y - 10),
                str(connection.number)
            )

    def mousePressEvent(self, event) -> None:
        """
        Handles mouse click events - selecting and deselecting holds. Also is used for curve editing.
        When a user clicks on a hold:
        - if the hold wasn't selected - selects it and gives it the next order number
        - if the hold was selected - deselects it
        """

        if not self.wall_image:
            return

        if not self.rect().contains(event.pos()):
            return  # Ignore clicks outside the widget

        # New curve editing mode
        if self.current_mode == "curve_edit":
            # Get active connections from current holds
            hand_holds = [h for h in self.holds if h.is_hand_selected]
            foot_holds = [h for h in self.holds if h.is_foot_selected]

            active_connections = [] # List of active connections

            # Add hand connections
            for i in range(len(hand_holds) - 1):
                if hand_holds[i].hand_order is not None and hand_holds[i + 1].hand_order is not None:
                    active_connections.append(Connection(hand_holds[i], hand_holds[i + 1]))

            # Add foot connections
            for i in range(len(foot_holds) - 1):
                if foot_holds[i].foot_order is not None and foot_holds[i + 1].foot_order is not None:
                    active_connections.append(Connection(foot_holds[i], foot_holds[i + 1]))

            # Check for clicks on control points or connection midpoints
            for connection in active_connections:
                if connection.control_points:
                    x, y = self.get_scaled_coordinates(*connection.control_points)
                    dist = ((event.pos().x() - x) ** 2 + (event.pos().y() - y) ** 2) ** 0.5
                    if dist <= 10:  # 10px radius for clicking
                        self.dragged_connection = connection
                        self.drag_point = 'control'
                        return

                # Check midpoint click
                if connection.midpoint:
                    mid_x, mid_y = self.get_scaled_coordinates(*connection.midpoint)
                    dist = ((event.pos().x() - mid_x) ** 2 + (event.pos().y() - mid_y) ** 2) ** 0.5
                    if dist <= 10:
                        self.active_connection = connection
                        if event.button() == Qt.RightButton:
                            connection.is_curved = not connection.is_curved
                        self.update()
                        return


        widget_x = event.pos().x()
        widget_y = event.pos().y()

        # Convert click coordinates to image coordinates
        image_x, image_y = self.get_image_coordinates(widget_x, widget_y)

        for hold in self.holds:
            if hold.contains_point(image_x, image_y):
                if self.current_hold_type == HoldType.HAND:
                    if not hold.is_hand_selected:
                        hold.is_hand_selected = True
                        hold.hand_order = self.next_hand_order  # ustawiamy kolejność
                        self.next_hand_order += 1
                    else:
                        hold.is_hand_selected = False
                        hold.hand_order = None
                        self._update_hand_order()
                else:  # FOOT
                    if not hold.is_foot_selected:
                        hold.is_foot_selected = True
                        hold.foot_order = self.next_foot_order  # ustawiamy kolejność
                        self.next_foot_order += 1
                    else:
                        hold.is_foot_selected = False
                        hold.foot_order = None
                        self._update_foot_order()

                self.update()
                break

    def _set_mode(self, mode: str) -> None:
        """Sets the current mode of the hold viewer."""
        self.current_mode = mode
        logger.info(f"Set mode to {mode}")
        self.update()

    def _update_hand_order(self) -> None:
        """Updates the order of hand holds."""
        selected_hand_holds = [h for h in self.holds if h.is_hand_selected]
        logger.debug(f"Updating order for {len(selected_hand_holds)} hand holds")

        for i, hold in enumerate(selected_hand_holds):
            hold.hand_order = i
            logger.debug(f"Hand hold {hold.id} set to order {i}")

        self.next_hand_order = len(selected_hand_holds)

    def _update_foot_order(self) -> None:
        """Updates the order of foot holds."""
        selected_foot_holds = [h for h in self.holds if h.is_foot_selected]
        logger.debug(f"Updating order for {len(selected_foot_holds)} foot holds")

        for i, hold in enumerate(selected_foot_holds):
            hold.foot_order = i
            logger.debug(f"Foot hold {hold.id} set to order {i}")

        self.next_foot_order = len(selected_foot_holds)

