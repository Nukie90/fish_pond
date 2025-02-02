from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout

class AddSenderDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.send_clicked = False
        
        self.setWindowTitle("Add Group")
        self.setFixedSize(300, 150)
        
        # Main layout
        layout = QVBoxLayout()
        
        # Input field for sender name
        self.label = QLabel("Enter group name:")
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Group Name")
        
        # Button layout
        button_layout = QHBoxLayout()
        
        # Buttons
        self.add_button = QPushButton("Add")
        self.cancel_button = QPushButton("Cancel")
        
        # Layout arrangement
        layout.addWidget(self.label)
        layout.addWidget(self.input_field)
        
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
        # Connect buttons
        self.add_button.clicked.connect(self.handle_add)
        self.cancel_button.clicked.connect(self.reject)
        
    def handle_add(self):
        self.send_clicked = False
        self.accept()
        
    def handle_send(self):
        self.send_clicked = True
        self.accept()
        
    def get_sender_name(self):
        return self.input_field.text().strip()