# Hướng dẫn cấu hình con người kỹ thuật số tất cả trong một

Dự án này được sử dụng để triển khai hệ thống hiển thị con người kỹ thuật số hoàn chỉnh trên các thiết bị kiến trúc x86 (như máy chủ mini, máy tính công nghiệp, máy tính thông thường, v.v.) nhằm đạt được các chức năng sau:
- Tự động vào trình duyệt toàn màn hình Kiosk khi khởi động, hiển thị trang web được chỉ định
- Chạy dịch vụ phát hiện từ đánh thức ở chế độ nền và hỗ trợ tương tác bằng giọng nói

> **Lưu ý**: Tài liệu này sử dụng **Máy chủ mini Intel N100 (Texhong QN10-100B4)** làm ví dụ cho minh họa triển khai. Các thiết bị x86 khác có thể được điều chỉnh làm tài liệu tham khảo (lưu ý sự khác biệt về cấu hình mạng và thiết bị card âm thanh).

## Môi trường áp dụng

| Dự án | Mô tả |
|------|------|
| Phần cứng mẫu | Cầu vồng QN10-100B4 (Intel N100) |
| Hệ điều hành | Ubuntu 24.04 LTS (Numbat cao quý) |
| Người dùng mẫu | xz (vui lòng thay thế theo tình hình thực tế) |
| Mạng | Kết nối Wi-Fi, IP cố định (có thể đổi sang có dây nếu cần) |

##Quy trình triển khai

1. Khởi tạo hệ thống (đổi nguồn, kết nối mạng)
2. Cài đặt các thành phần đồ họa và trình duyệt Kiosk
3. Cấu hình đăng nhập tự động và giao diện đồ họa
4. Triển khai dịch vụ Wake Word (Môi trường Python + micrô)
5. Tối ưu tốc độ khởi động và ẩn thông tin khởi động

---


### Khởi tạo hệ thống (đổi nguồn, kết nối mạng)

```
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak

sudo tee /etc/apt/sources.list > /dev/null <<EOF
deb http://mirrors.aliyun.com/ubuntu/ noble main restricted universe multiverse
# deb-src http://mirrors.aliyun.com/ubuntu/ noble main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ noble-security main restricted universe multiverse
# deb-src http://mirrors.aliyun.com/ubuntu/ noble-security main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ noble-updates main restricted universe multiverse
# deb-src http://mirrors.aliyun.com/ubuntu/ noble-updates main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ noble-proposed main restricted universe multiverse
# deb-src http://mirrors.aliyun.com/ubuntu/ noble-proposed main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ noble-backports main restricted universe multiverse
# deb-src http://mirrors.aliyun.com/ubuntu/ noble-backports main restricted universe multiverse
EOF

echo 'Acquire::ForceIPv4 "true";' | sudo tee /etc/apt/apt.conf.d/99force-ipv4
```


Cài đặt các công cụ quản lý mạng (bỏ qua nếu chúng đã tồn tại)

Bash

```
sudo apt update
sudo apt install network-manager -y
sudo systemctl start NetworkManager
sudo systemctl enable NetworkManager
```


Đặt mật khẩu wifi và sửa ip

> **Nhắc nhở**: Tên Wi-Fi, mật khẩu và địa chỉ IP trong các lệnh sau chỉ là ví dụ, vui lòng đảm bảo thay thế chúng bằng thông tin thực tế của riêng bạn.

Bash

```
sudo nmcli device wifi connect "MERCURY_1812" password "12345678"

sudo nmcli connection modify "MERCURY_1812" ipv4.addresses "192.168.0.86/24" ipv4.gateway "192.168.0.1" ipv4.dns "8.8.8.8,114.114.114.114" ipv4.method "manual"

sudo nmcli connection up "MERCURY_1812"
```


### Bước 1: Cài đặt các thành phần đồ họa cốt lõi và trình duyệt

Ở đây chúng tôi tuân thủ "chủ nghĩa tối giản" và kiên quyết không cài đặt các môi trường máy tính để bàn dư thừa (chẳng hạn như Gnome/KDE). Chúng tôi chỉ cài đặt trình điều khiển cấp thấp, trình quản lý cửa sổ nhẹ nhất (Openbox), công cụ chuột ẩn và trình duyệt Chrome.

Bash

```
sudo timedatectl set-timezone Asia/Shanghai


sudo apt install net-tools vim fonts-wqy-microhei fonts-wqy-zenhei alsa-utils pulseaudio -y
sudo apt install --no-install-recommends xserver-xorg x11-xserver-utils xinit openbox unclutter -y

wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb -y
rm google-chrome-stable_current_amd64.deb

sudo apt purge snapd -y

```

### Bước 2: Cấu hình TTY1 tự động đăng nhập không cần mật khẩu khi khởi động

Để tránh bối rối khi nhập mật khẩu tài khoản theo cách thủ công, chúng tôi đã sửa đổi dịch vụ systemd để hệ thống tự động đăng nhập với tên `xz` ngay khi bật nguồn. Lệnh ghi bằng một cú nhấp chuột được sử dụng ở đây để tránh hoàn toàn vấn đề lưu không thành công do hoạt động không đúng của `nano` hoặc `vi`.

**1. Tạo thư mục cấu hình:**

Bash

```
sudo mkdir -p /etc/systemd/system/getty@tty1.service.d/
```

**2. Viết quy tắc đăng nhập tự động:**

Bash

```
echo -e "[Service]\nExecStart=\nExecStart=-/sbin/agetty --autologin xz --noclear %I \$TERM" | sudo tee /etc/systemd/system/getty@tty1.service.d/override.conf
```

**3. Tải lại dịch vụ và đặt mục tiêu khởi động mặc định:**

Bash

```
sudo systemctl daemon-reload
sudo systemctl set-default multi-user.target
```

### Bước 3: Cấu hình giao diện đồ họa tự động khởi động sau khi đăng nhập

Hệ thống sau khi tự động đăng nhập sẽ mặc định ở dòng lệnh với ký tự màu trắng trên nền đen. Chúng ta cần định cấu hình tập lệnh để nó khởi động môi trường đồ họa X11 ngay sau khi đăng nhập.

**1. Kích hoạt logic khởi động của `startx`: **

Nối trực tiếp mã kích hoạt vào tệp cấu hình môi trường cá nhân của bạn:

Bash

```
cat << 'EOF' >> ~/.bash_profile
if [ -z "$DISPLAY" ] && [ "$(fgconsole)" -eq 1 ]; then
    exec startx
fi
EOF
```

**2. Yêu cầu `startx` khởi động Openbox: **

Bash

```
echo "exec openbox-session" > ~/.xinitrc
```

### Bước 4: Cấu hình Openbox và trình duyệt “bức tường sắt”

Đây là bước cốt lõi: tắt chế độ ngủ màn hình, ẩn chuột, khóa trình duyệt ở chế độ toàn màn hình và viết "vòng lặp vô hạn" để đảm bảo trình duyệt có thể được phục hồi ngay lập tức sau khi vô tình bị đóng.

**1. Tạo thư mục cấu hình Openbox:**

Bash

```
mkdir -p ~/.config/openbox
```

**2. Viết đoạn script tự khởi động (`autostart`): **

Sao chép toàn bộ mã bên dưới và nhấn Enter (điều này sẽ tự động ghi tất cả các quy tắc bảo vệ vào tệp):

Bash

```
mèo << 'EOF' > ~/.config/openbox/autostart
# Tắt trình bảo vệ màn hình
xset-dpms
xset s noblank
xsetsoff

# Ẩn chuột
dọn dẹp -nhàn rỗi 0,1 -root &

# Khởi động Chrome theo vòng lặp vô hạn (có thể khởi động lại sau vài giây ngay cả khi nó gặp sự cố hoặc bị tắt)
trong khi đúng; làm
    google-chrome\
        --kiosk\
        --không chạy lần đầu \
        --no-mặc định-kiểm tra trình duyệt \
        --disable-infobars \
        --disable-session-crashed-bubble \
        --disable-dịch \
        --disable-external-intent-requests \
        --autoplay-policy=no-user-gesture-required \
        --use-fake-ui-for-media-stream \
        "https://www.douyin.com"
    ngủ 2
xong &
EOF
```

**3. Phím tắt thoát Shield `Alt+F4`: **

Để ngăn người khác cắm bàn phím và buộc đóng cửa sổ, chúng tôi đã loại bỏ các phím tắt hệ thống mặc định của Openbox.

Bash

```
cp /etc/xdg/openbox/rc.xml ~/.config/openbox/
sed -i '/<keybind key="A-F4">/,/<\/keybind>/d' ~/.config/openbox/rc.xml
```

### Bước 5: Khởi động lại kết quả nghiệm thu

Nếu bạn rút cáp mạng hoặc không cần đợi tất cả các mạng trực tuyến, bạn có thể tắt dịch vụ chờ mạng để tránh tình trạng khởi động chậm.

Bash

```
sudo systemctl mask systemd-networkd-wait-online.service
sudo systemctl mask NetworkManager-wait-online.service
```

Ẩn thông tin khởi động (GRUB)

Bash

```
sudo sed -i 's/GRUB_CMDLINE_LINUX_DEFAULT=.*/GRUB_CMDLINE_LINUX_DEFAULT="quiet loglevel=3 systemd.show_status=false vt.global_cursor_default=0"/g' /etc/default/grub

echo 'GRUB_TIMEOUT_STYLE="hidden"' | sudo tee -a /etc/default/grub
echo 'GRUB_RECORDFAIL_TIMEOUT=0' | sudo tee -a /etc/default/grub

sudo update-grub
```

Đặt âm thanh thành 100%, sau đó khởi động lại:

Bash

```
amixer -q sset Master 100% unmute
sudo reboot
```

### Triển khai dịch vụ Wake Word

Để triển khai dịch vụ phát hiện từ đánh thức trên máy đa năng, bạn cần cài đặt môi trường Python, tải tệp dự án lên, định cấu hình micrô camera và tự động khởi động sau khi khởi động.

#### 1. Cài đặt Miniconda

```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda3
~/miniconda3/bin/conda init bash
source ~/.bashrc
rm Miniconda3-latest-Linux-x86_64.sh
```


Đảm bảo rằng bạn tự động vào môi trường conda khi đăng nhập

```bash
if ! grep -q '.bashrc' ~/.bash_profile; then
    cat << 'EOF' >> ~/.bash_profile

if [ -f ~/.bashrc ]; then
    . ~/.bashrc
fi
EOF
fi
```


#### 2. Tạo môi trường ảo Python

```bash
conda create -n test python=3.10 -y
conda activate test
```

Nếu xuất hiện lỗi "Điều khoản dịch vụ chưa được chấp nhận", hãy thực hiện:

```bash
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r
```

#### 3. Tải file dự án lên

Tải toàn bộ thư mục `main/digital-human/` trên máy phát triển lên thư mục `~/digital-human/` trên máy đa năng:

```bash
# 在开发机上执行（将 <一体机IP> 替换为实际 IP）
scp -r main/digital-human/ xz@<一体机IP>:~/digital-human/
```

#### 4. Cài đặt các phụ thuộc hệ thống

Dịch vụ Wake Word yêu cầu thư viện ghi âm và plug-in ALSA PulseAudio:

```bash
sudo apt install libportaudio2 portaudio19-dev libasound2-plugins -y
```

#### 5. Cài đặt các phụ thuộc Python

```bash
cd ~/digital-human/wakeword_runtime
pip install numpy
pip install -r requirements.txt
```

#### 6. Tải mô hình từ đánh thức

Tệp mô hình không được bao gồm trong dự án và cấu hình cần phải được tải xuống riêng. Để biết chi tiết, hãy xem chương "Tải xuống mô hình" trong [docs/digit-human-wakeword.md](digital-human-wakeword.md).

#### 7. Sửa đổi script tự khởi động Openbox

Bạn cần thêm cấu hình micrô PulseAudio và Camera để tự động khởi động và thay đổi địa chỉ Chrome thành trang thử nghiệm.

Đầu tiên hãy xác nhận tên thiết bị của Microphone Camera trong PulseAudio:

```bash
pulseaudio --start
pactl list sources short
```

Tìm dòng chứa `USB_Camera` và ghi chú tên đầy đủ, ví dụ:

```
alsa_input.usb-SN0002_2K_USB_Camera_46435000_P030D00_SN0002-02.mono-fallback
```

Sau đó ghi đè tự động khởi động bằng toàn bộ nội dung (thay thế `TARGET_MIC` bằng tên thiết bị thực của bạn):

``` bash
mèo << 'EOF' > ~/.config/openbox/autostart
# 1. Khởi động dịch vụ âm thanh và đợi một lát
xungaudio --bắt đầu
ngủ 1

#2. Khóa micro của Camera (vui lòng thay bằng tên thiết bị thật của bạn)
TARGET_MIC="alsa_input.usb-SN0002_2K_USB_Camera_46435000_P030D00_SN0002-02.mono-dự phòng"

#3. Đặt làm micro mặc định của hệ thống
Pactl set-default-source "$TARGET_MIC"

# 4. Bật tiếng
Pactl set-source-mute "$TARGET_MIC" 0

#5. Bật âm lượng lên 100%
Pactl set-source-volume "$TARGET_MIC" 100%

# --- Cấu hình môi trường trình duyệt và máy tính để bàn tối giản ---

# Tắt trình bảo vệ màn hình
xset-dpms
xset s noblank
xsetsoff

# Ẩn chuột
dọn dẹp -nhàn rỗi 0,1 -root &

# Khởi động trình duyệt theo vòng lặp vô hạn (nó có thể được khởi động lại sau vài giây ngay cả khi nó gặp sự cố hoặc bị tắt)
trong khi đúng; làm
    google-chrome\
        --kiosk\
        --không chạy lần đầu \
        --no-mặc định-kiểm tra trình duyệt \
        --disable-infobars \
        --disable-session-crashed-bubble \
        --disable-dịch \
        --disable-external-intent-requests \
        --autoplay-policy=no-user-gesture-required \
        --use-fake-ui-for-media-stream \
        "http://127.0.0.1:8006/index.html"
    ngủ 2
xong &
EOF
```

#### 8. Cấu hình dịch vụ Wake Word tự động khởi động khi khởi động

Tạo tệp dịch vụ systemd để cho phép dịch vụ Wake Word tự động chạy khi khởi động.

Đầu tiên hãy xác nhận UID của người dùng hiện tại:

```bash
id -u $(whoami)
```

Sau đó thay thế `1000` sau bằng UID tìm thấy (thường người dùng đầu tiên là 1000):

```bash
sudo tee /etc/systemd/system/digital-human.service << 'EOF'
[Unit]
Description=Digital Human Runtime
After=network.target sound.target

[Service]
Type=simple
User=xz
Environment=XDG_RUNTIME_DIR=/run/user/1000
Environment=PULSE_SERVER=unix:/run/user/1000/pulse/native
WorkingDirectory=/home/xz/digital-human
ExecStartPre=/bin/sleep 10
ExecStart=/home/xz/miniconda3/envs/test/bin/python start.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
```

> **Lưu ý quan trọng**:
> - `User=xz` — thay thế bằng tên người dùng thực tế của bạn
> - `/run/user/1000` — thay thế bằng UID thực tế của bạn
> - Đường dẫn trong `WorkingDirectory` và `ExecStart` — thay thế bằng đường dẫn triển khai thực tế của bạn
> - Biến môi trường PulseAudio trong `Environment` phải được giữ nguyên, nếu không dịch vụ Wake Word và trình duyệt không thể sử dụng Micrô máy ảnh cùng một lúc

Kích hoạt và bắt đầu dịch vụ:

```bash
sudo systemctl daemon-reload
sudo systemctl enable digital-human
sudo systemctl start digital-human
```

#### 9. Các lệnh quản lý dịch vụ thông dụng

```bash
sudo systemctl start digital-human     # 立即启动
sudo systemctl stop digital-human      # 停止
sudo systemctl restart digital-human   # 重启
sudo systemctl status digital-human    # 查看状态
journalctl -u digital-human -f         # 查看实时日志
```

