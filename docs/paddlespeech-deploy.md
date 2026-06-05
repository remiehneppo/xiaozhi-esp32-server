# PaddleSpeechTTS tích hợp dịch vụ xiaozhi

## Những điểm chính
- Ưu điểm: triển khai offline cục bộ, nhanh chóng
- Nhược điểm: Kể từ ngày 25/09/2025, model mặc định là model Trung Quốc và không hỗ trợ tiếng Anh để nói. Nếu nó chứa tiếng Anh, sẽ không có âm thanh. Nếu cần hỗ trợ cả tiếng Trung và tiếng Anh thì bạn cần phải tự rèn luyện.

## 1. Yêu cầu cơ bản về môi trường
Hệ điều hành: Windows/Linux/WSL 2

Phiên bản Python: 3.9 trở lên (vui lòng điều chỉnh theo hướng dẫn chính thức của Paddle)

Phiên bản mái chèo: phiên bản mới nhất chính thức ```https://www.paddlepaddle.org.cn/install```

Công cụ quản lý phụ thuộc: conda hoặc venv

## 2. Bắt đầu dịch vụ chèo thuyền
### 1. Lấy mã nguồn từ kho padspeech chính thức
```bash 
git clone https://github.com/PaddlePaddle/PaddleSpeech.git
```
### 2. Tạo môi trường ảo
``` bash

conda tạo -n chèo_env python=3.10 -y
conda kích hoạt mái chèo_env
```
### 3.安装paddle
因CPU架构、GPU架构不同，请根据Paddle官方支持的python版本建立环境  
```
https://www.paddlepaddle.org.cn/install
```

### 4. Vào thư mục câu nói mái chèo
```bash
cd PaddleSpeech
```
### 5. Cài đặt mái chèo
``` bash
pip cài đặt pytest-runner -i https://pypi.tuna.tsinghua.edu.cn/simple

#Sử dụng bất kỳ lệnh nào sau đây
pip cài đặt mái chèo -i https://mirror.baidu.com/pypi/simple
pip cài đặt mái chèo -i https://pypi.tuna.tsinghua.edu.cn/simple
```
### 6.使用命令自动下载语音模型
```bash
mái chèo tts --input "Xin chào, đây là bài kiểm tra"
```
Bước này sẽ tự động tải bộ đệm mô hình xuống thư mục .paddlespeech/models cục bộ

### 7. Sửa đổi cấu hình tts_online_application.yaml
Danh mục tham khảo ```"PaddleSpeech\demos\streaming_tts_server\conf\tts_online_application.yaml"```
Chọn tệp ```tts_online_application.yaml``` để mở bằng trình chỉnh sửa và đặt ```protocol``` thành ```WebSocket```

### 8. Khởi động dịch vụ
```yaml
paddlespeech_server start --config_file ./demos/streaming_tts_server/conf/tts_online_application.yaml
#官方默认启动命令：
paddlespeech_server start --config_file ./conf/tts_online_application.yaml
```
Vui lòng bắt đầu lệnh theo thư mục thực tế của ```tts_online_application.yaml``` của bạn. Khi bạn nhìn thấy nhật ký sau, quá trình khởi động đã thành công.
```
Prefix dict has been built successfully.
[2025-08-07 10:03:11,312] [   DEBUG] __init__.py:166 - Prefix dict has been built successfully.
INFO:     Started server process [2298]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8092 (Press CTRL+C to quit)
```

## 3. Sửa file cấu hình của Xiaozhi
### 1.```main/xiaozhi-server/core/providers/tts/paddle_speech.py```

### 2.```main/xiaozhi-server/data/.config.yaml```
Triển khai bằng một mô-đun duy nhất
```yaml
selected_module:
  TTS: PaddleSpeechTTS
TTS:
  PaddleSpeechTTS:
      type: paddle_speech
      protocol: WebSocket
      url:  ws://127.0.0.1:8092/paddlespeech/tts/streaming  # TTS 服务的 URL 地址，指向本地服务器 [WebSocket默认ws://127.0.0.1:8092/paddlespeech/tts/streaming]
      spk_id: 0  # 发音人 ID，0 通常表示默认的发音人
      sample_rate: 24000  # 采样率 [WebSocket默认24000，http默认0 自动选择]
      speed: 1.0  # 语速，1.0 表示正常语速，>1 表示加快，<1 表示减慢
      volume: 1.0  # 音量，1.0 表示正常音量，>1 表示增大，<1 表示减小
      save_path:   # 保存路径
```
### 3. Bắt đầu dịch vụ xiaozhi
```py
python app.py
```
Sau khi khởi động `python start.py` trong `main/digital-human`, hãy mở `http://127.0.0.1:8006/index.html` và kiểm tra xem có nhật ký đầu ra ở cuối giọng nói mái chèo khi kết nối và gửi tin nhắn hay không.

Tham chiếu nhật ký đầu ra:
```
THÔNG TIN: 127.0.0.1:44312 - "WebSocket/paddlespeech/tts/streaming" [được chấp nhận]
THÔNG TIN: kết nối mở
[2025-08-07 11:16:33,355] [ INFO] - câu: Haha, sao tự nhiên lại chat với mình thế?
[2025-08-07 11:16:33,356] [ INFO] - Thời lượng của âm thanh là: 2,4625 s
[2025-08-07 11:16:33,356] [ THÔNG TIN] - thời gian phản hồi đầu tiên: 0,1143045425415039 s
[2025-08-07 11:16:33,356] [ THÔNG TIN] - thời gian phản hồi cuối cùng: 0,4777836799621582 s
[2025-08-07 11:16:33,356] [ THÔNG TIN] - RTF: 0.19402382942625715
[2025-08-07 11:16:33,356] [ INFO] - Thông tin khác: thời gian trước: 0,06514096260070801 s, thời gian suy luận sáng đầu tiên: 0,008037090301513672 s, thời gian suy luận giọng nói đầu tiên: 0,04112648963928223 s,
[2025-08-07 11:16:33,356] [ INFO] - Hoàn thành việc tổng hợp các luồng âm thanh
THÔNG TIN: kết nối đã đóng

```
