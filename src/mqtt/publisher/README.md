# MQTT File Publisher

## Purpose
Publishes raw binary files over MQTT for throughput and application-layer overhead experiments. Each message payload is binary and contains:
```css
[timestamp (8 bytes, double)][iteration (4 bytes, uint32)][file bytes]
```
This keeps payload size essentially equal to the original file size so protocol overhead (MQTT) can be measured accurately.

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
python3 pub_qos.py
```
Behavior:
* Prompts once at start to choose QoS (0, 1, or 2) or q to quit.
* Runs the full set of configured experiments (all file sizes) for the chosen QoS.
* Publishes each transfer on topic files/<file_name> with payload [timestamp][iteration][file bytes].
* Prints published messages to terminal with timestamp, file name, and iteration information
* Uses a short, configurable pause between messages to avoid queueing effects.
* Cleanly disconnects when the experiment set finishes.

NOTE: Start the subscriber before the publisher so messages are received (unless you intentionally want to test retention/late subscribers).