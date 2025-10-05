import asyncio
import csv
import time
from aiocoap import Context, Message, GET

OUT_CSV = "coap_results.csv"

NUM_RUNS = {
    "100B": 3,
    "10KB": 3,
    "1MB": 2,
    "10MB": 1
}

async def fetch_file(context, uri, fname, iteration):
    start = time.perf_counter()
    try:
        response = await context.request(Message(code=GET, uri=uri)).response
        end = time.perf_counter()
        payload_len = len(response.payload)
        duration = end - start
        throughput = payload_len / duration if duration > 0 else 0
        print(f"[{fname} #{iteration}] {payload_len} bytes in {duration:.4f}s → {throughput/1024:.2f} KB/s")
        return {
            "file": fname,
            "iteration": iteration,
            "payload_bytes": payload_len,
            "duration_s": duration,
            "throughput_Bps": throughput,
            "timestamp": time.time(),
        }
    except Exception as e:
        print(f"[{fname} #{iteration}] ❌ Error: {e}")
        return {
            "file": fname,
            "iteration": iteration,
            "payload_bytes": 0,
            "duration_s": None,
            "throughput_Bps": 0,
            "timestamp": time.time(),
        }

async def main():
    server_ip = "127.0.0.1"
    files = ["100B", "10KB", "1MB", "10MB"]
    context = await Context.create_client_context()

    results = []
    for fname in files:
        uri = f"coap://{server_ip}/{fname}"
        for i in range(1, NUM_RUNS[fname] + 1):
            record = await fetch_file(context, uri, fname, i)
            results.append(record)
            await asyncio.sleep(0.5)

    header = ["file", "iteration", "payload_bytes", "duration_s", "throughput_Bps", "timestamp"]
    with open(OUT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(results)

    print(f"\n✅ Results saved to {OUT_CSV}")

if __name__ == "__main__":
    asyncio.run(main())
