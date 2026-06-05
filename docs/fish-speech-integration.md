Đăng nhập vào AutoDL và thuê images
Chọn images:
```
PyTorch / 2.1.0 / 3.10(ubuntu22.04) / cuda 12.1
```

Sau khi bật máy, thiết lập tăng tốc học tập
```
source /etc/network_turbo
```

Nhập thư mục làm việc
```
cd autodl-tmp/
```

Kéo vật phẩm
```
git clone https://gitclone.com/github.com/fishaudio/fish-speech.git ; cd fish-speech
```

Cài đặt phụ thuộc
```
pip install -e.
```

Nếu báo lỗi thì cài đặt portaudio
```
apt-get install portaudio19-dev -y
```

Thực hiện sau khi cài đặt
```
pip install torch==2.3.1 torchvision==0.18.1 torchaudio==2.3.1 --index-url https://download.pytorch.org/whl/cu121
```

Tải xuống mô hình
```
cd tools
python download_models.py 
```

Sau khi tải model về, chạy giao diện
```
python -m tools.api_server --listen 0.0.0.0:6006 
```

Sau đó sử dụng trình duyệt để truy cập trang phiên bản aotodl
```
https://autodl.com/console/instance/list
```

Như được hiển thị bên dưới, hãy nhấp vào nút `自定义服务` trên máy của bạn ngay bây giờ để bật dịch vụ chuyển tiếp cổng.
![Dịch vụ tùy chỉnh](images/fishspeech/autodl-01.png)

Sau khi thiết lập dịch vụ chuyển tiếp cổng, hãy mở URL `http://localhost:6006/` trên máy tính cục bộ của bạn để truy cập giao diện tiếng cá.
![Xem trước dịch vụ](images/fishspeech/autodl-02.png)


Nếu bạn đang triển khai một mô-đun duy nhất, cấu hình cốt lõi như sau
```
selected_module:
  TTS: FishSpeech
TTS:
  FishSpeech:
    reference_audio: ["config/assets/wakeup_words.wav",]
    reference_text: ["哈啰啊，我是小智啦，声音好听的台湾女孩一枚，超开心认识你耶，最近在忙啥，别忘了给我来点有趣的料哦，我超爱听八卦的啦",]
    api_key: "123"
    api_url: "http://127.0.0.1:6006/v1/tts"
```

Sau đó khởi động lại dịch vụ