import paho.mqtt.client as mqtt
import json

BROKER = "localhost"
PORT = 1883

# Callback when connection to broker is established
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Vivisystem connected to MQTT Broker!")
        # Subscribe to pond announcements and fish spawning topics
        client.subscribe("vivisystem/hello")
        client.subscribe("pond/+/spawn")
    else:
        print("Failed to connect, return code %d\n", rc)

# Callback when a message is received
def on_message(client, userdata, message):
    payload = json.loads(message.payload.decode())
    topic = message.topic
    if topic == "vivisystem/hello":
        print(f"New pond registered: {payload['type']}, {payload['sender']}, {payload['timestamp']}")
    elif "/spawn" in topic:
        print(f"Fish {payload['fish_id']} spawned in {payload['from_pond']}")

# Initialize MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
client.connect(BROKER, PORT)

# Start the client loop
client.loop_forever()
