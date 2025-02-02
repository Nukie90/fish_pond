import uuid
from PySide6.QtWidgets import QMainWindow, QWidget
from PySide6.QtCore import Qt
import random
from datetime import datetime
from core.mqtt_client import MqttClient
from core.pond import Pond, Fish
from ui.widgets.fish_widget import FishWidget
from ui.generated.pond_ui import Ui_MainWindow
from PySide6.QtCore import Signal, QObject


class PondWindow(QMainWindow):
    fish_received = Signal(dict)

    def __init__(self):
        super().__init__()

        # Set up the UI from the generated file
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Initialize core components
        self.mqtt_client = MqttClient(self)
        self.pond = Pond(name="DC_Universe")
        self.fish_widgets = {}

        # Connect the signal to the slot
        self.fish_received.connect(self.handle_received_fish)

        # Connect button signals
        self.setup_connections()

        # Initial UI state
        self.ui.sendfishButton.setEnabled(False)

    def setup_connections(self):
        """Setup event handlers"""
        self.ui.addfishButton.clicked.connect(self.handle_add_fish)
        self.ui.sendfishButton.clicked.connect(self.handle_send_fish)
        self.ui.connectButton.clicked.connect(self.handle_mqtt_connection)

    def handle_mqtt_connection(self):
        """Handle MQTT connection"""
        self.mqtt_client.connect()
        self.ui.connectButton.setEnabled(False)
        self.ui.connectButton.setText("Connected")
        self.ui.sendfishButton.setEnabled(True)

    def reset_connect_button(self):
        """Reset connect button text after failed connection"""
        self.ui.connectButton.setText("Connect to MQTT")

    def handle_add_fish(self):
        """Handle adding a new fish to the pond"""
        fish = self.pond.add_fish(
            name=str(uuid.uuid4()),
            group_name=self.pond.name,
            lifetime=15,
            data="https://drive.google.com/uc?id=1qkGAxmmiL6AQMXi5ssArBk-7RoqtD7U3",
        )
        self.create_fish_widget(fish)
        print(f"Added fish with name: {fish.name}, lifetime: {fish.lifetime} seconds")

    def handle_received_fish(self, message):
        """Handle receiving a fish from another pond"""
        try:
            fish = self.pond.add_fish(
                name=message.get("name", ""),
                group_name=message["group_name"],
                lifetime=message["lifetime"],
                data=message["data"],
            )
            print(fish)
            self.create_fish_widget(fish)
            fish_info = f"Received fish from {message['group_name']}, name: {message['name']}, lifetime: {message['lifetime']} seconds"
            print(fish_info)

        except Exception as e:
            print(f"Error handling received fish: {e}")

    def handle_send_fish(self):
        """Handle sending a fish to another pond"""
        if not self.mqtt_client.is_connected():
            print("Cannot send fish: Not connected to MQTT broker")
            return

        try:
            send_to = "Parallel"

            if not self.pond.fishes:
                print("No fish available to send!")
                return

            name, fish = random.choice(list(self.pond.fishes.items()))

            self.mqtt_client.send_fish(
                name=name,
                group_name=self.pond.name,
                lifetime=fish.lifetime,
                send_to=send_to,
                data=fish.data,
            )

            self.fish_widgets[name].die()
            print(f"Sent fish with name: {name} to {send_to}")
        except Exception as e:
            print(f"Failed to send fish: {e}")

    def create_fish_widget(self, fish: Fish):
        """Create and setup a fish widget"""
        fish_widget = FishWidget(self.ui.mainFrame, self, fish)

        # Random position within the pond frame
        frame_size = self.ui.mainFrame.size()
        x = random.randint(0, frame_size.width() - 200)
        y = random.randint(0, frame_size.height() - 200)
        fish_widget.move(x, y)
        fish_widget.show()
        fish_widget.raise_()

        # Start lifetime countdown
        remaining_lifetime = fish.remaining_lifetime
        if remaining_lifetime > 0:
            fish_widget.start_lifetime(int(remaining_lifetime))

            # Store reference to widget
            self.fish_widgets[fish.name] = fish_widget
            self.update_fish_label()
        else:
            fish_widget.deleteLater()

    def update_fish_label(self):
        """Update the fish count label in the UI"""
        self.ui.fashLabel.setText(f"Fishes: {len(self.fish_widgets)}")

    def remove_fish_by_widget(self, fish_widget):
        """Remove fish from pond and UI when its lifetime ends"""
        fish_id_to_remove = None

        for fish_id, widget in self.fish_widgets.items():
            if widget == fish_widget:
                fish_id_to_remove = fish_id
                break

        if fish_id_to_remove:
            self.fish_widgets.pop(fish_id_to_remove, None)
            self.pond.fishes.pop(fish_id_to_remove, None)
            self.update_fish_label()

    def closeEvent(self, event):
        """Handle window closing"""
        self.mqtt_client.disconnect()
        super().closeEvent(event)
