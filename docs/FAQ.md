# Câu hỏi thường gặp ❓

### 1. Tại sao Xiaozhi nhận ra nhiều tiếng Hàn, tiếng Nhật và tiếng Anh khi tôi nói? 🇰🇷

Gợi ý: Kiểm tra xem `models/SenseVoiceSmall` đã có `model.pt` chưa
Nếu chưa có file thì hãy tải về, xem tại đây [Tải file mô hình nhận dạng giọng nói](Deployment.md)

### 2. Tại sao lại xuất hiện thông báo "tệp lỗi tác vụ TTS không tồn tại"? 📁

Đề xuất: Kiểm tra xem `conda` có được sử dụng đúng cách để cài đặt thư viện `libopus` và `ffmpeg` hay không.

Nếu chưa cài thì cài đi

```
conda install conda-forge::libopus
conda install conda-forge::ffmpeg
```

### 3. TTS thường xuyên bị lỗi và time out ⏰

Đề xuất: Nếu `EdgeTTS` thường xuyên bị lỗi, trước tiên hãy kiểm tra xem proxy (thang) có được sử dụng hay không. Nếu được sử dụng, vui lòng thử đóng proxy và thử lại;
Nếu bạn đang sử dụng Beanbag TTS của Volcano engine thì nên sử dụng phiên bản trả phí khi nó thường xuyên bị lỗi, vì phiên bản thử nghiệm chỉ hỗ trợ 2 đồng thời.

### 4. Bạn có thể kết nối với máy chủ tự build bằng Wifi nhưng chế độ 4G không kết nối được 🔐

Lý do: Phần sụn của Xia Ge yêu cầu kết nối an toàn ở chế độ 4G.

Giải pháp: Hiện nay có 2 cách giải quyết. Chọn bất kỳ một:

1. Thay đổi mã. Tham khảo video này để giải quyết vấn đề https://www.bilibili.com/video/BV18MfTYoE85

2. Sử dụng nginx để định cấu hình chứng chỉ ssl. Hướng dẫn tham khảo https://icnt94i5ctj4.feishu.cn/docx/GnYOdMNJOoRCljx1ctecsj9cnRe

### 5. Làm cách nào để cải thiện tốc độ phản hồi hội thoại của Xiaozhi? ⚡

Cấu hình mặc định của dự án này là một giải pháp chi phí thấp. Người mới bắt đầu nên sử dụng mô hình miễn phí mặc định trước để giải quyết vấn đề "chạy nhanh" và sau đó tối ưu hóa "chạy nhanh".
Nếu bạn cần cải thiện tốc độ phản hồi, bạn có thể thử thay thế từng thành phần. Bắt đầu từ phiên bản `0.5.2`, dự án hỗ trợ cấu hình phát trực tuyến. So với các phiên bản trước, tốc độ phản hồi tăng lên khoảng `2.5 giây`, cải thiện đáng kể trải nghiệm người dùng.

| Tên mô-đun | Thiết lập cấp đầu vào miễn phí | Cấu hình phát trực tuyến |
|:---:|:---:|:---:|
| ASR (Nhận dạng giọng nói) | FunASR (Địa phương) | 👍XunfeiStreamASR (Truyền phát iFlytek) |
| LLM (Mô hình lớn) | glm-4-flash (Zhipu) | 👍qwen-flash (Alibaba Bailian) |
| VLLM (Mô hình trực quan lớn) | glm-4v-flash (Phổ trí tuệ) | 👍qwen3.5-flash (Alibaba Bailian) |
| TTS (tổng hợp giọng nói) | EdgeTTS (Microsoft) | 👍HuoshanDoubleStreamTTS (dòng núi lửa) |
| Ý định (nhận dạng ý định) | function_call (gọi hàm) | function_call (gọi hàm) |
| Bộ nhớ (chức năng bộ nhớ) | mem_local_short (bộ nhớ ngắn hạn cục bộ) | mem_local_short (bộ nhớ ngắn hạn cục bộ) |

Nếu bạn lo ngại về mức tiêu thụ thời gian của từng thành phần, vui lòng kiểm tra [báo cáo kiểm tra hiệu suất thành phần của Xiaozhi](https://github.com/xinnan-tech/xiaozhi-performance-research) và bạn thực sự có thể kiểm tra nó trong môi trường của mình theo các phương pháp kiểm tra trong báo cáo.

### 6. Tôi nói rất chậm và Xiaozhi luôn tóm lấy lời khi tôi tạm dừng 🗣️

Gợi ý: Tìm phần sau trong tệp cấu hình và tăng giá trị của `min_silence_duration_ms` (ví dụ: thay đổi thành `1000`):

```yaml
VAD:
  SileroVAD:
    threshold: 0.5
    model_dir: models/snakers4_silero-vad
    min_silence_duration_ms: 700  # Nếu người nói dừng lâu hơn, có thể tăng giá trị này
```

### 7. Hướng dẫn liên quan đến triển khai
1. [Cách thực hiện triển khai đơn giản nhất](./Deployment.md)<br/>
2. [Cách triển khai mô-đun đầy đủ](./Deployment_all.md)<br/>
3. [Cách triển khai cổng MQTT để kích hoạt giao thức MQTT+UDP](./mqtt-gateway-integration.md)<br/>
4. [Cách tự động lấy mã mới nhất của dự án này và tự động biên dịch và khởi động nó](./dev-ops-integration.md)<br/>
5. [Cách tích hợp với Nginx](https://github.com/xinnan-tech/xiaozhi-esp32-server/issues/791)<br/>

### 8. Hướng dẫn liên quan đến biên dịch firmware
1. [Cách tự biên dịch firmware Xiaozhi](./firmware-build.md)<br/>
2. [Cách sửa đổi địa chỉ OTA dựa trên chương trình cơ sở do  biên soạn](./firmware-setting.md)<br/>
3. [Cách định cấu hình nâng cấp OTA chương trình cơ sở tự động để triển khai một mô-đun](./OTA-upgrade-guide.md)<br/>

### 9. Mở rộng các hướng dẫn liên quan
1. [Cách bật bảng điều khiển thông minh đăng ký số điện thoại di động](./ali-sms-integration.md)<br/>
2. [Cách tích hợp HomeAssistant để điều khiển nhà thông minh](./homeassistant-integration.md)<br/>
3. [Cách bật mô hình trực quan để nhận dạng vật thể bằng cách chụp ảnh](./mcp-vision-integration.md)<br/>
4. [Cách triển khai điểm truy cập MCP](./mcp-endpoint-enable.md)<br/>
5. [Cách truy cập điểm truy cập MCP](./mcp-endpoint-integration.md)<br/>
6. [Cách lấy thông tin thiết bị bằng phương pháp MCP](./mcp-get-device-info.md)<br/>
7. [Cách bật nhận dạng giọng nói](./voiceprint-integration.md)<br/>
8. [Hướng dẫn cấu hình nguồn plug-in tin tức](./newsnow_plugin_config.md)<br/>
9. [Hướng dẫn tích hợp Ragflow cơ sở kiến thức](./ragflow-integration.md)<br/>
10. [Cách triển khai nguồn ngữ cảnh](./context-provider-integration.md)<br/>
11. [Cách tích hợp bộ nhớ thông minh PowerMem](./powermem-integration.md)<br/>
12. [Cách định cấu hình plug-in thời tiết để truy vấn thời tiết](./weather-integration.md)<br/>
13. [Cách bật plug-in gọi điện trên thiết bị](./device-call-guide.md)<br/>

### 10. Hướng dẫn liên quan đến dân số
1. [phương pháp khởi động kỹ thuật số-con người](./digital-human-wakeword.md)<br/>
2. [Cách triển khai con người kỹ thuật số trên máy chủ mini N100](./all-in-one-digital-human-setup.md)<br/>

### 11. Hướng dẫn liên quan đến nhân bản giọng nói và triển khai giọng nói cục bộ
1. [Cách sao chép âm thanh trên bảng điều khiển thông minh](./huoshan-streamTTS-voice-cloning.md)<br/>
2. [Cách triển khai chỉ mục tích hợp-tts giọng nói cục bộ](./index-stream-integration.md)<br/>
3. [Cách triển khai giọng nói địa phương tích hợp giọng nói cá](./fish-speech-integration.md)<br/>
4. [Cách triển khai và tích hợp giọng nói cục bộ PaddleSpeech](./paddlespeech-deploy.md)<br/>

### 12. Hướng dẫn kiểm tra hiệu năng
1. [Hướng dẫn kiểm tra tốc độ của từng thành phần](./performance_tester.md)<br/>
2. [Kết quả kiểm tra công khai định kỳ](https://github.com/xinnan-tech/xiaozhi-performance-research)<br/>

### 13. Mọi thắc mắc vui lòng liên hệ với chúng tôi để được phản hồi 💬

Bạn có thể gửi vấn đề của mình tại [issues](https://github.com/xinnan-tech/xiaozhi-esp32-server/issues).
