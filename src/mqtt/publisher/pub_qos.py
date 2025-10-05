import paho.mqtt.client as mqtt
import time
import os
import struct

BROKER = os.environ.get("MQTT_BROKER", "localhost")
TOPIC_BASE = "files"
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

while True:
    qos_input = input("\nEnter QoS level (0, 1, or 2) or 'q' to quit: ").strip().lower()
    if qos_input == 'q':
        break
    if qos_input not in ('0', '1', '2'):
        print("Invalid input. Please enter 0, 1, 2, or q.")
        continue

    QOS = int(qos_input)
    print(f"\nStarting experiment run with QoS = {QOS}")

    for file_name, config in EXPERIMENTS.items():
        n_iter = config["iterations"]
        pause = config["pause"]

        path = os.path.join(FILES_DIR, file_name)
        with open(path, "rb") as f:
            file_bytes = f.read()

        topic = f"{TOPIC_BASE}/{file_name}"

        for i in range(n_iter):
            t_send = time.perf_counter()
            payload = struct.pack("dI", t_send, i) + file_bytes

            info = client.publish(topic, payload, qos=QOS)
            info.wait_for_publish()
            print(f"{t_send:.6f} Sent {file_name} iter {i}")

            time.sleep(pause)

    print(f"Finished all experiments for QoS = {QOS}")

print("\nGracefully disconnecting...")
client.loop_stop()
client.disconnect()
print("Publisher stopped cleanly.")