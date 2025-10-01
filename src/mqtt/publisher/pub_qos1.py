import paho.mqtt.client as mqtt
import time
import json
import os

BROKER = os.environ.get("MQTT_BROKER", "localhost")
TOPIC = "experiment/file"
QOS = 1
ITERATIONS = { "100B": 10000, "10kB": 1000, "1MB": 100, "10MB": 10 }
FILES_DIR = "../../../files"

client = mqtt.Client()
client.connect(BROKER, 1883, 60)

for file_name, n_iter in ITERATIONS.items():
    path = os.path.join(FILES_DIR, file_name)
    with open(path, "rb") as f:
        file_bytes = f.read()

    for i in range(n_iter):
        t_send = time.perf_counter()  # timestamp at sending
        payload = {
            "file_name": file_name,
            "iteration": i,
            "timestamp": t_send,  # for accurate elapsed time measurement
            "data": file_bytes.decode("latin1")  # minimal serialization
        }
        client.publish(TOPIC, json.dumps(payload), qos=QOS)

print("Publisher done sending all files.")
client.disconnect()
