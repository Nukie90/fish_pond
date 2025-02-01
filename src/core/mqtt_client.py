import json
import time
import paho.mqtt.client as mqtt
from config.settings import MQTT_CONFIG
from typing import Callable
import base64
from pathlib import Path
import os


class MqttClient:
    def __init__(self):
        self.broker = MQTT_CONFIG["BROKER"]
        self.port = MQTT_CONFIG["PORT"]
        self.username = MQTT_CONFIG["USERNAME"]
        self.password = MQTT_CONFIG["PASSWORD"]
        self.group_name = MQTT_CONFIG["GROUP_NAME"]
        self.hello_topic = MQTT_CONFIG["HELLO_TOPIC"]
        self.our_fish_topic = MQTT_CONFIG["OUR_FISH_TOPIC"]

        self._connected = False
        self.on_new_fish_callback: Callable = None

        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.username_pw_set(self.username, self.password)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

    def is_connected(self) -> bool:
        """Check if connected to MQTT broker"""
        return self._connected

    def set_new_fish_callback(self, callback: Callable):
        """Set callback for handling new fish from other ponds"""
        self.on_new_fish_callback = callback

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

    def _on_message(self, client, userdata, message, properties=None):
        try:
            payload = json.loads(message.payload.decode())
            topic = message.topic

            match topic:
                case self.hello_topic:
                    print(
                        f"New pond registered: {payload['type']}, {payload['sender']}, {payload['timestamp']}"
                    )
                    if payload["sender"] != self.group_name:
                        self.client.subscribe(f"user/{payload['sender']}", 0)

                case self.our_fish_topic:
                    print(
                        f"Received fish: {payload['name']} from {payload['group_name']}, lifetime: {payload['lifetime']}"
                    )

                    if self.on_new_fish_callback:
                        self.on_new_fish_callback(
                            name=payload.get("name", ""),
                            group_name=payload["group_name"],
                            lifetime=payload["lifetime"],
                            data=payload["data"],
                        )

        except Exception as e:
            print(f"Error processing message: {e}")

    def send_fish(
        self, name: str, group_name: str, lifetime: int, send_to: str, data: str
    ):
        """Send a fish to another pond"""
        message = {
            "name": name,
            "group_name": group_name,
            "lifetime": lifetime,
            "data": data,
        }

        topic = f"user/{send_to}"
        payload = json.dumps(message)
        print(f"Sending fish to topic: {topic}")
        print(
            f"Payload: {message['name']} {message['group_name']} {message['lifetime']}"
        )
        self.client.publish(topic, payload)
