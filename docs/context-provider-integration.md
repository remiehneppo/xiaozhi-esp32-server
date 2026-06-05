#Hướng dẫn sử dụng nguồn ngữ cảnh

## Tổng quan

`上下文源` là thêm [nguồn dữ liệu] vào ngữ cảnh của các từ nhắc hệ thống Xiaozhi.

`上下文源` Ngay lúc Xiaozhi thức dậy, hãy lấy dữ liệu của hệ thống bên ngoài và tự động đưa dữ liệu đó vào từ nhắc hệ thống (System Nhắc) của mô hình lớn.
Hãy để nó nhận thức được trạng thái của một cái gì đó trên thế giới khi nó thức dậy.

Về cơ bản, nó khác với MCP và bộ nhớ: `上下文源` là dữ liệu buộc Xiaozhi nhận thức thế giới; `记忆(Mem)` cho phép anh ấy biết những gì anh ấy đã nói trước đó; `MCP(functionc all)` được sử dụng khi cần gọi một khả năng/kiến thức nhất định.

Thông qua chức năng này, thời điểm Xiaozhi thức dậy, anh ấy “nhận thức” được:
- Trạng thái cảm biến sức khỏe con người (nhiệt độ cơ thể, huyết áp, trạng thái oxy trong máu, v.v.)
- Dữ liệu thời gian thực của hệ thống kinh doanh (tải máy chủ, dữ liệu việc cần làm, thông tin chứng khoán, v.v.)
- Bất kỳ tin nhắn văn bản nào có sẵn thông qua API HTTP

**Lưu ý**: Chức năng này chỉ giúp Xiaozhi nhận biết được trạng thái của sự vật khi thức dậy. Nếu bạn muốn Xiaozhi có được trạng thái của mọi thứ trong thời gian thực sau khi thức dậy, bạn nên kết hợp chức năng này với lệnh gọi của công cụ MCP.

## Nguyên tắc làm việc

1. **Nguồn cấu hình**: Người dùng định cấu hình một hoặc nhiều địa chỉ API HTTP.
2. **Yêu cầu kích hoạt**: Khi hệ thống xây dựng Lời nhắc, nếu phát hiện thấy mẫu chứa phần giữ chỗ `{{ dynamic_context }}` thì tất cả các API đã định cấu hình sẽ được yêu cầu.
3. **Tự động chèn**: Hệ thống sẽ tự động định dạng dữ liệu được API trả về vào danh sách Markdown, thay thế phần giữ chỗ `{{ dynamic_context }}`.

## Đặc tả giao diện

Để Xiaozhi phân tích cú pháp dữ liệu chính xác, API của bạn cần đáp ứng các thông số kỹ thuật sau:

- **Phương thức yêu cầu**: `GET`
- **Tiêu đề yêu cầu**: Hệ thống sẽ tự động thêm trường `device-id` vào Tiêu đề yêu cầu.
- **Định dạng phản hồi**: Phải trả về định dạng JSON và chứa các trường `code` và `data`.

### Ví dụ về phản hồi

**Trường hợp 1: Trả về cặp khóa-giá trị**
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "客厅温度": "26℃",
    "客厅湿度": "45%",
    "大门状态": "已关闭"
  }
}
```
*Tác dụng tiêm:*
```markdown
<context>
- **客厅温度：** 26℃
- **客厅湿度：** 45%
- **大门状态：** 已关闭
</context>
```

**Trường hợp 2: Quay lại danh sách**
```json
{
  "code": 0,
  "data": [
    "您有10个待办事项",
    "当前汽车的行驶速度是100km每小时"
  ]
}
```
*Tác dụng tiêm:*
```markdown
<context>
- 您有10个待办事项
- 当前汽车的行驶速度是100km每小时
</context>
```

## Hướng dẫn cấu hình

### Cách 1: Cấu hình console thông minh (triển khai toàn bộ module)

1. Đăng nhập vào bảng điều khiển thông minh và vào trang **Cấu hình vai trò**.
2. Tìm mục cấu hình **Nguồn ngữ cảnh** (nhấp vào nút "Chỉnh sửa nguồn").
3. Nhấp vào **Thêm** và nhập địa chỉ API của bạn.
4. Nếu API yêu cầu xác thực, bạn có thể thêm `Authorization` hoặc các Tiêu đề khác vào phần **tiêu đề yêu cầu**.
5. Lưu cấu hình.

### Cách 2: Cấu hình file cấu hình (triển khai từng module)

Chỉnh sửa tệp `xiaozhi-server/data/.config.yaml` và thêm phần cấu hình `context_providers`:

```yaml
# 上下文源配置
context_providers:
  - url: "http://api.example.com/data"
    headers:
      Authorization: "Bearer your-token"
  - url: "http://another-api.com/data"
```

## Kích hoạt chức năng

Theo mặc định, phần giữ chỗ `{{ dynamic_context }}` đã được đặt sẵn trong tệp mẫu từ nhắc nhở của hệ thống (`data/.agent-base-prompt.txt`) và bạn không cần thêm nó theo cách thủ công.

**Ví dụ:**

```markdown
<context>
【重要！以下信息已实时提供，无需调用工具查询，请直接使用：】
- **设备ID：** {{device_id}}
- **当前时间：** {{current_time}}
...
{{ dynamic_context }}
</context>
```

**Lưu ý**: Nếu không cần sử dụng tính năng này, bạn có thể chọn không định cấu hình bất kỳ nguồn ngữ cảnh nào hoặc bạn có thể xóa trình giữ chỗ `{{ dynamic_context }}` khỏi tệp mẫu từ lời nhắc.

## Phụ lục: Ví dụ về dịch vụ thử nghiệm mô phỏng

Để tạo điều kiện thuận lợi cho việc thử nghiệm và phát triển của bạn, chúng tôi cung cấp tập lệnh Python Mock Server đơn giản. Bạn có thể chạy tập lệnh này để mô phỏng giao diện API cục bộ.

**mock_api_server.py**

```python
import http.server
import socketserver
import json
from urllib.parse import urlparse, parse_qs

# Đặt số cổng
CỔNG = 8081

lớp MockRequestHandler(http.server.SimpleHTTPRequestHandler):
    chắc chắn do_GET(tự):
        # Phân tích đường dẫn và tham số
        Pared_path = urlparse(self.path)
        đường dẫn = Pared_path.path
        truy vấn = pars_qs(parsed_path.query)

        response_data = {}
        status_code = 200

print(f"Đã nhận được yêu cầu: {path}, tham số: {query}")

# Trường hợp 1: Mô phỏng dữ liệu sức khỏe (trả về từ điển Dict)
        # Kiểu tham số đường dẫn: /health
        # device_id được lấy từ Tiêu đề
        nếu đường dẫn == "/sức khỏe":
            device_id = self.headers.get("device-id", "unknown_device")
            print(f"device_id: {device_id}")
            phản hồi_data = {
                "mã": 0,
                "tin nhắn": "thành công",
                "dữ liệu": {
                    "ID thiết bị thử nghiệm": device_id,
                    "Nhịp tim": "80 nhịp/phút",
                    "huyết áp": "120/80 mmHg",
                    "Trạng thái": "Tốt"
                }
            }

# Trường hợp 2: Mô phỏng danh sách tin tức (return list List)
        # Không có tham số: /news/list
        đường dẫn elif == "/news/list":
            phản hồi_data = {
                "mã": 0,
                "tin nhắn": "thành công",
                "dữ liệu": [
                    "Tiêu đề hôm nay: Python 3.14 đã được phát hành",
                    "Tin tức công nghệ: Trợ lý AI thay đổi cuộc sống",
                    "Tin tức địa phương: Ngày mai trời sẽ mưa to, nhớ mang theo ô"
                ]
            }

# Trường hợp 3: Mô phỏng thông tin thời tiết (trả về chuỗi String)
        # Không có tham số: /weather/simple
        đường dẫn Elif == "/thời tiết/đơn giản":
            phản hồi_data = {
                "mã": 0,
                "tin nhắn": "thành công",
                "data": "Hôm nay trời nắng đến có mây, nhiệt độ 20-25 độ. Chất lượng không khí rất tốt và thích hợp cho việc đi du lịch."
            }

# Trường hợp 4: Mô phỏng chi tiết thiết bị (kiểu tham số truy vấn)
        # Kiểu tham số: /device/info
        # device_id được lấy từ Tiêu đề
        đường dẫn elif == "/thiết bị/thông tin":
            device_id = self.headers.get("device-id", "unknown_device")
            phản hồi_data = {
                "mã": 0,
                "tin nhắn": "thành công",
                "dữ liệu": {
                    "Phương thức truy vấn": "Tham số tiêu đề",
                    "ID thiết bị": device_id,
                    "Pin": "85%",
                    "chương trình cơ sở": "v2.0.1"
                }
            }
        
        # Trường hợp 5: 404 Not Found
        khác:
            mã trạng thái = 404
            reply_data = {"error": "Giao diện không tồn tại"}

# Gửi phản hồi
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(response_data, Ensure_ascii=False).encode('utf-8'))

# Bắt đầu dịch vụ
# Cho phép sử dụng lại địa chỉ để tránh lỗi khởi động lại nhanh
socketserver.TCPServer.allow_reuse_address = Đúng
với socketserver.TCPServer(("", PORT), MockRequestHandler) là httpd:
    print(f"=========================================================")
    print(f"Máy chủ API giả đã khởi động: http://localhost:{PORT}")
    print(f"Danh sách giao diện có sẵn:")
    print(f"1. [Từ điển] http://localhost:{PORT}/health")
    print(f"2. [Danh sách] http://localhost:{PORT}/news/list")
    print(f"3. [text] http://localhost:{PORT}/weather/simple")
    print(f"4. [tham số] http://localhost:{PORT}/device/info")
    print(f"=========================================================")
    thử:
        httpd.serve_forever()
    ngoại trừ Bàn phímInterrupt:
        print("\nDịch vụ đã dừng")
```