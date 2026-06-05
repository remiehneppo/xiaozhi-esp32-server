Tài liệu này là một tài liệu phát triển. Nếu bạn cần triển khai máy chủ Xiaozhi, [bấm vào đây để xem hướng dẫn triển khai](../../README.md#%E9%83%A8%E7%BD%B2%E6%96%87%E6%A1%A3)

Để xem quá trình triển khai con người kỹ thuật số tất cả trong một, khởi động toàn màn hình Kiosk và cấu hình môi trường hệ thống, [nhấp vào đây để xem hướng dẫn triển khai tất cả trong một](../../docs/all-in-one-digital-human-setup.md)

Để xem bản tải xuống mô hình Wake Word, cấu hình thời gian chạy và hướng dẫn sử dụng chi tiết, [bấm vào đây để xem tài liệu đặc biệt của Wake Word](../../docs/digital-human-wakeword.md)

#Giới thiệu dự án

digital-human là một mô-đun thử nghiệm con người kỹ thuật số độc lập, chịu trách nhiệm cung cấp các trang thử nghiệm cục bộ, tài nguyên tương tác giao diện người dùng, thời gian chạy từ đánh thức và khả năng cầu nối sự kiện để kết nối và điều chỉnh toàn bộ liên kết tương tác kỹ thuật số của con người.

# Bắt đầu nhanh

Cài đặt phụ thuộc:

```bash
pip install -r wakeword_runtime/requirements.txt
```

Bắt đầu mô-đun:

```bash
python start.py
```

#Địa chỉ truy cập

Sau khi khởi động, bạn có thể truy cập:

- Địa chỉ trang: http://127.0.0.1:8006/index.html
- Địa chỉ cầu nối sự kiện: ws://127.0.0.1:8006/wakeword-ws
- Kiểm tra sức khỏe: http://127.0.0.1:8006/health

# Mô tả thư mục

- `start.py`: mục khởi động mô-đun
- `index.html`: Lối vào trang thử nghiệm con người kỹ thuật số
- `wakeword_runtime`: thư mục cấu hình và thời gian chạy từ đánh thức cục bộ
- `js`, `css`: tập lệnh và kiểu giao diện người dùng trang
- `images`, `resources`: file tài nguyên trang

# Tài liệu liên quan

- Hướng dẫn triển khai máy tất cả trong một: phù hợp với triển khai toàn bộ máy thiết bị x86, hiển thị Kiosk và cấu hình tự động khởi động
	[../../docs/all-in-one-digit-human-setup.md](../../docs/all-in-one-digital-human-setup.md)
- Tài liệu đặc biệt Wake word: áp dụng cho việc tải xuống mô hình Wake Word, cấu hình thời gian chạy và hướng dẫn gỡ lỗi cục bộ
	[../../docs/digital-human-wakeword.md](../../docs/digital-human-wakeword.md)