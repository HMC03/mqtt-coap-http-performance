# MQTT File Subscriber

## Purpose
Receives raw binary file transfers from the publisher, extracts the embedded timestamp and iteration, logs each transfer, saves results to CSV, and prints per-file statistics (average throughput, standard deviation, and payload/file ratio).

## Setup
**Broker**

Make sure you start the broker and get its ip by following the instructions found in `src/mqtt/broker/README.md`

**Virtual Environment**

```bash
# go to project root
cd ../../../

# create & activate venv (run this once)
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```
`requirements.txt` is in the project root and includes dependency `paho-mqtt`

**Environment Variable**
```bash
export MQTT_BROKER=<your_broker_ip>
```

## How to Run
```bash
# Follow setup instructions
python3 sub_qos.py
```
Behavior:
* Prompts once for QoS (0, 1, or 2) and subscribes to files/# using that QoS.
* For each incoming message:
    * Parses first 8 bytes as t_send (double), next 4 bytes as iteration (uint32), remaining bytes are file bytes.
    * Records t_receive, elapsed = t_receive - t_send, file_size, and payload_size.
    * Drops duplicates using (file_name, iteration).
* When the publisher run is complete, press ENTER in the subscriber terminal to:
    * Write all records to a CSV in results/ (filename includes QoS and timestamp).
    * Print a per-file summary: average throughput (kB/s), standard deviation, and average payload/file ratio.
    * After analysis, the subscriber clears its in-memory log and asks whether to run another test with a different QoS.
NOTE: Start the subscriber before the publisher so messages are received (unless you intentionally want to test retention/late subscribers).

## CSV output format
Saved as `results/mqtt_results_qos<level>_<YYYYMMDD_HHMMSS>.csv` with columns
```scss
File Name, Iteration, Elapsed (s), File Size (bytes), Payload Size (bytes), Throughput (kB/s)
```
**What the statistics mean**
* Throughput (kB/s) = `file_size / elapsed / 1000.`
* Avg payload/file ratio = `payload_size / file_size` averaged across iterations (should be close to 1.000... using this experiment format).
* Standard deviation is computed across throughput samples for each file type.