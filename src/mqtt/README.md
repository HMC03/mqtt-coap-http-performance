# MQTT Experiments

This directory contains the MQTT setup used for comparing protocol performance.

## Structure
- `broker/` – Mosquitto broker setup and config
- `publisher/` – Publisher scripts and instructions
- `subscriber/` – Subscriber scripts and instructions

## Running MQTT Experiments
1. Set up and run the broker (`broker/README.md`).
2. Start the subscriber (`subscriber/README.md`).
3. Start the publisher (`publisher/README.md`) with the test files.
4. Ensure both QoS 1 and QoS 2 experiments are run (see publisher/subscriber docs).

For more details, see the README in each subdirectory.