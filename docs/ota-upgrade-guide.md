# Hướng dẫn cấu hình nâng cấp tự động OTA chương trình cơ sở triển khai mô-đun đơn

Hướng dẫn này sẽ hướng dẫn bạn cách định cấu hình chức năng nâng cấp tự động OTA chương trình cơ sở trong kịch bản **triển khai mô-đun đơn** để đạt được cập nhật tự động chương trình cơ sở của thiết bị.

Nếu bạn đang sử dụng **Triển khai mô-đun đầy đủ**, vui lòng bỏ qua hướng dẫn này.

## Giới thiệu chức năng

Khi triển khai một mô-đun, máy chủ xiaozhi có chức năng quản lý chương trình cơ sở OTA tích hợp, có thể tự động phát hiện phiên bản thiết bị và phát hành chương trình cơ sở được nâng cấp. Hệ thống sẽ tự động khớp và đẩy phiên bản phần sụn mới nhất dựa trên kiểu máy và phiên bản hiện tại.

## Điều kiện tiên quyết

- Bạn đã thực hiện thành công **triển khai mô-đun đơn** và chạy xiaozhi-server
- Thiết bị có thể kết nối với máy chủ bình thường

## Bước 1: Chuẩn bị file firmware

### 1. Tạo thư mục lưu trữ firmware

Các tập tin chương trình cơ sở cần phải được đặt trong thư mục `data/bin/`. Nếu thư mục không tồn tại, hãy tạo nó theo cách thủ công:

```bash
mkdir -p data/bin
```

### 2. Quy tắc đặt tên file firmware

Các tệp chương trình cơ sở phải tuân theo định dạng đặt tên sau:

```
{设备型号}_{版本号}.bin
```

**Mô tả quy tắc đặt tên:**
- `设备型号`: tên model của thiết bị, chẳng hạn như `lichuang-dev`, `bread-compact-wifi`, v.v.
- `版本号`: Số phiên bản firmware, phải bắt đầu bằng số, hỗ trợ số, chữ cái, dấu chấm, dấu gạch dưới và dấu gạch ngang, chẳng hạn như `1.6.6`, `2.0.0`, v.v.
- Đuôi file phải là `.bin`

**Ví dụ đặt tên:**
```
bread-compact-wifi_1.6.6.bin
lichuang-dev_2.0.0.bin
```

### 3. Đặt file firmware

Sao chép tệp chương trình cơ sở đã chuẩn bị (tệp .bin) vào thư mục `data/bin/`:

Điều quan trọng cần nói ba lần: tệp bin được nâng cấp là `xiaozhi.bin`, không phải tệp chương trình cơ sở đầy đủ `merged-binary.bin`!

Điều quan trọng cần nói ba lần: tệp bin được nâng cấp là `xiaozhi.bin`, không phải tệp chương trình cơ sở đầy đủ `merged-binary.bin`!

Điều quan trọng cần nói ba lần: tệp bin được nâng cấp là `xiaozhi.bin`, không phải tệp chương trình cơ sở đầy đủ `merged-binary.bin`!

```bash
cp xiaozhi.bin data/bin/设备型号_版本号.bin
```

Ví dụ:
```bash
cp xiaozhi.bin data/bin/bread-compact-wifi_1.6.6.bin
```

## Bước 2 Cấu hình địa chỉ truy cập mạng công cộng (chỉ bắt buộc khi triển khai mạng công cộng)

**Lưu ý: Bước này chỉ áp dụng cho các tình huống triển khai mạng công cộng một mô-đun. **

Nếu máy chủ xiaozhi của bạn được triển khai trên mạng công cộng (sử dụng IP công cộng hoặc tên miền), bạn phải định cấu hình tham số `server.vision_explain`, vì địa chỉ tải xuống chương trình cơ sở OTA sẽ sử dụng tên miền và cổng được định cấu hình.

Nếu bạn đang triển khai trên mạng LAN, bạn có thể bỏ qua bước này.

### Tại sao phải cấu hình tham số này?

Khi triển khai một mô-đun, khi hệ thống tạo địa chỉ tải xuống chương trình cơ sở, hệ thống sẽ sử dụng tên miền và cổng được định cấu hình trong `vision_explain` làm địa chỉ cơ sở. Nếu không cấu hình hoặc cấu hình sai, thiết bị sẽ không thể truy cập vào địa chỉ tải firmware.

### Phương thức cấu hình

Mở tệp `data/.config.yaml`, tìm phần cấu hình `server` và đặt tham số `vision_explain`:

```yaml
server:
  vision_explain: http://你的域名或IP:端口号/mcp/vision/explain
```

**Ví dụ về cấu hình:**

Triển khai mạng LAN (mặc định):
```yaml
server:
  vision_explain: http://192.168.1.100:8003/mcp/vision/explain
```

Triển khai tên miền công cộng:
```yaml
server:
  vision_explain: http://yourdomain.com:8003/mcp/vision/explain
```

### Ghi chú

- Tên miền hoặc IP phải là địa chỉ mà thiết bị có thể truy cập
- Nếu bạn sử dụng triển khai Docker, bạn không thể sử dụng địa chỉ nội bộ Docker (chẳng hạn như 127.0.0.1 hoặc localhost)
- Nếu bạn sử dụng proxy ngược nginx, vui lòng điền địa chỉ bên ngoài và số cổng, không phải số cổng nơi dự án này chạy.


## Câu hỏi thường gặp

### 1. Máy không nhận được bản cập nhật firmware

**Nguyên nhân và giải pháp có thể:**

- Kiểm tra việc đặt tên file firmware có đúng quy định không: `{型号}_{版本号}.bin`
- Kiểm tra xem tệp chương trình cơ sở có được đặt chính xác trong thư mục `data/bin/` không
- Kiểm tra xem model thiết bị có khớp với model trong tên file firmware không
- Kiểm tra xem số phiên bản firmware có cao hơn phiên bản hiện tại của thiết bị không
- Kiểm tra nhật ký máy chủ để xác nhận xem yêu cầu OTA có được xử lý bình thường không

### 2. Máy báo không truy cập được địa chỉ download

**Nguyên nhân và giải pháp có thể:**

- Kiểm tra tên miền hoặc IP được cấu hình trong `server.vision_explain` có đúng không
- Xác nhận số cổng đã được cấu hình đúng (mặc định 8003)
- Nếu nó được triển khai trên mạng công cộng, hãy đảm bảo rằng thiết bị có thể truy cập địa chỉ mạng công cộng.
- Nếu triển khai qua Docker, hãy đảm bảo bạn không sử dụng địa chỉ nội bộ (127.0.0.1)
- Kiểm tra xem tường lửa đã mở cổng tương ứng chưa
- Nếu bạn sử dụng proxy ngược nginx, vui lòng điền địa chỉ bên ngoài và số cổng, không phải số cổng nơi dự án này chạy.

### 3. Cách xác nhận phiên bản hiện tại của thiết bị

Kiểm tra nhật ký yêu cầu OTA. Số phiên bản được thiết bị báo cáo sẽ được hiển thị trong nhật ký:

```
[OTA_handler] - 设备 AA:BB:CC:DD:EE:FF 固件已是最新: 1.6.6
```

### 4. File firmware không có hiệu lực sau khi được đặt.

Hệ thống có thời gian lưu vào bộ đệm là 30 giây (mặc định) và có thể:
- Đợi 30 giây trước khi cho phép thiết bị thực hiện yêu cầu OTA
- Khởi động lại dịch vụ máy chủ xiaozhi
- Điều chỉnh cấu hình `firmware_cache_ttl` với thời gian ngắn hơn