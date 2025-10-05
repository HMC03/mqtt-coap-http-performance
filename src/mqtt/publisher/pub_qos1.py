import paho.mqtt.client as mqtt
import time
import json
import os

BROKER = os.environ.get("MQTT_BROKER", "localhost")
TOPIC = "experiment/file"
QOS = 1
ITERATIONS = { "100B": 10000, "10KB": 1000, "1MB": 100, "10MB": 10 }
FILES_DIR = "../../../files"

def on_connect(client, userdata, flags, reason_code, properties=None):
    print("Connected with result code", reason_code)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect

print("Connecting to broker")
client.connect(BROKER, 1883, 60)
client.loop_start()  # starts a background network loop

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
        info = client.publish(TOPIC, json.dumps(payload), qos=QOS)
        if info.rc != mqtt.MQTT_ERR_SUCCESS:
            print("Publish failed with code:", info.rc, "For: ", file_name, i)
        else:
            info.wait_for_publish()
            print(t_send, "Sent", file_name, i)

print("Publisher done sending all files.")
client.loop_stop()
client.disconnect()
