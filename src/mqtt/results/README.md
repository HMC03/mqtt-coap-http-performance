# Results Directory
This directory stores all MQTT experiment output files and provides a script to analyze them

## Overview
| File / Folder                       | Description                                                                                                                                                                 |
| ----------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `mqtt_results_qosX_<timestamp>.csv` | Automatically generated result files created by the subscriber after each experiment run. Contain detailed message-level logs for each file type, QoS level, and iteration. |
| `analyze_results.py`                | Python script that aggregates and summarizes data from all result `.csv` files in this directory.                                                                           |
| `README.md`                         | Documentation for how to interpret and analyze results.                                                                                                                     |


## CSV Data Structure
Each .csv file contains one row per message received:
| Column                   | Description                                                             |
| ------------------------ | ----------------------------------------------------------------------- |
| **File Name**            | Name of the transmitted file (e.g., `100B`, `10KB`, `1MB`, `10MB`).     |
| **Iteration**            | Sequential message index for that file.                                 |
| **Elapsed (s)**          | One-way latency between send and receive timestamps.                    |
| **File Size (bytes)**    | Size of the original file payload.                                      |
| **Payload Size (bytes)** | Total MQTT message size including header and metadata.                  |
| **Throughput (kB/s)**    | Calculated throughput for that message: `(file_size / elapsed) / 1000`. |

## Analyzing Results
Run the analysis script after you;ve completed one or more MQTT experiments:
```bash
cd src/mqtt/results
python3 analyze_results.py
```

## Output Example
After execution, the script scans all `.csv` files in this directory and prints a formatted summary to the terminal, grouped by file name and CSV file.

Example output:
```yaml
=== MQTT Throughput Summary (Aggregated Results) ===

mqtt_results_qos1_20251005_190246.csv Results:
File Name                    Avg Throughput (kB/s)      Std Dev (kB/s)       Avg (Payload/File)
-----------------------------------------------------------------------------------------------
100B                                         52.36               11.24                   1.1200
10KB                                       2510.13              659.81                   1.0012
1MB                                        6077.99             2049.07                   1.0000
10MB                                       8857.61             1689.75                   1.0000

mqtt_results_qos2_20251005_190946.csv Results:
File Name                    Avg Throughput (kB/s)      Std Dev (kB/s)       Avg (Payload/File)
-----------------------------------------------------------------------------------------------
100B                                         18.67                6.93                   1.1200
10KB                                       1495.44              275.98                   1.0012
1MB                                        6918.71             2227.28                   1.0000
10MB                                       5763.70              752.51                   1.0000

Analysis complete.
==========================================================================================
```

## Metrics Explained
| Metric                    | Meaning                                                                                       |
| ------------------------- | --------------------------------------------------------------------------------------------- |
| **Avg Throughput (kB/s)** | Average transmission speed for all iterations of that file type.                              |
| **Std Dev (kB/s)**        | Variability in throughput across all iterations.                                              |
| **Avg (Payload/File)**    | Average ratio of total MQTT payload size to original file size (indicates protocol overhead). |


## Notes
* Each run of the subscriber script creates a new timestamped .csv file
* You can safely delete old result files once analyzed
* The script automatically processes all .csv files found in the directory.
