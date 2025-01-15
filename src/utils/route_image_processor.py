from pathlib import Path
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPainter, QImage, QColor
from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime
from pathlib import Path
from src.utils.logger import setup_logger
from src.utils.config import ProjectConfig
from typing import List, Tuple

logger = setup_logger("utils/route_image", ProjectConfig.get_log_file("utils/route_image"))


class RouteImageProcessor:
    def __init__(self, font_path=None):
        self.font_path = font_path

    def add_route_info_overlay(self, hold_viewer, route_info, output_path):
        """
        Renders exactly what's visible in the HoldViewer and adds info overlay

        Args:
            hold_viewer: HoldViewer widget instance
            route_info: Dictionary containing route information
            output_path: Path where to save the processed image
        """
        try:
            # Create a QImage of the exact same size as the HoldViewer
            qimage = QImage(hold_viewer.size(), QImage.Format_ARGB32)
            qimage.fill(Qt.transparent)

            # Create painter for QImage
            painter = QPainter(qimage)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setRenderHint(QPainter.SmoothPixmapTransform)

            # Paint the wall image
            if hold_viewer.wall_image:
                scaled_image = hold_viewer.wall_image.scaled(
                    hold_viewer.size(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                x = (hold_viewer.width() - scaled_image.width()) // 2
                y = (hold_viewer.height() - scaled_image.height()) // 2
                painter.drawPixmap(x, y, scaled_image)

            # Draw holds using HoldViewer's own drawing functions
            for hold in hold_viewer.holds:
                hold_viewer.draw_hold(painter, hold)

            # Draw route connections using HoldViewer's function
            hold_viewer.draw_route_connections(painter, hold_viewer.holds)

            # End QPainter before converting image
            painter.end()

            # Convert QImage to PIL Image
            buffer = qimage.bits().asstring(qimage.width() * qimage.height() * 4)
            image = Image.frombytes(
                'RGBA',
                (qimage.width(), qimage.height()),
                buffer,
                'raw',
                'BGRA'
            )

            # Create overlay for route info
            overlay = Image.new('RGBA', image.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(overlay)

            # Draw route info box
            padding = 20
            rect_height = 180
            rect_width = 300
            rect_position = (image.width - rect_width - padding, padding)

            draw.rectangle(
                [
                    rect_position[0],
                    rect_position[1],
                    rect_position[0] + rect_width,
                    rect_position[1] + rect_height
                ],
                fill=(255, 255, 255, 230)
            )

            # Setup fonts
            try:
                title_font = ImageFont.truetype(self.font_path, 24) if self.font_path else ImageFont.load_default()
                info_font = ImageFont.truetype(self.font_path, 16) if self.font_path else ImageFont.load_default()
            except Exception:
                title_font = info_font = ImageFont.load_default()

            # Draw text
            text_x = rect_position[0] + 15
            text_y = rect_position[1] + 10

            # Draw route name
            draw.text((text_x, text_y), route_info["name"], font=title_font, fill=(0, 0, 0, 255))
            text_y += 35

            # Draw other info
            info_items = [
                f"Grade: {route_info['grade']}",
                f"Author: {route_info['author']}",
                f"Created: {datetime.now().strftime('%Y-%m-%d')}",
                f"Description: {route_info['description'][:50]}..."
            ]

            for item in info_items:
                draw.text((text_x, text_y), item, font=info_font, fill=(0, 0, 0, 255))
                text_y += 25

            # Composite image with overlay
            final_image = Image.alpha_composite(image, overlay)

            # Save the result
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            final_image.convert('RGB').save(output_path, 'JPEG', quality=95)

        except Exception as e:
            raise