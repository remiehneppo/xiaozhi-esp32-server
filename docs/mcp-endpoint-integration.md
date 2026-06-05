Hướng dẫn sử dụng điểm truy cập #MCP

Hướng dẫn này sử dụng chức năng máy tính mcp mã nguồn mở của Xiago làm ví dụ để giới thiệu cách kết nối dịch vụ mcp tùy chỉnh của riêng bạn với điểm truy cập của riêng bạn.

Tiền đề của hướng dẫn này là `xiaozhi-server` của bạn đã kích hoạt chức năng điểm truy cập mcp. Nếu bạn chưa kích hoạt nó, bạn có thể kích hoạt nó trước theo [hướng dẫn này](./mcp-endpoint-enable.md).

# Cách kết nối hàm mcp đơn giản với tác nhân, chẳng hạn như hàm máy tính

### Nếu bạn triển khai một mô-đun đầy đủ
Nếu triển khai một mô-đun đầy đủ, bạn có thể vào bảng điều khiển thông minh, quản lý tác nhân, nhấp vào `配置角色` và có nút `编辑功能` ở bên phải `意图识别`.

Bấm vào nút này. Trong trang bật lên, ở phía dưới cùng, sẽ có `MCP接入点`. Thông thường, `MCP接入点地址` của tác nhân này sẽ được hiển thị. Tiếp theo, chúng tôi sẽ mở rộng chức năng của máy tính dựa trên công nghệ MCP cho tác nhân này.

`MCP接入点地址` này rất quan trọng, bạn sẽ sử dụng nó sau.

### Nếu bạn đang triển khai một mô-đun duy nhất
Nếu bạn đang triển khai một mô-đun duy nhất và đã định cấu hình địa chỉ điểm truy cập MCP trong tệp cấu hình thì thông thường, khi bắt đầu triển khai mô-đun đơn lẻ, nhật ký sau sẽ được xuất ra.
```
250705[__main__]-INFO-初始化组件: vad成功 SileroVAD
250705[__main__]-INFO-初始化组件: asr成功 FunASRServer
250705[__main__]-INFO-OTA接口是          http://192.168.1.25:8002/xiaozhi/OTA/
250705[__main__]-INFO-视觉分析接口是     http://192.168.1.25:8002/mcp/vision/explain
250705[__main__]-INFO-mcp接入点是        ws://192.168.1.25:8004/mcp_endpoint/mcp/?token=abc
250705[__main__]-INFO-WebSocket地址是    ws://192.168.1.25:8000/xiaozhi/v1/
250705[__main__]-INFO-=======上面的地址是WebSocket协议地址，请勿用浏览器访问=======
250705[__main__]-INFO-如想测试WebSocket请启动digital-human模块，打开浏览器交互测试
250705[__main__]-INFO-=============================================================
```

Như trên, `ws://192.168.1.25:8004/mcp_endpoint/mcp/?token=abc` ở đầu ra `mcp接入点是` là `MCP接入点地址` của bạn.

`MCP接入点地址` này rất quan trọng, bạn sẽ sử dụng nó sau.

## Bước đầu tiên là tải xuống mã dự án máy tính Xia Ge MCP

Trình duyệt mở [dự án máy tính](https://github.com/78/mcp-calculator) do Anh Xia viết,

Sau khi mở nó, hãy tìm một nút màu xanh lục trên trang có nội dung `Code`, nhấp vào nút đó và sau đó bạn sẽ thấy nút `Download ZIP`.

Nhấp vào nó để tải xuống gói nén mã nguồn của dự án này. Sau khi tải về máy tính, hãy giải nén nó. Lúc này tên của nó có thể là `mcp-calculatorr-main`
Bạn cần đổi tên nó thành `mcp-calculator`. Tiếp theo, chúng ta sử dụng dòng lệnh để vào thư mục dự án và cài đặt các phần phụ thuộc.


``` bash
# Nhập thư mục dự án
máy tính cd mcp

conda remove -n mcp-calculator --all -y
conda create -n mcp-calculator python=3.10 -y
conda activate mcp-calculator

pip install -r requirements.txt
```

## Bước 2 Bắt đầu

Trước khi bắt đầu, hãy sao chép địa chỉ của điểm truy cập MCP từ phần thân thông minh của bảng điều khiển thông minh của bạn.

Ví dụ: địa chỉ mcp của đại lý của tôi là
```
ws://192.168.1.25:8004/mcp_endpoint/mcp/?token=abc
```

Bắt đầu gõ lệnh

```bash
export MCP_ENDPOINT=ws://192.168.1.25:8004/mcp_endpoint/mcp/?token=abc
```

Sau khi nhập xong, khởi động chương trình

```bash
python mcp_pipe.py calculator.py
```

### Nếu bạn đang triển khai bảng điều khiển thông minh
Nếu bạn đang triển khai bảng điều khiển thông minh, sau khi khởi động nó, bạn có thể vào lại bảng điều khiển thông minh, nhấp vào Làm mới trạng thái truy cập MCP và bạn sẽ thấy danh sách chức năng mở rộng của mình.

### Nếu bạn đang triển khai một mô-đun duy nhất
Nếu bạn triển khai một mô-đun duy nhất, khi thiết bị được kết nối, một nhật ký tương tự sẽ được xuất ra, cho biết thành công.

```
250705 -INFO-正在初始化MCP接入点: wss://2662r3426b.vicp.fun/mcp_e 
250705 -INFO-发送MCP接入点初始化消息
250705 -INFO-MCP接入点连接成功
250705 -INFO-MCP接入点初始化成功
250705 -INFO-统一工具处理器初始化完成
250705 -INFO-MCP接入点服务器信息: name=Calculator, version=1.9.4
250705 -INFO-MCP接入点支持的工具数量: 1
250705 -INFO-所有MCP接入点工具已获取，客户端准备就绪
250705 -INFO-工具缓存已刷新
250705 -INFO-当前支持的函数列表: [ 'get_time', 'get_lunar', 'play_music', 'get_weather', 'handle_exit_intent', 'calculator']
```
Nếu bao gồm `'calculator'`, điều đó có nghĩa là thiết bị sẽ có thể nhận dạng và gọi công cụ máy tính dựa trên mục đích.