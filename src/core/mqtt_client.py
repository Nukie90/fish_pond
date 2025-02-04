import json
import time
import paho.mqtt.client as mqtt
from config.settings import MQTT_CONFIG


class MqttClient:
    def __init__(self, pond_window):
        self.pond_window = pond_window
        self.broker = MQTT_CONFIG["BROKER"]
        self.port = MQTT_CONFIG["PORT"]
        self.username = MQTT_CONFIG["USERNAME"]
        self.password = MQTT_CONFIG["PASSWORD"]
        self.group_name = MQTT_CONFIG["GROUP_NAME"]
        self.hello_topic = MQTT_CONFIG["HELLO_TOPIC"]
        self.our_fish_topic = MQTT_CONFIG["OUR_FISH_TOPIC"]

        self._connected = False

        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.username_pw_set(self.username, self.password)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

    def is_connected(self) -> bool:
        """Check if connected to MQTT broker"""
        return self._connected

    def connect(self):
        self.client.connect(self.broker, self.port)
        self.client.loop_start()

    def disconnect(self):
        self._connected = False
        self.client.loop_stop()
        self.client.disconnect()

    def _on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0:
            print(f"Connected to MQTT Broker at {self.broker}!")
            self._connected = True
            self._send_hello_message()
            self.client.subscribe(
                [
                    ("fishhaven/stream", 0),
                    ("user/DC_Universe", 0),
                ]
            )
        else:
            print(f"Failed to connect, return code {rc}")
            self._connected = False

    def _send_hello_message(self):
        message = {
            "type": "hello",
            "sender": self.group_name,
            "timestamp": int(time.time()),
            "data": {},
        }

        payload = json.dumps(message)

        self.client.publish(self.hello_topic, payload)
        print(f"Sent hello message: {payload}")

    def send_fish(self, name: str, group_name: str, lifetime: int, send_to: str):
        """Send a fish to another pond"""
        message = {
            "name": name,
            "group_name": group_name,
            "lifetime": lifetime,
        }

        topic = f"user/{send_to}"
        payload = json.dumps(message)
        print(f"Sending fish to topic: {topic}")
        self.client.publish(topic, payload)

    def _on_message(self, client, userdata, message):
        """Handle incoming MQTT messages"""
        try:
            match message.topic:
                case self.hello_topic:
                    payload = json.loads(message.payload.decode())
                    sender = payload["sender"]
                    if sender != self.group_name:  # Don't add ourselves
                        print(
                            f"New pond registered: {payload['type']}, {sender}, {payload['timestamp']}"
                        )
                        self.pond_window.pond.add_connected_pond(sender)
                case self.our_fish_topic:
                    payload = json.loads(message.payload.decode())
                    print(payload)
                    print(
                        f"Received fish: {payload['name']} {payload['group_name']} {payload['lifetime']}"
                    )
                    self.pond_window.fish_received.emit(payload)

        except Exception as e:
            print(f"Error handling message: {str(e)}")
