import paho.mqtt.client as mqtt
import json
import time


class MqttClient:
    def __init__(self, broker, port, username, password, group_name, hello_topic):
        # Initialize Object details
        self.broker = broker
        self.port = port
        self.username = username
        self.password = password
        self.group_name = group_name
        self.hello_topic = hello_topic

        # Initialize MQTT client
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
        self.client.username_pw_set(self.username, self.password)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.receive_message

    def connect(self):
        # Connect to the MQTT broker
        self.client.connect(self.broker, self.port)
        # Start the client loop to maintain connection and send message
        self.client.loop_forever()

    # Callback when connection to broker is established
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f"Connected to MQTT Broker at {BROKER}!")
            self.send_hello_message()  # Send hello message after connecting
            
            # Subscribe to pond announcements and fish spawning topics
            self.client.subscribe("fishhaven/stream")
            self.client.subscribe("pond/+/spawn")
        else:
            print(f"Failed to connect, return code {rc}\n")

    # Function to send "hello" message
    def send_hello_message(self):
        # Get the current UNIX timestamp
        timestamp = int(time.time())

        message = {
            "type": "hello",
            "sender": GROUP_NAME,
            "timestamp": timestamp,
            "data": {}
        }

        # Convert the message to JSON
        payload = json.dumps(message)

        # Publish the message to the "hello" topic
        self.client.publish(HELLO_TOPIC, payload)
        print(f"Sent hello message: {payload}")
    
    def receive_message(self, userdata, message):
        payload = json.loads(message.payload.decode())
        topic = message.topic
        if topic == "fishhaven/stream":
            print(f"New pond registered: {payload['type']}, {payload['sender']}, {payload['timestamp']}")
        elif "/spawn" in topic:
            print(f"Fish {payload['fish_id']} spawned in {payload['from_pond']}")

if __name__ == "__main__":
    # MQTT Server details
    BROKER = "40.90.169.126"
    PORT = 1883
    USERNAME = "dc24"
    PASSWORD = "kmitl-dc24"
    GROUP_NAME = "DC Universe"
    HELLO_TOPIC = "fishhaven/stream"

    #Construct the Mqtt object
    Mqtt = MqttClient(BROKER, PORT, USERNAME, PASSWORD, GROUP_NAME, HELLO_TOPIC)

    #Sent hello message
    Mqtt.connect()