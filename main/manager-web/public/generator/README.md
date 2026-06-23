# Tùy chỉnh chủ đề hộp thoại

## Tổng quan dự án

Thư mục này chứa các tệp tĩnh được đóng gói từ dự án [xiaozhi-assets-generator](https://github.com/xinnan-tech/xiaozhi-assets-generator), được sử dụng để tùy chỉnh trực tuyến và tạo chủ đề hộp thoại. Người dùng có thể định cấu hình các thành phần như từ đánh thức, phông chữ, biểu tượng cảm xúc và hình nền trò chuyện thông qua công cụ này và xuất chúng sang tệp `assets.bin`.

## Cấu trúc thư mục

```
generator/
├── assets/              # Xây dựng các tệp tài nguyên được tạo
│   ├── ft_render-ByO_jG18.js
│   ├── index-CYcyz9xb.js
│   └── index-NXxBVrod.css
├── static/              # Thư mục tài nguyên tĩnh
│   ├── charsets/        # tập tin bộ ký tự
│   │   ├── deepseek.txt
│   │   ├── gb2312.txt
│   │   ├── latin1.txt
│   │   └── qwen18409.txt
│   ├── fonts/           # Tài nguyên font chữ
│   │   ├── font_noto_qwen_14_1.bin
│   │   ├── font_noto_qwen_16_4.bin
│   │   ├── font_noto_qwen_20_4.bin
│   │   ├── font_noto_qwen_30_4.bin
│   │   ├── font_puhui_deepseek_14_1.bin
│   │   ├── font_puhui_deepseek_16_4.bin
│   │   ├── font_puhui_deepseek_20_4.bin
│   │   ├── font_puhui_deepseek_30_4.bin
│   │   ├── noto_qwen.ttf
│   │   └── puhui_deepseek.ttf
│   ├── multinet_model/  # Mô hình từ kích hoạt (wake word) tùy chỉnh
│   │   ├── fst/
│   │   ├── mn6_cn/
│   │   ├── mn6_en/
│   │   ├── mn7_cn/
│   │   └── mn7_en/
│   ├── twemoji32/       # 32x32 Hình ảnh biểu hiện
│   ├── twemoji64/       # 64x64 Hình ảnh biểu hiện
│   ├── wakenet_model/   # Mô hình từ kích hoạt (wake word) mặc định
│   └── README.md        # Mô tả tài nguyên tĩnh
├── index.html           # Trang chính
└── README.md            # Tài liệu mô tả dự án
```

##Chức năng chính

### 1. Cấu hình chip và màn hình
- Hỗ trợ nhiều model chip: ESP32-S3, ESP32-C3, ESP32-P4, ESP32-C6
- Cài đặt độ phân giải màn hình linh hoạt
-Hỗ trợ định dạng màu RGB565

### 2. Đánh thức cấu hình word
- **Từ Wake mặc định**: Dựa trên các mô hình WakeNet được hỗ trợ bởi các chip khác nhau
- **Từ đánh thức tùy chỉnh**: Hỗ trợ các từ lệnh tiếng Trung và tiếng Anh, ngưỡng có thể định cấu hình và thời gian chờ

### 3. Cấu hình phông chữ
- Nhiều phông chữ cài sẵn: Alibaba Puhui, Noto Qwen, v.v.
- Hỗ trợ tải lên các tệp phông chữ TTF/WOFF tùy chỉnh
- Kích thước phông chữ có thể cấu hình và độ sâu màu (bpp)

### 4. Tập hợp biểu thức
- Cung cấp 21 sơ đồ cài sẵn cho các biểu thức cơ bản (hai kích thước: 32x32 và 64x64)
- Hỗ trợ tải lên các biểu thức tùy chỉnh

### 5. Nền trò chuyện
-Hỗ trợ chuyển đổi chế độ sáng/tối
- Nền màu hoặc nền images có thể định cấu hình
- Tự động thích ứng với độ phân giải màn hình

## Cách sử dụng

1. Khởi động tệp `index.html` dưới dạng dịch vụ
2. Chọn model chip và cấu hình màn hình
3. Định cấu hình các thành phần chủ đề thông qua các tab khác nhau
4. Nhấp vào nút Tạo để xem danh sách tài nguyên
5. Sau khi xác nhận, hãy tạo và tải xuống tệp `assets.bin`

## Mô tả kỹ thuật

- Các tài nguyên tĩnh được xây dựng nằm trong thư mục `assets/`
- Các tệp tài nguyên và mô hình gốc được đặt trong thư mục `static/`
- Hỗ trợ sử dụng ngoại tuyến, không cần phụ thuộc thêm

## Ghi chú

- Công cụ này được thiết kế để sử dụng ngoại tuyến và tất cả tài nguyên đều có trong thư mục
- Tệp `assets.bin` được tạo cần được sử dụng với phần cứng hộp thoại
- Tài nguyên tùy chỉnh cần chú ý đến các hạn chế về định dạng và kích thước tệp để đảm bảo khả năng tương thích