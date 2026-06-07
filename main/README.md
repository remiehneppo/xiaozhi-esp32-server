# Tài liệu kỹ thuật cho `xiaozhi-esp32-server`

Tài liệu này là bản tổng quan ngắn gọn cho các thành phần chính của hệ thống. Phần hướng dẫn triển khai chi tiết vẫn nằm ở `README.md` và `docs/Deployment.md`.

## Tổng quan

`xiaozhi-esp32-server` là backend cho hệ sinh thái trợ lý giọng nói chạy trên ESP32. Hệ thống kết hợp các thành phần xử lý âm thanh, mô hình ngôn ngữ, TTS, quản trị cấu hình và các mô-đun giao tiếp thời gian thực.

## Các thành phần chính

### `xiaozhi-server`

Đây là dịch vụ lõi bằng Python. Nó xử lý:

- Kết nối WebSocket với thiết bị ESP32
- Thu âm, VAD, ASR, LLM và TTS
- Nạp cấu hình động từ `manager-api`
- Chạy hệ thống plugin và các tác vụ điều khiển

### `manager-api`

Dịch vụ backend quản trị bằng Java Spring Boot. Nó cung cấp:

- API cho `manager-web` và `manager-mobile`
- Quản lý người dùng, thiết bị, cấu hình và OTA
- Lưu trữ dữ liệu với MySQL và cache với Redis

### `manager-web`

Giao diện web để cấu hình hệ thống, quản lý thiết bị và theo dõi vận hành.

### `manager-mobile`

Ứng dụng quản trị di động dùng cho các tác vụ cấu hình và kiểm tra nhanh trên điện thoại.

### `digital-human`

Mô-đun kiểm thử cục bộ cho luồng âm thanh, wake word và tương tác trình duyệt.

## Luồng hoạt động

1. ESP32 kết nối vào `xiaozhi-server` qua WebSocket.
2. Âm thanh được xử lý qua VAD và ASR.
3. Văn bản được gửi đến LLM để suy luận.
4. Kết quả được chuyển sang TTS để phát lại.
5. Cấu hình hệ thống được lấy từ `manager-api` khi cần.

## Ghi chú triển khai

- Nếu muốn chạy nhanh theo cấu hình tối thiểu, ưu tiên `config.yaml` trong `main/xiaozhi-server`.
- Nếu muốn quản trị tập trung, dùng `manager-api` kèm `manager-web`.
- Các chi tiết cài đặt, mô hình local và Docker đã được mô tả ở tài liệu triển khai chính.
