#Hướng dẫn sử dụng mô hình trực quan
Hướng dẫn này được chia thành hai phần:
- Phần 1: Chạy xiaozhi-server trên một mô-đun duy nhất để mở mô hình trực quan
- Phần 2: Cách mở mô hình trực quan khi toàn bộ module đang chạy

Trước khi mở mô hình trực quan, bạn cần chuẩn bị 3 thứ:
- Bạn cần chuẩn bị một thiết bị có camera, thiết bị này đã có sẵn trong kho của Anh Xiabao và có chức năng gọi camera. Ví dụ `立创·实战派ESP32-S3开发板`
- Nâng cấp phiên bản phần mềm thiết bị của bạn lên 1.6.6 trở lên
- Bạn đã vượt qua thành công mô-đun hội thoại cơ bản

## Mô-đun đơn chạy máy chủ xiaozhi để mở mô hình trực quan

### Bước đầu tiên là xác nhận mạng
Bởi vì mô hình trực quan sẽ bắt đầu cổng 8003 theo mặc định.

Nếu bạn đang chạy docker, vui lòng xác nhận xem `docker-compose.yml` của bạn có cổng `8003` hay không. Nếu không, hãy cập nhật tệp `docker-compose.yml` mới nhất.

Nếu bạn đang chạy từ mã nguồn, hãy xác nhận xem tường lửa có cho phép cổng `8003` không

### Bước thứ hai là chọn mô hình trực quan của bạn
Mở tệp `data/.config.yaml` của bạn và đặt cài đặt `selected_module.VLLM` của bạn thành một mô hình trực quan nhất định. Hiện tại chúng tôi đã hỗ trợ mô hình trực quan của giao diện loại `openai`. `ChatGLMVLLM` là một trong những model tương thích với `openai`.

```
selected_module:
  VAD: ..
  ASR: ..
  LLM: ..
  VLLM: ChatGLMVLLM
  TTS: ..
  Memory: ..
  Intent: ..
```

Giả sử chúng ta sử dụng `ChatGLMVLLM` làm mô hình trực quan, thì chúng ta cần đăng nhập vào trang web [Zhipu AI](https://bigmodel.cn/usercenter/proj-mgmt/apikeys) và đăng ký khóa. Nếu bạn đã đăng ký khóa trước đó, bạn có thể sử dụng lại nó.

Trong tệp cấu hình của bạn, thêm cấu hình này. Nếu bạn đã có cấu hình này, hãy đặt api_key.

```
VLLM:
  ChatGLMVLLM:
    api_key: 你的api_key
```

### Bước thứ ba là khởi động dịch vụ máy chủ xiaozhi
Nếu bạn là mã nguồn thì nhập lệnh để bắt đầu
```
python app.py
```
Nếu bạn đang chạy docker, hãy khởi động lại vùng chứa
```
docker restart xiaozhi-esp32-server
```

Sau khi khởi động, nội dung nhật ký sau sẽ được xuất ra.

```
2025-06-01 **** - OTA接口是           http://192.168.4.7:8003/xiaozhi/OTA/
2025-06-01 **** - 视觉分析接口是        http://192.168.4.7:8003/mcp/vision/explain
2025-06-01 **** - WebSocket地址是       ws://192.168.4.7:8000/xiaozhi/v1/
2025-06-01 **** - =======上面的地址是WebSocket协议地址，请勿用浏览器访问=======
2025-06-01 **** - 如想测试WebSocket请启动digital-human模块，打开浏览器交互测试
2025-06-01 **** - =============================================================
```

Sau khi khởi động, hãy sử dụng trình duyệt để mở kết nối `视觉分析接口` trong nhật ký. Xem đầu ra là gì? Nếu bạn đang dùng Linux và không có trình duyệt, bạn có thể thực thi lệnh này:
```
curl -i 你的视觉分析接口
```

Bình thường nó sẽ hiển thị như thế này
```
MCP Vision 接口运行正常，视觉解释接口地址是：http://xxxx:8003/mcp/vision/explain
```

Xin lưu ý rằng nếu bạn triển khai trên mạng công cộng hoặc docker, bạn phải thay đổi cấu hình này trong `data/.config.yaml` của mình
```
server:
  vision_explain: http://你的ip或者域名:端口号/mcp/vision/explain
```

Tại sao? Vì giao diện giải thích trực quan cần được gửi đến thiết bị nên nếu địa chỉ của bạn là địa chỉ LAN hoặc địa chỉ nội bộ docker thì thiết bị không thể truy cập được.

Giả sử địa chỉ mạng công cộng của bạn là `111.111.111.111` thì `vision_explain` sẽ được định cấu hình như thế này

```
server:
  vision_explain: http://111.111.111.111:8003/mcp/vision/explain
```

Nếu giao diện MCP Vision của bạn đang chạy bình thường và bạn cũng cố gắng sử dụng trình duyệt để truy cập `视觉解释接口地址` đã phân phối một cách bình thường, vui lòng chuyển sang bước tiếp theo.

### Bước 4: Kích hoạt tính năng đánh thức thiết bị

Nói với thiết bị "Vui lòng bật camera và cho tôi biết bạn nhìn thấy gì"

Hãy chú ý đến đầu ra nhật ký của xiaozhi-server để xem có lỗi gì không.


## Cách mở mô hình trực quan khi toàn bộ mô-đun đang chạy

### Bước đầu tiên là xác nhận mạng
Bởi vì mô hình trực quan sẽ bắt đầu cổng 8003 theo mặc định.

Nếu bạn đang chạy docker, vui lòng xác nhận xem `docker-compose_all.yml` của bạn có được ánh xạ tới cổng `8003` hay không. Nếu không, hãy cập nhật tệp `docker-compose_all.yml` mới nhất.

Nếu bạn đang chạy từ mã nguồn, hãy xác nhận xem tường lửa có cho phép cổng `8003` không

### Bước 2 Xác nhận file cấu hình của bạn

Mở tệp `data/.config.yaml` của bạn và xác nhận xem cấu trúc tệp cấu hình của bạn có giống với `data/config_from_api.yaml` hay không. Nếu khác hoặc thiếu gì thì điền vào nhé.

### Bước 3 Định cấu hình khóa mô hình trực quan

Sau đó, trước tiên chúng ta cần đăng nhập vào trang web [Zhipu AI](https://bigmodel.cn/usercenter/proj-mgmt/apikeys) và đăng ký khóa. Nếu bạn đã đăng ký khóa trước đó, bạn có thể sử dụng lại nó.

Đăng nhập vào `智控台`, nhấp vào `模型配置` ở menu trên cùng, nhấp vào `视觉打语言模型` ở cột bên trái, tìm `VLLM_ChatGLMVLLM`, nhấp vào nút sửa đổi, nhập khóa của bạn vào `API密钥` trong hộp bật lên và nhấp vào lưu.

Sau khi lưu thành công, hãy đến tác nhân bạn cần kiểm tra, nhấp vào `配置角色` và trong nội dung mở ra, hãy kiểm tra xem `视觉大语言模型(VLLM)` đã chọn mô hình trực quan vừa rồi hay chưa. Nhấp vào Lưu.

### Bước 3: Khởi động module xiaozhi-server
Nếu bạn là mã nguồn thì nhập lệnh để bắt đầu
```
python app.py
```
Nếu bạn đang chạy docker, hãy khởi động lại vùng chứa
```
docker restart xiaozhi-esp32-server
```

Sau khi khởi động, nội dung nhật ký sau sẽ được xuất ra.

```
2025-06-01 **** - 视觉分析接口是        http://192.168.4.7:8003/mcp/vision/explain
2025-06-01 **** - WebSocket地址是       ws://192.168.4.7:8000/xiaozhi/v1/
2025-06-01 **** - =======上面的地址是WebSocket协议地址，请勿用浏览器访问=======
2025-06-01 **** - 如想测试WebSocket请启动digital-human模块，打开浏览器交互测试
2025-06-01 **** - =============================================================
```

Sau khi khởi động, hãy sử dụng trình duyệt để mở kết nối `视觉分析接口` trong nhật ký. Xem đầu ra là gì? Nếu bạn đang dùng Linux và không có trình duyệt, bạn có thể thực thi lệnh này:
```
curl -i 你的视觉分析接口
```

Bình thường nó sẽ hiển thị như thế này
```
MCP Vision 接口运行正常，视觉解释接口地址是：http://xxxx:8003/mcp/vision/explain
```

Xin lưu ý rằng nếu bạn triển khai trên mạng công cộng hoặc docker, bạn phải thay đổi cấu hình này trong `data/.config.yaml` của mình
```
server:
  vision_explain: http://你的ip或者域名:端口号/mcp/vision/explain
```

Tại sao? Vì giao diện giải thích trực quan cần được gửi đến thiết bị nên nếu địa chỉ của bạn là địa chỉ LAN hoặc địa chỉ nội bộ docker thì thiết bị không thể truy cập được.

Giả sử địa chỉ mạng công cộng của bạn là `111.111.111.111` thì `vision_explain` sẽ được định cấu hình như thế này

```
server:
  vision_explain: http://111.111.111.111:8003/mcp/vision/explain
```

Nếu giao diện MCP Vision của bạn đang chạy bình thường và bạn cũng cố gắng sử dụng trình duyệt để truy cập `视觉解释接口地址` đã phân phối một cách bình thường, vui lòng chuyển sang bước tiếp theo.

### Bước 4: Kích hoạt tính năng đánh thức thiết bị

Nói với thiết bị "Vui lòng bật camera và cho tôi biết bạn nhìn thấy gì"

Hãy chú ý đến đầu ra nhật ký của xiaozhi-server để xem có lỗi gì không.