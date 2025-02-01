from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import QPoint, QTimer
import random
from datetime import datetime
from ui.generated.pond_ui import Ui_MainWindow
from core.mqtt_client import MqttClient
from core.pond import Pond, Fish
from ui.widgets.fish_widget import FishWidget
from pathlib import Path
import base64


class PondWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.mqtt_client = MqttClient()
        self.pond = Pond(name="DC Universe")
        self.fish_widgets = {}
        self.ui.sendfishButton.setEnabled(False)

        self.connect_button_timer = QTimer(self)
        self.connect_button_timer.timeout.connect(self.reset_connect_button)
        self.connect_button_timer.setSingleShot(True)

        # Set up MQTT callback for receiving fish
        self.mqtt_client.set_new_fish_callback(self.handle_received_fish)

        self.setup_connections()

    def setup_connections(self):
        self.ui.connectButton.clicked.connect(self.handle_mqtt_connection)
        self.ui.addfishButton.clicked.connect(self.handle_add_fish)
        self.ui.sendfishButton.clicked.connect(self.handle_send_fish)

    def handle_mqtt_connection(self):
        try:
            self.mqtt_client.connect()
            self.ui.connectButton.setEnabled(False)
            self.ui.connectButton.setText("Connected")
            self.ui.sendfishButton.setEnabled(True)
        except Exception as e:
            print(f"Failed to connect: {e}")
            self.ui.connectButton.setText("Failed")
            self.connect_button_timer.start(3000)

    def reset_connect_button(self):
        """Reset connect button text after failed connection"""
        self.ui.connectButton.setText("Connect to MQTT")

    def handle_add_fish(self):
        """Handle adding a new fish to the pond"""
        fish = self.pond.add_fish()
        self.create_fish_widget(fish)
        print(f"Added fish with name: {fish.name}, lifetime: {fish.lifetime} seconds")

    def handle_received_fish(
        self,
        group_name: str,
        lifetime: int,
        name: str = "",
        data: str = "",
    ):
        """Handle receiving a fish from another pond"""
        try:
            fish = Fish(
                name=name,
                spawn_time=datetime.now(),
                group_name=group_name,
                lifetime=lifetime,
            )

            if data:
                gif_path = Path(__file__).parent.parent / "resources/images/temp"
                gif_path.mkdir(exist_ok=True, parents=True)
                temp_gif = gif_path / f"{group_name}.gif"

                gif_bytes = base64.b64decode(data)
                with open(temp_gif, "wb") as f:
                    f.write(gif_bytes)

                fish.gif_path = str(temp_gif)

            self.pond.fishes[fish.name] = fish
            self.create_fish_widget(fish)
            fish_info = f"Received fish from {group_name}, name: {name}, lifetime: {lifetime} seconds"
            print(fish_info)

        except Exception as e:
            print(f"Error handling received fish: {e}")

    def handle_send_fish(self):
        """Handle sending a fish to another pond"""
        if not self.mqtt_client.is_connected():
            print("Cannot send fish: Not connected to MQTT broker")
            return

        try:
            send_to = "DC_Universe2"

            if not self.pond.fishes:
                print("No fish available to send!")
                return

            name, fish = random.choice(list(self.pond.fishes.items()))

            self.mqtt_client.send_fish(
                name=name,
                group_name=self.pond.name,
                lifetime=fish.lifetime,
                send_to=send_to,
            )

            self.fish_widgets[name].die()
            print(f"Sent fish with name: {name} to {send_to}")
        except Exception as e:
            print(f"Failed to send fish: {e}")

    def create_fish_widget(self, fish: Fish):
        """Create and setup a fish widget"""
        fish_widget = FishWidget(self.ui.mainFrame, self, fish)

        # Random position within the pond frame
        x = random.randint(0, self.ui.mainFrame.width() - fish_widget.width())
        y = random.randint(0, self.ui.mainFrame.height() - fish_widget.height())
        fish_widget.move(QPoint(x, y))

        # Start lifetime countdown
        remaining_lifetime = fish.remaining_lifetime
        if remaining_lifetime > 0:
            fish_widget.start_lifetime(int(remaining_lifetime))
            fish_widget.show()

            # Store reference to widget
            self.fish_widgets[fish.name] = fish_widget
            self.update_fish_label()
            self.update_fish_info()
        else:
            fish_widget.deleteLater()

    def update_fish_info(self, fish_widget: FishWidget = None):
        """Update the fish information display"""
        if not self.fish_widgets:
            self.ui.fishInfoText.setText("Fish List:\nNo fish in the pond")
            return

        info_text = "Fish List:\n"
        for name, widget in self.fish_widgets.items():
            if widget.fish:
                fish = widget.fish
                line = f"Name: {fish.name} | Lifetime: {widget.remaining_lifetime}s | "
                if fish.group_name != self.pond.name:
                    line += f"From: {fish.group_name}"
                else:
                    line += "Our fish"
                info_text += line + "\n"

        self.ui.fishInfoText.setText(info_text)

    def remove_fish_by_widget(self, fish_widget: FishWidget):
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
            self.update_fish_info()

    def update_fish_label(self):
        """Update the fish count label in the UI"""
        self.ui.fashLabel.setText(f"Fish Count: {len(self.fish_widgets)}")

    def closeEvent(self, event):
        self.mqtt_client.disconnect()
        super().closeEvent(event)
