import paho.mqtt.client as mqtt
import time
import os
import struct
import csv
import statistics
import threading

BROKER = os.environ.get("MQTT_BROKER", "localhost")
TOPIC_BASE = "files/#"
RESULTS_DIR = "../results"
os.makedirs(RESULTS_DIR, exist_ok=True)

received_log = {}  # (file_name, iteration) -> (elapsed, file_size, payload_size)
stop_flag = threading.Event()

def get_qos():
    """Prompt for QoS selection."""
    while True:
        try:
            q = int(input("Select QoS level (0, 1, or 2): "))
            if q in [0, 1, 2]:
                return q
            else:
                print("Invalid choice. Enter 0, 1, or 2.")
        except ValueError:
            print("Please enter a valid integer (0, 1, or 2).")

def keyboard_listener():
    """Wait for user to press 'q' to trigger log saving."""
    input("\nPress ENTER when publisher is done to log and analyze results...\n")
    stop_flag.set()

def on_connect(client, userdata, flags, reason_code, properties=None):
    print(f"Connected with result code {reason_code}, subscribing with QoS={QOS_LEVEL}")
    client.subscribe(TOPIC_BASE, qos=QOS_LEVEL)

def on_message(client, userdata, msg):
    t_receive = time.perf_counter()

    # Extract file_name from topic
    _, file_name = msg.topic.split("/")

    # Unpack timestamp + iteration
    t_send, iteration = struct.unpack("dI", msg.payload[:12])
    key = (file_name, iteration)

    if key in received_log:
        return  # duplicate

    file_bytes = msg.payload[12:]
    file_size = len(file_bytes)
    payload_size = len(msg.payload)
    elapsed = t_receive - t_send

    received_log[key] = (elapsed, file_size, payload_size)
    print(f"Received {file_name} iter {iteration}: elapsed={elapsed:.6f}s, "
          f"file_size={file_size}, payload_size={payload_size}")

def analyze_and_log():
    """Write CSV, compute statistics, print summary."""
    if not received_log:
        print("\nNo messages received, skipping log.")
        return

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    csv_path = os.path.join(RESULTS_DIR, f"mqtt_results_qos{QOS_LEVEL}_{timestamp}.csv")

    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["File Name", "Iteration", "Elapsed (s)", "File Size (bytes)",
                         "Payload Size (bytes)", "Throughput (kB/s)"])
        for (file_name, iteration), (elapsed, file_size, payload_size) in received_log.items():
            throughput = (file_size / elapsed) / 1000 if elapsed > 0 else 0
            writer.writerow([file_name, iteration, elapsed, file_size, payload_size, throughput])

    # Aggregate statistics
    results_by_file = {}
    for (file_name, _), (elapsed, file_size, payload_size) in received_log.items():
        throughput = (file_size / elapsed) / 1000 if elapsed > 0 else 0
        ratio = payload_size / file_size if file_size > 0 else 0
        if file_name not in results_by_file:
            results_by_file[file_name] = {"throughputs": [], "ratios": []}
        results_by_file[file_name]["throughputs"].append(throughput)
        results_by_file[file_name]["ratios"].append(ratio)

    print("\n=== MQTT Throughput Summary ===")
    print(f"{'File Name':<20}{'Avg Throughput (kB/s)':>25}{'Std Dev (kB/s)':>20}"
          f"{'Avg (Payload/File)':>25}")
    print("-" * 90)
    for file_name, data in results_by_file.items():
        avg_t = statistics.mean(data["throughputs"])
        std_t = statistics.stdev(data["throughputs"]) if len(data["throughputs"]) > 1 else 0
        avg_r = statistics.mean(data["ratios"])
        print(f"{file_name:<20}{avg_t:>25.2f}{std_t:>20.2f}{avg_r:>25.4f}")

    print(f"\nResults saved to {csv_path}")
    print("=" * 90 + "\n")

# --- Main Loop ---
while True:
    QOS_LEVEL = get_qos()

    received_log.clear()
    stop_flag.clear()

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message

    print(f"\nConnecting subscriber with QoS={QOS_LEVEL}")
    client.connect(BROKER, 1883, 60)

    # Run keyboard listener in separate thread
    threading.Thread(target=keyboard_listener, daemon=True).start()

    client.loop_start()

    # Wait until user signals to stop
    stop_flag.wait()

    client.loop_stop()
    client.disconnect()

    analyze_and_log()

    again = input("Run another test with a different QoS? (y/n): ").strip().lower()
    if again != "y":
        print("Exiting subscriber.")
        break