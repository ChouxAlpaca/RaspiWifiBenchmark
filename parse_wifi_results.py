import os, json, math, statistics
from datetime import datetime

logdir = os.path.expanduser("~/wifi_test_logs")
#Chia thời gian
blocks = {
    "00:00-05:59": range(0, 6),    # 0h-6h
    "06:00-11:59": range(6, 12),   # 6h-12h
    "12:00-17:59": range(12, 18),  # 12h-18h
    "18:00-23:59": range(18, 24)   # 18h-24h
}

# Data storage: 
data = {"wlan0": {}, "wlan1": {}}
for iface in data:
    for block in blocks:
        data[iface][block] = {"throughputs": [], "rtts": []}

# Helper: 
def get_block_label(dt):
    hr = dt.hour
    for label, hrs in blocks.items():
        if hr in hrs:
            return label
    return None

# Xử lý file log
for fname in os.listdir(logdir):
    if fname.endswith(".iperf") or fname.endswith(".ping"):
        # Filename format: wlanX_YYYYmmdd-HHMMSS.ext
        parts = fname.split("_", 1)
        if len(parts) < 2:
            continue
        iface = parts[0]        # "wlan0" or "wlan1"
        timestamp_str = parts[1].split(".",1)[0]  # e.g. "20250521-153000"
        try:
            dt = datetime.strptime(timestamp_str, "%Y%m%d-%H%M%S")
        except ValueError:
            continue
        block_label = get_block_label(dt)
        if block_label is None:
            continue

        filepath = os.path.join(logdir, fname)
        if fname.endswith(".iperf"):
            # Load JSON and extract throughput in Mbps
            with open(filepath, "r") as f:
                try:
                    result = json.load(f)
                except json.JSONDecodeError:
                    continue  # skip if any partial/incomplete file
                        bps = None
            try:
                bps = result["end"]["sum_received"]["bits_per_second"]
            except KeyError:
                try:
                    bps = result["end"]["sum_sent"]["bits_per_second"]
                except KeyError:
                    bps = None
            if bps is not None:
                mbps = bps / 1e6
                data[iface][block_label]["throughputs"].append(mbps)
        elif fname.endswith(".ping"):
            # Parse ping log to extract all RTTs (ms)
            with open(filepath, "r") as f:
                for line in f:
                    if " time=" in line:
                        try:
                            time_part = line.split("time=")[1]
                            ms_str = time_part.split(" ")[0]
                            rtt = float(ms_str)
                            data[iface][block_label]["rtts"].append(rtt)
                        except Exception:
                            continue
# Thống kê
output_lines = []
header = ("Time Range", "wlan0 Throughput (Mbps)", "wlan0 RTT (ms)", 
                      "wlan1 Throughput (Mbps)", "wlan1 RTT (ms)")
output_lines.append("{:<13} {:>25} {:>20} {:>25} {:>20}".format(*header))
output_lines.append("-" * 105)
for block_label in blocks.keys():
    for iface in ["wlan0", "wlan1"]:
        thr_list = data[iface][block_label]["throughputs"]
        rtt_list = data[iface][block_label]["rtts"]
        # Tính trung bình và độ lệch chuẩn
        if thr_list:
            thr_avg = statistics.mean(thr_list)
            thr_std = statistics.pstdev(thr_list) 
        else:
            thr_avg = 0.0
            thr_std = 0.0
        if rtt_list:
            rtt_avg = statistics.mean(rtt_list)
            rtt_std = statistics.pstdev(rtt_list)
        else:
            rtt_avg = 0.0
            rtt_std = 0.0
        data[iface][block_label]["thr_avg"] = thr_avg
        data[iface][block_label]["thr_std"] = thr_std
        data[iface][block_label]["rtt_avg"] = rtt_avg
        data[iface][block_label]["rtt_std"] = rtt_std
    wlan0_thr = f"{data['wlan0'][block_label]['thr_avg']:.1f} ± {data['wlan0'][block_label]['thr_std']:.1f}"
    wlan0_rtt = f"{data['wlan0'][block_label]['rtt_avg']:.1f} ± {data['wlan0'][block_label]['rtt_std']:.1f}"
    wlan1_thr = f"{data['wlan1'][block_label]['thr_avg']:.1f} ± {data['wlan1'][block_label]['thr_std']:.1f}"
    wlan1_rtt = f"{data['wlan1'][block_label]['rtt_avg']:.1f} ± {data['wlan1'][block_label]['rtt_std']:.1f}"
    output_lines.append(f"{block_label:<13} {wlan0_thr:>25} {wlan0_rtt:>20} {wlan1_thr:>25} {wlan1_rtt:>20}")

# In bảng
print("\n".join(output_lines))

# Lưu file .txt
result_path = os.path.join(logdir, "24h_summary_results.txt")
with open(result_path, "w") as fout:
    fout.write("\n".join(output_lines) + "\n")
print(f"\nSummary saved to {result_path}")
