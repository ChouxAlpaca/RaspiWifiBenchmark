Repo này sẽ tự động chạy iPerf3 và ping trong 24h để kiểm tra RTT và băng thông trên 2 wifi interfaces và tạo bảng tính means và độ lệch chuẩn <br>
# 1. Clone <br>
git clone https://github.com/ChouxAlpaca/RaspiWifiBenchmark.git <br>
cd wifi-test-24h 
<br>
# 2. Cài đặt <br>
./install.sh          
<br>

# 3. Thử nghiệm <br>
sudo systemctl start wifi24h.service <br>
<br>

# 4. Thống kê <br>
python3 parse_wifi_results.py#   R a s p i W i f i B e n c h m a r k  
 <br>
