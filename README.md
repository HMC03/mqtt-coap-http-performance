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

|  | Throughput (in kilo bits per second) |  |  |  |  |  |  |  | Total application layer data transferred from sender to receiver (including header content) per file divided by the file size |  |  |   |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
|  | 100B file |  | 10kB file |  | 1MB file |  | 10MB file |  | 100B file | 10kB file | 1MB file | 10MB file  |
|  | Average  | Std. Dev. | Average  | Std. Dev. | Average  | Std. Dev. | Average  | Std. Dev. | Average  | Average  | Average  | Average   |
| MQTT QoS1 | 52.36 | 11.24 | 2510.13 | 659.81 | 6077.99 | 2049.07 | 8857.61 | 1689.75 | 1.12 | 1.0012 | 1 | 1  |
| MQTT QoS2 | 18.67 | 6.93 | 1495.44 | 275.98 | 6918.71 | 2227.28 | 5763.7 | 752.51 | 1.12 | 1.0012 | 1 | 1  |
| CoAP |  |  |  |  |  |  |  |  |  |  |  |   |
| HTTP |  |  |  |  |  |  |  |  |  |  |  |   |

<h3>Performance Comparison</h3>

<table>
  <tr>
    <th rowspan="3">Protocol</th>
    <th colspan="8">Throughput (kbps)</th>
    <th colspan="4">Total Application Layer Data Transferred / File Size</th>
  </tr>
  <tr>
    <th colspan="2">100B File</th>
    <th colspan="2">10kB File</th>
    <th colspan="2">1MB File</th>
    <th colspan="2">10MB File</th>
    <th>100B File</th>
    <th>10kB File</th>
    <th>1MB File</th>
    <th>10MB File</th>
  </tr>
  <tr>
    <th>Avg</th><th>Std. Dev.</th>
    <th>Avg</th><th>Std. Dev.</th>
    <th>Avg</th><th>Std. Dev.</th>
    <th>Avg</th><th>Std. Dev.</th>
    <th>Avg</th><th>Avg</th><th>Avg</th><th>Avg</th>
  </tr>
  <tr>
    <td><b>MQTT QoS1</b></td>
    <td>52.36</td><td>11.24</td>
    <td>2510.13</td><td>659.81</td>
    <td>6077.99</td><td>2049.07</td>
    <td>8857.61</td><td>1689.75</td>
    <td>1.12</td><td>1.0012</td><td>1</td><td>1</td>
  </tr>
  <tr>
    <td><b>MQTT QoS2</b></td>
    <td>18.67</td><td>6.93</td>
    <td>1495.44</td><td>275.98</td>
    <td>6918.71</td><td>2227.28</td>
    <td>5763.7</td><td>752.51</td>
    <td>1.12</td><td>1.0012</td><td>1</td><td>1</td>
  </tr>
  <tr>
    <td><b>CoAP</b></td>
    <td colspan="12"></td>
  </tr>
  <tr>
    <td><b>HTTP</b></td>
    <td colspan="12"></td>
  </tr>
</table>