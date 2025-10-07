import socket
import time
import os
import statistics
import csv
from dotenv import load_dotenv

load_dotenv(".env")
SERVER_HOST = os.getenv("SERVER_HOST")
SERVER_PORT = os.getenv("SERVER_PORT")

def get_data(host, port, file_path):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)

    # Total received bytes per file.
    total_bytes_received = 0

    try:
        start = time.time()

        sock.connect((host, int(port)))
        # GET Request format
        request = (
            f"GET /{file_path} HTTP/1.1\r\n"
            f"Host: {host}:{port}\r\n"
            f"Connection: close\r\n"
            f"\r\n"
        )

        sock.sendall(request.encode())

        response_data = b""
        while True:
            chunk = sock.recv(8192)
            if not chunk:
                break
            response_data += chunk
            total_bytes_received += len(chunk)

        elapsed = time.time() - start

        if b"200 OK" in response_data[:100]:
            return response_data, elapsed, total_bytes_received
        else:
            return None, 0, 0
    except Exception as e:
        print(f"Error: {e}")
        return None, 0, 0
    finally:
        sock.close()

def get_file_size(file_name):
    # File sizes were based on the given files in /files/ in root directory of repo.   
    if file_name == "100B":
        return 100
    elif file_name == "10KB":
        return 10240
    elif file_name == "1MB":
        return 1048576
    elif file_name == "10MB":
        return 10320162
    else:
        return 0

def calculate_metrics(file_size, elapsed_list, bytes_received_list):
    throughputs = []
    overhead_ratios = []

    for elapsed, bytes_received_size in zip(elapsed_list, bytes_received_list):
        throughput = (file_size * 8) / (elapsed * 1000) # Kilobits per second
        throughputs.append(throughput)

        overhead_ratio = bytes_received_size / file_size
        overhead_ratios.append(overhead_ratio)

    return statistics.mean(throughputs), statistics.stdev(throughputs), statistics.mean(overhead_ratios)

def results_to_csv(results_list):
    with open('results.csv', 'w', newline='') as csvfile:
        fieldnames = ['File', 'Avg Throughput (kbps)', 'Std Dev Throughput (kbps)', 'Avg Overhead Ratio']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for result in results_list:
            writer.writerow(result)

if __name__ == "__main__":
    # Stores results into a list to be exported into csv.
    results = []

    # Dictionary (key: file name, value: number of iterations)
    files = {
        "100B": 10000,
        "10KB": 1000,
        "1MB": 100,
        "10MB": 10,
    }

    print(f"{'='*60}")
    print(f"Files to be transferred: {files}")
    print(f"{'='*60}")

    for file, iter_count in files.items():
        print(f"\nConnecting to {SERVER_HOST}:{SERVER_PORT}...")
        print(f"Requesting file: /{file}...")

        times_elapsed = []
        bytes_received = []

        for nums in range(iter_count):
            data, time_elapsed, total_bytes = get_data(SERVER_HOST, SERVER_PORT, file)
            if data:
                times_elapsed.append(time_elapsed)
                bytes_received.append(total_bytes)

                if (nums % 20) == 0:
                    print(f"Epoch: {nums} -- Time elapsed: {time_elapsed} seconds")
                    print(f"Total bytes received: {total_bytes}")
            else:
                print(f"Miss at runs {nums} for file: /{file}")

        avg_throughput, std_throughput, avg_overhead_ratio = calculate_metrics(get_file_size(file), times_elapsed, bytes_received)

        print(f"Results for file: /{file}")
        print(f"Average throughput: {avg_throughput} Kbps")
        print(f"Standard deviation of throughput: {std_throughput} Kbps")
        print(f"Average overhead ratio: {avg_overhead_ratio}\n")

        results.append({
            'File': file,
            'Avg Throughput (kbps)': avg_throughput,
            'Std Dev Throughput (kbps)': std_throughput,
            'Avg Overhead Ratio': avg_overhead_ratio
        })

    write_to_csv = input("Do you want to write results to csv? (y/n): ")
    if write_to_csv.lower() == "y":
        results_to_csv(results)
        print("\nResults exported to results.csv")
    else:
        print("\nResults not exported to csv.")

    print(f"\n{'=' * 60}")
    print("Test completed.")
    print(f"{'=' * 60}")

