import pandas as pd

# Load results
df = pd.read_csv("coap_results.csv")

# Group by file size
groups = df.groupby("file")

print("\n=== CoAP Performance Summary ===\n")
print(f"{'File':<8}{'Avg kbps':>12}{'Std Dev':>12}{'Overhead Ratio':>18}")
print("-" * 42)

for file, g in groups:
    avg_kbps = g["throughput_Bps"].mean() * 8 / 1000  # bytes/s -> kilobits/s
    std_kbps = g["throughput_Bps"].std() * 8 / 1000
    payload = g["payload_bytes"].iloc[0]
    overhead_ratio = (payload + 20) / payload  # 20 bytes CoAP header estimate

    print(f"{file:<8}{avg_kbps:>12.2f}{std_kbps:>12.2f}{overhead_ratio:>18.4f}")

print("\n✅ Copy these values to the Excel row for CoAP.")
