from PySide6.QtWidgets import QMainWindow, QMessageBox
from PySide6.QtCore import QPoint
import random
from datetime import datetime
from ui.generated.pond_ui import Ui_MainWindow
from core.mqtt_client import MqttClient
from core.pond import Pond, Fish
from ui.widgets.fish_widget import FishWidget
from ui.views.add_sender_dialog import AddSenderDialog

class PondWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.mqtt_client = MqttClient()
        self.pond = Pond(name="DC Universe")
        self.fish_widgets = {}
        self.group_names = set()
        
        # Initialize the combo box
        self.init_combo_box()
        
        # Set up MQTT callback for receiving fish
        self.mqtt_client.set_new_fish_callback(self.handle_received_fish)
        
        self.setup_connections()
        
    def init_combo_box(self):
        """Initialize the combo box with add group option"""
        self.ui.groupselectionbox.clear()
        self.ui.groupselectionbox.addItem("Add Group...")
        for group in sorted(self.group_names):
            self.ui.groupselectionbox.addItem(group)
            
    def setup_connections(self):
        self.ui.connectButton.clicked.connect(self.handle_mqtt_connection)
        self.ui.addfishButton.clicked.connect(self.handle_add_fish)
        self.ui.sendfishButton.clicked.connect(self.handle_send_fish)
        self.ui.groupselectionbox.activated.connect(self.handle_combo_box_change)
        
    def handle_combo_box_change(self, index):
        """Handle combo box selection changes"""
        if self.ui.groupselectionbox.currentText() == "Add Group...":
            dialog = AddSenderDialog(self)
            if dialog.exec():
                new_group = dialog.get_sender_name()
                if new_group:
                    if new_group not in self.group_names:
                        self.group_names.add(new_group)
                        self.init_combo_box()
                        # Set the combo box to the newly added group
                        index = self.ui.groupselectionbox.findText(new_group)
                        self.ui.groupselectionbox.setCurrentIndex(index)
                        
                        # If dialog was accepted with the send button
                        if dialog.send_clicked:
                            self.handle_send_fish()
                    else:
                        QMessageBox.warning(self, "Warning", "Group name already exists!")
                        
    def create_fish_widget(self, fish: Fish):
        """Create and setup a fish widget"""
        fish_widget = FishWidget(self.ui.mainFrame, self, fish.fish_id)
        
        # Random position within the pond frame
        x = random.randint(0, self.ui.mainFrame.width() - 50)  # Assuming fish widget width
        y = random.randint(0, self.ui.mainFrame.height() - 50)  # Assuming fish widget height
        fish_widget.move(QPoint(x, y))
        
        # Start lifetime countdown
        remaining_lifetime = fish.remaining_lifetime
        if remaining_lifetime > 0:
            fish_widget.start_lifetime(int(remaining_lifetime))
            fish_widget.show()
            
            # Store reference to widget
            self.fish_widgets[fish.fish_id] = fish_widget
            
            self.update_fish_label()
        else:
            fish_widget.deleteLater()
            
    def handle_add_fish(self):
        """Handle adding a new fish to the pond"""
        fish = self.pond.add_fish()
        self.create_fish_widget(fish)
        print(f"Added fish with ID: {fish.fish_id}, lifetime: {fish.lifetime} seconds")
        
    def handle_received_fish(self, group_name: str, lifetime: int, name: str = ""):
        """Handle receiving a fish from another pond"""
        try:
            fish = Fish(
                name=name,
                spawn_time=datetime.now(),
                group_name=group_name,
                lifetime=lifetime,
            )
            
            self.pond.fishes[fish.fish_id] = fish
            self.create_fish_widget(fish)
            fish_info = f"Received fish from {group_name}"
            if name:
                fish_info += f", name: {name}"
            fish_info += f", new ID: {fish.fish_id}, lifetime: {lifetime} seconds"
            print(fish_info)
            
        except Exception as e:
            print(f"Error handling received fish: {e}")
            
    def handle_mqtt_connection(self):
        try:
            self.mqtt_client.connect()
            self.ui.connectButton.setEnabled(False)
            self.ui.connectButton.setText("Connected")
        except Exception as e:
            print(f"Failed to connect: {e}")
            
    def handle_send_fish(self):
        """Handle sending a fish to selected group"""
        selected_group = self.ui.groupselectionbox.currentText()
        
        if selected_group == "Add Group..." or not selected_group:
            QMessageBox.warning(self, "Warning", "Please select or add a group first!")
            return
            
        try:
            if not self.pond.fishes:
                QMessageBox.warning(self, "Warning", "No fish to send! Add some fish first.")
                return
                
            fish_id, fish = random.choice(list(self.pond.fishes.items()))
            self.mqtt_client.send_fish(
                group_name=fish.group_name,
                name=fish_id,
                lifetime=fish.lifetime,
                send_to=selected_group
            )
            print(f"Sent fish with ID: {fish_id} to {selected_group}")
        except Exception as e:
            print(f"Failed to send fish: {e}")
            QMessageBox.critical(self, "Error", f"Failed to send fish: {str(e)}")

    def closeEvent(self, event):
        self.mqtt_client.disconnect()
        super().closeEvent(event)
        
    def remove_fish_by_widget(self, fish_widget: FishWidget):
        """Remove fish from pond and UI when its lifetime ends"""
        fish_id_to_remove = None

        # Find the fish ID associated with the widget
        for fish_id, widget in self.fish_widgets.items():
            if widget == fish_widget:
                fish_id_to_remove = fish_id
                break

        if fish_id_to_remove:
            self.fish_widgets.pop(fish_id_to_remove, None)  # Remove from dict
            self.pond.fishes.pop(fish_id_to_remove, None)   # Remove from pond data
            self.update_fish_label()  # Update UI

    def update_fish_label(self):
        """Update the fish count label in the UI"""
        if len(self.fish_widgets) == 1:
            self.ui.fashLabel.setText(f"Fish: {len(self.fish_widgets)}")
        else:
            self.ui.fashLabel.setText(f"Fishes: {len(self.fish_widgets)}")
        print(f"Fish Count: {len(self.fish_widgets)}")

