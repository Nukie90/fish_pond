from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import QPoint
import random
from ui.generated.pond_ui import Ui_MainWindow
from core.mqtt_client import MqttClient
from core.pond import Pond
from ui.widgets.fish_widget import FishWidget


class PondWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.mqtt_client = MqttClient()
        self.pond = Pond(name="DC Universe")
        self.fish_widgets = {}

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
        except Exception as e:
            print(f"Failed to connect: {e}")

    def handle_add_fish(self):
        """Handle adding a new fish to the pond"""
        # Create new fish in the pond
        fish = self.pond.add_fish()

        # Create and setup fish widget
        fish_widget = FishWidget(self.ui.mainFrame)

        # Random position within the pond frame
        x = random.randint(0, self.ui.mainFrame.width() - fish_widget.width())
        y = random.randint(0, self.ui.mainFrame.height() - fish_widget.height())
        fish_widget.move(QPoint(x, y))

        # Start lifetime countdown
        fish_widget.start_lifetime(fish.lifetime)
        fish_widget.show()

        # Store reference to widget
        self.fish_widgets[fish.fish_id] = fish_widget

        print(f"Added fish with ID: {fish.fish_id}")

    def handle_send_fish(self):
        # TODO: Implement send fish functionality
        print("Send fish")
        pass

    def closeEvent(self, event):
        self.mqtt_client.disconnect()
        super().closeEvent(event)
