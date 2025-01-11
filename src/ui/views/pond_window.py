from PySide6.QtWidgets import QMainWindow
from ui.generated.pond_ui import Ui_MainWindow
from core.mqtt_client import MqttClient


class PondWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.mqtt_client = MqttClient()

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
        # TODO: Implement add fish functionality
        print("Add fish")
        pass

    def handle_send_fish(self):
        # TODO: Implement send fish functionality
        print("Send fish")
        pass

    def closeEvent(self, event):
        self.mqtt_client.disconnect()
        super().closeEvent(event)
