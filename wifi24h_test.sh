#!/usr/bin/env bash
# wifi24h_test.sh: 24-hour Wi-Fi throughput & ping test on wlan0 and wlan1

# Cài đặt IP và sever cloud
SERVER="ping.online.net" #Ta sử dụng sever public của iperf3
PORT="5201"                
IFACE1_NAME="wlan0"
IFACE1_IP= IP của wlan 0
IFACE2_NAME="wlan1"
IFACE2_IP= IP của wlan1

# Log 
LOGDIR="$HOME/wifi_test_logs"
mkdir -p "$LOGDIR"


echo "Starting 24h test at $(date) using server $SERVER:$PORT..." 
#Cài thời gian để phục vụ lập bảng cho bước sau
START_TIME=$(date +%s)
DURATION=$((24*3600))  # 

# Loop 24 tiếng
while [ $(($(date +%s) - START_TIME)) -lt $DURATION ]; do
    #wlan0
    timestamp=$(date +%Y%m%d-%H%M%S)
    echo "[$(date)] Running iperf3 (download) on $IFACE1_NAME..."
    iperf3 -c $SERVER -p $PORT -R -t 60 -B $IFACE1_IP -J \
           > "$LOGDIR/${IFACE1_NAME}_${timestamp}.iperf"
    echo "[$(date)] Running ping on $IFACE1_NAME..."
    ping -I $IFACE1_IP -c 60 $SERVER \
           > "$LOGDIR/${IFACE1_NAME}_${timestamp}.ping"

    # wlan1
    timestamp=$(date +%Y%m%d-%H%M%S)
    echo "[$(date)] Running iperf3 (download) on $IFACE2_NAME..."
    iperf3 -c $SERVER -p $PORT -R -t 60 -B $IFACE2_IP -J \
           > "$LOGDIR/${IFACE2_NAME}_${timestamp}.iperf"
    echo "[$(date)] Running ping on $IFACE2_NAME..."
    ping -I $IFACE2_IP -c 60 $SERVER \
           > "$LOGDIR/${IFACE2_NAME}_${timestamp}.ping"

echo "Test completed at $(date). Logs saved in $LOGDIR"
