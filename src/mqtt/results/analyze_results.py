import os
import csv
import statistics

RESULTS_DIR = os.path.dirname(__file__) 

def analyze_csv(file_path):
    """Analyze a single CSV file and return per-file statistics."""
    results_by_file = {}
    with open(file_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                file_name = row["File Name"]
                elapsed = float(row["Elapsed (s)"])
                file_size = float(row["File Size (bytes)"])
                payload_size = float(row["Payload Size (bytes)"])
                if elapsed <= 0:
                    continue
                throughput = (file_size / elapsed) / 1000  # kB/s
                ratio = payload_size / file_size if file_size > 0 else 0

                if file_name not in results_by_file:
                    results_by_file[file_name] = {"throughputs": [], "ratios": []}
                results_by_file[file_name]["throughputs"].append(throughput)
                results_by_file[file_name]["ratios"].append(ratio)
            except (ValueError, KeyError):
                print(f"  Skipping row in {file_path}: {row}")
                continue

    return results_by_file


def summarize_results(results_by_file):
    """Print summary statistics for each file name."""
    print(f"{'File Name':<25}{'Avg Throughput (kB/s)':>25}{'Std Dev (kB/s)':>20}{'Avg (Payload/File)':>25}")
    print("-" * 90)
    for file_name, data in results_by_file.items():
        throughputs = data["throughputs"]
        ratios = data["ratios"]
        avg_t = statistics.mean(throughputs)
        std_t = statistics.stdev(throughputs) if len(throughputs) > 1 else 0
        avg_r = statistics.mean(ratios)
        print(f"{file_name:<25}{avg_t:>25.2f}{std_t:>20.2f}{avg_r:>25.4f}")
    print()


def main():
    csv_files = [f for f in os.listdir(RESULTS_DIR) if f.endswith(".csv")]
    if not csv_files:
        print("No CSV data found in results directory.")
        return

    print("\n=== MQTT Throughput Summary (Aggregated Results) ===\n")

    for file_name in sorted(csv_files):
        file_path = os.path.join(RESULTS_DIR, file_name)
        results = analyze_csv(file_path)
        if not results:
            print(f"No valid rows found in {file_name}")
            continue

        print(f"{file_name} results:")
        summarize_results(results)

    print("Analysis complete.")
    print("=" * 90)


if __name__ == "__main__":
    main()
