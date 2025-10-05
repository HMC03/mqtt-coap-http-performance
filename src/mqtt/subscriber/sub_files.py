import paho.mqtt.client as mqtt
import time
import os
import struct

BROKER = os.environ.get("MQTT_BROKER", "localhost")
TOPIC_BASE = "files/#"
received_log = {}  # key: (file_name, iteration) -> value: (elapsed, file_size, payload_size)

# --- QoS selection ---
while True:
    try:
        QOS_LEVEL = int(input("Select QoS level (0, 1, or 2): "))
        if QOS_LEVEL in [0, 1, 2]:
            break
        else:
            print("Invalid choice. Enter 0, 1, or 2.")
    except ValueError:
        print("Please enter a valid integer (0, 1, or 2).")

def on_connect(client, userdata, flags, reason_code, properties=None):
    print(f"Connected with result code {reason_code}, subscribing with QoS={QOS_LEVEL}")
    client.subscribe(TOPIC_BASE, qos=QOS_LEVEL)

def on_message(client, userdata, msg):
    t_receive = time.perf_counter()

    # extract file_name from topic
    _, file_name = msg.topic.split("/")

    # unpack timestamp + iteration
    t_send, iteration = struct.unpack("dI", msg.payload[:12])
    key = (file_name, iteration)

    if key in received_log:
        return  # duplicate, ignore

    file_bytes = msg.payload[12:]
    file_size = len(file_bytes)
    payload_size = len(msg.payload)
    elapsed = t_receive - t_send

    received_log[key] = (elapsed, file_size, payload_size)
    print(f"Received {file_name} iter {iteration}: elapsed={elapsed:.6f}s, "
          f"file_size={file_size}, payload_size={payload_size}, qos={QOS_LEVEL}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

print(f"Connecting subscriber with QoS={QOS_LEVEL}")
client.connect(BROKER, 1883, 60)
client.loop_forever()
