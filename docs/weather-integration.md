# Hướng dẫn sử dụng plugin thời tiết

## Tổng quan

Plug-in thời tiết `get_weather` là một trong những chức năng cốt lõi của trợ lý giọng nói Xiaozhi ESP32, hỗ trợ truy vấn thông tin thời tiết trên toàn quốc thông qua giọng nói. Plug-in này dựa trên API thời tiết Zephyr và cung cấp các chức năng dự báo thời tiết theo thời gian thực và thời tiết trong 7 ngày.

## Hướng dẫn ứng dụng khóa API

### 1. Đăng ký tài khoản Zefeng Weather

1. Truy cập [Bảng điều khiển thời tiết Nhật Bản](https://console.qweather.com/)
2. Đăng ký tài khoản và hoàn tất xác minh email
3. Đăng nhập vào bảng điều khiển

### 2. Tạo ứng dụng lấy API Key

1. Sau khi vào bảng điều khiển, nhấp vào ["Quản lý dự án"](https://console.qweather.com/project?lang=zh) → "Tạo dự án" ở bên phải
2. Điền thông tin dự án:
   - **Tên dự án**: chẳng hạn như "Trợ lý giọng nói Xiao Zhi"
3. Nhấp vào Lưu
4. Sau khi dự án được tạo, hãy nhấp vào "Tạo thông tin xác thực" trong dự án
5. Điền thông tin xác thực:
    - **Tên thông tin xác thực**: Chẳng hạn như "Trợ lý giọng nói Xiao Zhi"
    - **Phương thức xác thực danh tính**: Chọn "API Key"
6. Nhấp vào Lưu
7. Sao chép `API Key` trong thông tin đăng nhập, đây là thông tin cấu hình key đầu tiên

### 3. Nhận máy chủ API

1. Nhấp vào ["Cài đặt"](https://console.qweather.com/setting?lang=zh) → "Máy chủ API" trong bảng điều khiển
2. Xem địa chỉ `API Host` độc quyền được chỉ định cho bạn. Đây là thông tin cấu hình quan trọng thứ hai.

Thao tác trên sẽ nhận được 2 thông tin cấu hình quan trọng: `API Key` và `API Host`

## Phương thức cấu hình (chọn một phương thức bất kỳ)

### Phương pháp 1. Nếu bạn sử dụng triển khai bảng điều khiển thông minh (được khuyến nghị)

1. Đăng nhập vào bảng điều khiển thông minh
2. Nhập trang "Cấu hình vai trò"
3. Chọn tác nhân để cấu hình
4. Nhấp vào nút "Chỉnh sửa tính năng"
5. Tìm plug-in "Weather Query" trong khu vực cấu hình tham số ở bên phải
6. Kiểm tra "Truy vấn thời tiết"
7. Điền cấu hình key đầu tiên đã sao chép `API Key` vào `天气插件 API 密钥`
8. Điền cấu hình khóa thứ hai đã sao chép `API Host` vào `开发者 API Host`
9. Lưu cấu hình, sau đó lưu cấu hình tác nhân

### Cách 2. Nếu bạn chỉ triển khai một module xiaozhi-server

Định cấu hình trong `data/.config.yaml`:

1. Điền cấu hình khóa đầu tiên đã sao chép `API Key` vào `api_key`
2. Điền cấu hình khóa thứ hai đã sao chép `API Host` vào `api_host`
3. Điền thành phố của bạn vào `default_location`, ví dụ `广州`

```yaml
plugins:
  get_weather:
    api_key: "你的和风天气API密钥"
    api_host: "你的和风天气API主机地址"
    default_location: "你的默认查询城市"
```

