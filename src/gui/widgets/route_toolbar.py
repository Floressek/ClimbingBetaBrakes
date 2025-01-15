from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QPushButton, QLabel, QButtonGroup,
    QComboBox, QFrame, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont


class RouteToolbar(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self) -> None:
        # Main layout
        layout = QHBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(20, 12, 20, 12)

        # Route Controls Group
        route_group = self.create_button_group([
            ("New Route", "plus.png", False),
            ("Save Route", "save.png", False)
        ])
        self.new_route_button = route_group.findChild(QPushButton, "New Route")
        self.save_route_button = route_group.findChild(QPushButton, "Save Route")
        self.save_route_button.setEnabled(True)
        layout.addWidget(route_group)

        layout.addWidget(self.create_vertical_separator())

        # Mode Selection Group
        mode_group = QButtonGroup(self)
        mode_frame = self.create_button_group([
            ("Hands", "hand.png", True),
            ("Feet", "foot.png", True)
        ])
        self.hands_button = mode_frame.findChild(QPushButton, "Hands")
        self.feet_button = mode_frame.findChild(QPushButton, "Feet")
        mode_group.addButton(self.hands_button)
        mode_group.addButton(self.feet_button)
        self.hands_button.setChecked(True)
        layout.addWidget(mode_frame)

        layout.addWidget(self.create_vertical_separator())

        # Edit Controls Group
        edit_group = self.create_button_group([
            ("Edit Curves", "curve.png", True),
            ("Show Numbers", "numbers.png", True)
        ])
        self.curve_edit_button = edit_group.findChild(QPushButton, "Edit Curves")
        self.show_numbers = edit_group.findChild(QPushButton, "Show Numbers")
        layout.addWidget(edit_group)

        layout.addWidget(self.create_vertical_separator())

        # Grade Selector Group
        grade_frame = QFrame()
        grade_frame.setObjectName("toolbarGroup")
        grade_layout = QHBoxLayout(grade_frame)
        grade_layout.setContentsMargins(12, 8, 12, 8)
        grade_layout.setSpacing(8)

        grade_label = QLabel("Grade:")
        grade_label.setObjectName("toolbarLabel")

        self.grade_selector = QComboBox()
        self.grade_selector.addItems([
            "4a", "4b", "4c", "5a", "5b", "5c",
            "6a", "6a+", "6b", "6b+", "6c", "6c+",
            "7a", "7a+", "7b", "7b+"
        ])
        self.grade_selector.setObjectName("gradeSelector")

        grade_layout.addWidget(grade_label)
        grade_layout.addWidget(self.grade_selector)
        layout.addWidget(grade_frame)

        # Add final stretch
        layout.addStretch()

        self.apply_styles()

    def create_button_group(self, buttons):
        """Create a group of buttons with consistent styling"""
        frame = QFrame()
        frame.setObjectName("toolbarGroup")
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(8)

        for text, icon, checkable in buttons:
            btn = QPushButton(text)
            btn.setObjectName(text)
            if icon:
                btn.setIcon(QIcon(f"icons/{icon}"))
            btn.setCheckable(checkable)
            layout.addWidget(btn)

        return frame

    def create_vertical_separator(self):
        """Create a vertical separator line"""
        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setObjectName("separator")
        separator.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        return separator

    def apply_styles(self):
        """Apply modern styling to all components"""
        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
            }

            #toolbarGroup {
                background: rgba(255, 255, 255, 0.7);
                border: 1px solid #e0e0e0;
                border-radius: 6px;
            }

            QPushButton {
                padding: 8px 16px;
                font-size: 13px;
                border: none;
                background: transparent;
                border-radius: 4px;
                color: #333333;
                min-width: 80px;
            }

            QPushButton:hover {
                background: rgba(0, 0, 0, 0.05);
            }

            QPushButton:pressed {
                background: rgba(0, 0, 0, 0.1);
            }

            QPushButton:checked {
                background: #e3f2fd;
                color: #1976d2;
            }

            QPushButton:disabled {
                color: #999999;
                background: transparent;
            }

            QPushButton:checked:hover {
                background: #bbdefb;
            }

            #separator {
                color: #e0e0e0;
                margin: 0px 8px;
            }

            #toolbarLabel {
                font-size: 13px;
                color: #555555;
                margin-right: 4px;
            }

            #gradeSelector {
                padding: 6px 24px 6px 12px;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                min-width: 100px;
                background: white;
                font-size: 13px;
            }

            #gradeSelector:hover {
                border-color: #bbbbbb;
            }

            #gradeSelector:focus {
                border-color: #2196f3;
            }
        """)

    def enable_route_editing(self):
        """Enable route editing functionality"""
        self.save_route_button.setEnabled(True)