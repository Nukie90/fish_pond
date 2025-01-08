import paho.mqtt.client as mqtt
import json
import time

# MQTT Server details
BROKER = "localhost"
PORT = 1883
USERNAME = "dc24"
PASSWORD = "kmitl-dc24"

# Your group name
GROUP_NAME = "DC Universe"  # Change this to your actual group name

# Topic for sending "hello" message
HELLO_TOPIC = "vivisystem/hello"

# Callback when connection to broker is established
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected to MQTT Broker at {BROKER}!")
        send_hello_message(client)  # Send hello message after connecting
    else:
        print(f"Failed to connect, return code {rc}\n")

# Function to send "hello" message
def send_hello_message(client):
    # Get the current UNIX timestamp
    timestamp = int(time.time())

    # Create the message format
    message = {
        "type": "hello",
        "sender": GROUP_NAME,
        "timestamp": timestamp,
        "data": {}
    }

    # Convert the message to JSON
    payload = json.dumps(message)

    # Publish the message to the "hello" topic
    client.publish(HELLO_TOPIC, payload)
    print(f"Sent hello message: {payload}")

# Initialize MQTT client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client.username_pw_set(USERNAME, PASSWORD)
client.on_connect = on_connect

# Connect to the MQTT broker
client.connect(BROKER, PORT)

# Start the client loop to maintain connection and send message
client.loop_forever()
