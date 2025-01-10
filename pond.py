import paho.mqtt.client as mqtt
import json
import time

# MQTT Server details
BROKER = "40.90.169.126"
PORT = 1883
USERNAME = "dc24"
PASSWORD = "kmitl-dc24"

GROUP_NAME = "DC Universe"

HELLO_TOPIC = "fishhaven/stream"

# Callback when connection to broker is established
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected to MQTT Broker at {BROKER}!")
        send_hello_message(client)  # Send hello message after connecting
        
        # Subscribe to pond announcements and fish spawning topics
        client.subscribe("fishhaven/stream")
        client.subscribe("pond/+/spawn")
    else:
        print(f"Failed to connect, return code {rc}\n")

# Function to send "hello" message
def send_hello_message(client):
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
    client.publish(HELLO_TOPIC, payload)
    print(f"Sent hello message: {payload}")
    
def receive_message(client, userdata, message):
    payload = json.loads(message.payload.decode())
    topic = message.topic
    if topic == "fishhaven/stream":
        print(f"New pond registered: {payload['type']}, {payload['sender']}, {payload['timestamp']}")
    elif "/spawn" in topic:
        print(f"Fish {payload['fish_id']} spawned in {payload['from_pond']}")

# Initialize MQTT client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client.username_pw_set(USERNAME, PASSWORD)
client.on_connect = on_connect
client.on_message = receive_message

# Connect to the MQTT broker
client.connect(BROKER, PORT)

# Start the client loop to maintain connection and send message
client.loop_forever()
