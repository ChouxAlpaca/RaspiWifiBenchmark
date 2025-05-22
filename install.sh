cat > install.sh <<'EOF'
#!/usr/bin/env bash
set -e
echo "Installing dependencies…"
sudo apt update
sudo apt install -y iperf3 python3 git netcat-openbsd
sudo cp wifi24h.service /etc/systemd/system/
sudo systemctl daemon-reload
echo "Thay đổi phần Config trong file setup bằng IP của wlan0 và wlan1."
EOF
chmod +x install.sh
