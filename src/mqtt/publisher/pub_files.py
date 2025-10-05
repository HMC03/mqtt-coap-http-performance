import paho.mqtt.client as mqtt
import time
import os
import struct

BROKER = os.environ.get("MQTT_BROKER", "localhost")
TOPIC_BASE = "files"
QOS = 1
EXPERIMENTS = {
    "100B":  {"iterations": 10000, "pause": 0.01},
    "10KB":  {"iterations": 1000,  "pause": 0.05},
    "1MB":   {"iterations": 100,   "pause": 0.2},
    "10MB":  {"iterations": 10,    "pause": 1.0},
}
FILES_DIR = "../../../files"

def on_connect(client, userdata, flags, reason_code, properties=None):
    print("Connected with result code", reason_code)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect

print("Connecting to broker")
client.connect(BROKER, 1883, 60)
client.loop_start()

for file_name, config in EXPERIMENTS.items():
    n_iter = config["iterations"]
    pause = config["pause"]

    path = os.path.join(FILES_DIR, file_name)
    with open(path, "rb") as f:
        file_bytes = f.read()

    topic = f"{TOPIC_BASE}/{file_name}"  # topic per file only

    for i in range(n_iter):
        t_send = time.perf_counter()
        # Pack timestamp (8 bytes) + iteration (4 bytes) + file bytes
        payload = struct.pack("dI", t_send, i) + file_bytes

        info = client.publish(topic, payload, qos=QOS)
        info.wait_for_publish()

        print(t_send, "Sent", file_name, i)
        time.sleep(pause)

print("Publisher done sending all files.")

client.loop_stop()
client.disconnect()