from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QFormLayout,
                             QLineEdit, QTextEdit, QDialogButtonBox,
                             QLabel, QWidget, QComboBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class RouteInfoDialog(QDialog):
    """
    Dialog for entering route information.
    """

    def __init__(self, parent=None, initial_grade='6a'):
        super().__init__()
        self.setWindowTitle("Save Route")
        self.setMinimumWidth(400)
        self.setup_ui(initial_grade)

    def setup_ui(self, initial_grade):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        # Title
        title = QLabel("Save Route")
        title.setFont(QFont('Arial', 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Form layout for inputs
        form = QFormLayout()
        form.setSpacing(10)

        # Route name input
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Enter route name")
        form.addRow("Route Name: ", self.name_edit)

        # Author input
        self.author_edit = QLineEdit()
        self.author_edit.setPlaceholderText("Enter author name")
        form.addRow("Author: ", self.author_edit)

        # Grade selector
        self.grade_selector = QComboBox()
        self.grade_selector.addItems([
            '4a', '4b', '4c',
            '5a', '5b', '5c',
            '6a', '6a+', '6b', '6b+', '6c', '6c+',
            '7a', '7a+', '7b', '7b+', '7c', '7c+',
        ])
        self.grade_selector.setCurrentText(initial_grade)
        form.addRow("Grade: ", self.grade_selector)

        # Description input
        self.description_edit = QTextEdit()
        self.description_edit.setPlaceholderText("Enter route description")
        self.description_edit.setMinimumHeight(100)
        form.addRow("Description: ", self.description_edit)

        layout.addLayout(form)

        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel) # Save and Cancel buttons
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        # Apply modern styling - generated
        self.setStyleSheet("""
            QDialog {
                        background-color: white;
                    }
                    QLabel {
                        color: #333333;
                    }
                    QLineEdit, QTextEdit, QComboBox {
                        padding: 8px;
                        border: 1px solid #cccccc;
                        border-radius: 4px;
                        background-color: white;
                    }
                    QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
                        border: 1px solid #2196F3;
                    }
                    QPushButton {
                        padding: 8px 16px;
                        border: none;
                        border-radius: 4px;
                        color: white;
                        background-color: #2196F3;
                    }
                    QPushButton:hover {
                        background-color: #1976D2;
                    }
                    QPushButton[text="Cancel"] {
                        background-color: #f0f0f0;
                        color: #333333;
                    }
                    QPushButton[text="Cancel"]:hover {
                        background-color: #e0e0e0;
                    }
                """)

    def get_route_info(self):
        """
        Get the entered route information.
        :return:  Dictionary with route information
        """
        return {
            "name": self.name_edit.text(),
            "author": self.author_edit.text(),
            "description": self.description_edit.toPlainText(),
            "grade": self.grade_selector.currentText()
        }

    def set_grade(self, grade):
        """
        Set the grade for the route.
        :param grade:
        :return:
        """
        self.grade_selector.setCurrentText(grade)