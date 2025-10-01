# mqtt-coap-http-performance

## Overview

This project compares the performance of three communication protocols — MQTT, CoAP, and HTTP — when transferring files of different sizes across devices.

The experiments are designed to highlight differences in throughput and application layer overhead across protocols commonly used in IoT and networking.

## Project Structure
```bash
mqtt-coap-http-performance/
│── README.md              # Project overview and instructions
│── files/                 # Test files (100B, 10KB, 1MB, 10MB)
│── results/               # Raw logs and final Results.xlsx
│── src/                   # Source code
│   ├── mqtt/              # MQTT experiments (broker, publisher, subscriber)
│   ├── coap/              # CoAP experiments (server/client)
│   ├── http/              # HTTP experiments (server/client)
│── requirements.txt       # Python dependencies
│── Results File.xlsx      # Table for recording measurements
```

## Requirements
* **Hardware:** Up to three computers/VMs with Wi-Fi (e.g., laptops, Raspberry Pis, or smartphones) on the same local network.
* Software:
    * Python 3.x
    * Eclipse Mosquitto (MQTT broker)
    * paho-mqtt (MQTT client)

Install dependencies:
```bash
# install python virtual environment
sudo apt install python3-venv -y

# create a venv in the project
python3 -m venv venv

# activate venv
source venv/bin/activate   # Linux/macOS
# venv\Scripts\activate    # Windows

# install required Python packages
pip install -r requirements.txt
```

## Running Experiments
Each protocol follows the same experiment design:
| File Size | Transfers |
|-----------|:---------:|
| 100 B     | 10,000    |
| 10 KB     | 1,000     |
| 1 MB      | 100       |
| 10 MB     | 10        |

For every transfer:
* Record transfer time programmatically
* Compute throughput = file_size / transfer_time
* Log results for later analysis in Results File.xlsx

Protocol Setup
* MQTT (QoS 1 & QoS 2) → Requires a broker, publisher, and subscriber.
* CoAP → Requires a server and client (confirmable + block transfer).
* HTTP → Requires a server and client.

Detailed instructions and commands are provided in the corresponding directories:
* src/mqtt/README.md
* src/coap/README.md
* src/http/README.md

## Results
TBD