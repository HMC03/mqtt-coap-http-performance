import paho.mqtt.client as mqtt
import time
import os
import struct

BROKER = os.environ.get("MQTT_BROKER", "localhost")
TOPIC_BASE = "files/#"
received_log = {}  # key: (file_name, iteration) -> value: (elapsed, file_size, payload_size)

def on_connect(client, userdata, flags, reason_code, properties=None):
    print("Connected with result code", reason_code)
    client.subscribe(TOPIC_BASE, qos=1)

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
          f"file_size={file_size}, payload_size={payload_size}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

print("Connecting subscriber")
client.connect(BROKER, 1883, 60)
client.loop_forever()