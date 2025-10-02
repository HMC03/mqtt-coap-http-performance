import paho.mqtt.client as mqtt
import time
import os
import csv
import json
import statistics

BROKER = os.environ.get("MQTT_BROKER", "localhost")
TOPIC = "experiment/file"
RESULTS_DIR = "../results"
os.makedirs(RESULTS_DIR, exist_ok=True)

results = {}  # { "100B_qos1": [ {"elapsed":..., "file_size_bytes":..., "total_bytes":...} ] }

def on_message(client, userdata, msg):
    t_receive = time.perf_counter()

    # Minimal decoding
    payload_meta = json.loads(msg.payload.decode("utf-8"))
    file_name = payload_meta["file_name"]
    iteration = payload_meta["iteration"]
    t_send = payload_meta["timestamp"]
    file_size_bytes = len(payload_meta["data"].encode("latin1"))

    key = f"{file_name}_qos{msg.qos}"
    if key not in results:
        results[key] = []

    results[key].append({
        "elapsed": t_receive - t_send,
        "file_size_bytes": file_size_bytes,
        "total_bytes": len(msg.payload)  # total application-layer bytes
    })

# MQTT setup
client = mqtt.Client()
client.on_message = on_message
client.connect(BROKER, 1883, 60)
client.subscribe(TOPIC, qos=1)

print("Subscriber running... Ctrl+C to stop.")
try:
    client.loop_forever()
except KeyboardInterrupt:
    print("Subscriber stopping...")

# -------------------
# Post-run aggregation
summary_csv = os.path.join(RESULTS_DIR, "summary.csv")
with open(summary_csv, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["file_name", "qos", "trials",
                     "avg_throughput_kbps", "std_throughput_kbps",
                     "avg_overhead_ratio"])

    for key, trials in results.items():
        file_name, qos_str = key.split("_qos")
        qos = int(qos_str)

        throughputs = [(t["file_size_bytes"]*8)/t["elapsed"]/1000 for t in trials]  # kbps
        avg_throughput = statistics.mean(throughputs)
        std_throughput = statistics.stdev(throughputs)
        overhead_ratios = [t["total_bytes"]/t["file_size_bytes"] for t in trials]
        avg_overhead = statistics.mean(overhead_ratios)

        writer.writerow([file_name, qos, len(trials),
                         avg_throughput, std_throughput, avg_overhead])

print(f"Summary CSV written to {summary_csv}")

# Optional JSON backup
json_backup = os.path.join(RESULTS_DIR, "results_backup.json")
with open(json_backup, "w") as f:
    json.dump(results, f)
print(f"Raw results JSON written to {json_backup}")
