from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QComboBox,
    QPushButton,
    QLabel,
    QHBoxLayout,
)
from PySide6.QtCore import Qt
import random


class PondSelectionDialog(QDialog):
    def __init__(self, connected_ponds, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Destination...")
        self.setModal(True)
        self.setFixedSize(400, 350)  # Made taller for new button
        self.connected_ponds = connected_ponds
        self.selected_random = False

        self.setStyleSheet(
            """
            QDialog {
                background-color: #FFFFFF;
            }
            QLabel {
                font-size: 18px;
                color: #333333;
                padding: 10px;
                margin-bottom: 15px;
            }
            QComboBox {
                padding: 8px 15px;
                border: 2px solid #CCCCCC;
                border-radius: 8px;
                background-color: white;
                min-height: 50px;
                font-size: 16px;
                margin: 15px 0;
                color: #333333;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
                padding-right: 10px;
            }
            QComboBox::down-arrow {
                border: none;
                background: #666666;
                width: 12px;
                height: 12px;
            }
            QComboBox:hover {
                border-color: #66afe9;
            }
            QComboBox QAbstractItemView {
                border: 2px solid #CCCCCC;
                border-radius: 8px;
                background-color: white;
                selection-background-color: #66afe9;
                selection-color: white;
                color: #333333;
                padding: 4px;
            }
            QPushButton {
                min-height: 40px;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                min-width: 150px;
                margin: 8px 0;
            }
            QPushButton#sendButton {
                background-color: #4CAF50;
                color: white;
            }
            QPushButton#sendButton:hover {
                background-color: #45a049;
            }
            QPushButton#sendRandomButton {
                background-color: #FF9800;
                color: white;
            }
            QPushButton#sendRandomButton:hover {
                background-color: #F57C00;
            }
            QPushButton#cancelButton {
                background-color: #f44336;
                color: white;
            }
            QPushButton#cancelButton:hover {
                background-color: #da190b;
            }
        """
        )

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(40, 30, 40, 30)

        # Add label
        label = QLabel("Select a pond to send fish to:")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        # Add combo box for pond selection
        self.pond_combo = QComboBox()
        self.pond_combo.addItems(connected_ponds)
        self.pond_combo.setMinimumWidth(320)
        self.pond_combo.setPlaceholderText("Select a pond...")
        self.pond_combo.setCurrentIndex(-1)
        layout.addWidget(self.pond_combo)

        # Add spacing
        layout.addSpacing(10)

        # Add buttons
        send_button = QPushButton("Send")
        send_button.setObjectName("sendButton")
        send_button.clicked.connect(self.accept)
        layout.addWidget(send_button)

        # Add cancel button
        cancel_button = QPushButton("Cancel")
        cancel_button.setObjectName("cancelButton")
        cancel_button.clicked.connect(self.reject)
        layout.addWidget(cancel_button)

        self.setLayout(layout)

    def selected_pond(self):
        return self.pond_combo.currentText()
