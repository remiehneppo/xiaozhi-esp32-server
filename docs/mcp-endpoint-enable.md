Hướng dẫn sử dụng triển khai điểm truy cập #MCP

Hướng dẫn này bao gồm 3 phần
- 1. Cách triển khai dịch vụ điểm truy cập MCP
- 2. Làm cách nào để định cấu hình điểm truy cập MCP khi triển khai tất cả các mô-đun?
- 3. Làm cách nào để định cấu hình điểm truy cập MCP khi triển khai một mô-đun?

#1. Cách triển khai dịch vụ điểm truy cập MCP

## Bước đầu tiên là tải xuống mã nguồn dự án điểm truy cập mcp

Mở trình duyệt [địa chỉ dự án điểm truy cập mcp](https://github.com/xinnan-tech/mcp-endpoint-server)

Sau khi mở nó, hãy tìm một nút màu xanh lục trên trang có nội dung `Code`, nhấp vào nút đó và sau đó bạn sẽ thấy nút `Download ZIP`.

Nhấp vào nó để tải xuống gói nén mã nguồn của dự án này. Sau khi tải về máy tính, hãy giải nén nó. Lúc này tên của nó có thể là `mcp-endpoint-server-main`
Bạn cần đổi tên nó thành `mcp-endpoint-server`.

## Bước thứ hai là khởi động chương trình
Dự án này rất đơn giản và nên sử dụng docker để chạy nó. Tuy nhiên, nếu bạn không muốn sử dụng docker để chạy thì có thể tham khảo [trang này](https://github.com/xinnan-tech/mcp-endpoint-server/blob/main/README_dev.md) để chạy bằng mã nguồn. Đây là cách docker chạy

```
# Nhập thư mục gốc mã nguồn của dự án này
cd mcp-endpoint-máy chủ

# Xóa bộ nhớ đệm
docker soạn -f docker-compose.yml xuống
docker dừng mcp-endpoint-server
docker rm mcp-endpoint-server
docker rmi ghcr.nju.edu.cn/xinnan-tech/mcp-endpoint-server:latest

# Khởi động vùng chứa docker
docker soạn -f docker-compose.yml lên -d
# Xem nhật ký
nhật ký docker -f mcp-endpoint-server
```

Tại thời điểm này, nhật ký sẽ xuất ra nội dung tương tự như sau:
```
250705 INFO-=====下面的地址分别是智控台/单模块MCP接入点地址====
250705 INFO-智控台MCP参数配置: http://172.22.0.2:8004/mcp_endpoint/health?key=abc
250705 INFO-单模块部署MCP接入点: ws://172.22.0.2:8004/mcp_endpoint/mcp/?token=def
250705 INFO-=====请根据具体部署选择使用，请勿泄露给任何人======
```

Vui lòng sao chép hai địa chỉ giao diện:

Vì bạn đang triển khai bằng docker nên bạn không được sử dụng trực tiếp địa chỉ trên!

Vì bạn đang triển khai bằng docker nên bạn không được sử dụng trực tiếp địa chỉ trên!

Vì bạn đang triển khai bằng docker nên bạn không được sử dụng trực tiếp địa chỉ trên!

Đầu tiên bạn sao chép địa chỉ và viết nó vào bản nháp. Bạn cần biết IP LAN của máy tính là gì. Ví dụ: IP LAN của máy tính của tôi là `192.168.1.25`, thì
Hóa ra địa chỉ giao diện của tôi
```
智控台MCP参数配置: http://172.22.0.2:8004/mcp_endpoint/health?key=abc
单模块部署MCP接入点: ws://172.22.0.2:8004/mcp_endpoint/mcp/?token=def
```
Nó sẽ được đổi thành
```
智控台MCP参数配置: http://192.168.1.25:8004/mcp_endpoint/health?key=abc
单模块部署MCP接入点: ws://192.168.1.25:8004/mcp_endpoint/mcp/?token=def
```

Sau khi sửa đổi, vui lòng sử dụng trình duyệt của bạn để truy cập trực tiếp `智控台MCP参数配置`. Khi mã tương tự xuất hiện trên trình duyệt, điều đó có nghĩa là thành công.
```
{"result":{"status":"success","connections":{"tool_connections":0,"robot_connections":0,"tOTAl_connections":0}},"error":null,"id":null,"jsonrpc":"2.0"}
```

Vui lòng giữ lại hai `接口地址` ở trên, chúng sẽ được sử dụng trong bước tiếp theo.

# 2. Làm cách nào để định cấu hình điểm truy cập MCP khi triển khai toàn bộ mô-đun?
Trước tiên, bạn cần kích hoạt chức năng điểm truy cập MCP. Trong bảng điều khiển thông minh, nhấp vào `参数字典` ở trên cùng và trong menu thả xuống, nhấp vào trang `系统功能配置`. Kiểm tra `MCP接入点` trên trang và nhấp vào `保存配置`. Trên trang `角色配置`, nhấp vào nút `编辑功能` để xem chức năng `mcp接入点`.

Nếu bạn đang triển khai tất cả các mô-đun, hãy sử dụng tài khoản quản trị viên để đăng nhập vào bảng điều khiển thông minh, nhấp vào `参数字典` ở trên cùng và chọn chức năng `参数管理`.

Sau đó tìm kiếm tham số `server.mcp_endpoint`. Tại thời điểm này, giá trị của nó phải là giá trị `null`.
Nhấp vào nút sửa đổi và dán `智控台MCP参数配置` thu được ở bước trước vào `参数值`. Sau đó lưu lại.

Nếu có thể lưu thành công nghĩa là mọi thứ đang diễn ra tốt đẹp và bạn có thể đến đại lý để kiểm tra hiệu quả. Nếu không thành công, điều đó có nghĩa là bảng điều khiển thông minh không thể truy cập điểm truy cập mcp. Rất có thể là do tường lửa mạng hoặc địa chỉ IP LAN chính xác chưa được điền.

# 3. Làm cách nào để định cấu hình điểm truy cập MCP khi triển khai một mô-đun?

Nếu bạn đang triển khai một mô-đun duy nhất, hãy tìm tệp cấu hình `data/.config.yaml`.
Tìm kiếm `mcp_endpoint` trong tệp cấu hình. Nếu không tìm thấy thì bạn thêm cấu hình `mcp_endpoint`. Tương tự như tôi
```
máy chủ:
  WebSocket: ws://ip hoặc tên miền của bạn: số cổng/xiaozhi/v1/
  http_port: 8002
nhật ký:
  log_level: THÔNG TIN

# Có thể có thêm cấu hình ở đây..

mcp_endpoint: 你的接入点WebSocket地址
```
这时，请你把`Cách triển khai dịch vụ điểm truy cập MCP`中得到的`Điểm truy cập MCP triển khai mô-đun đơn` 粘贴到 `mcp_endpoint`. một cái gì đó như thế này

```
máy chủ:
  WebSocket: ws://ip hoặc tên miền của bạn: số cổng/xiaozhi/v1/
  http_port: 8002
nhật ký:
  log_level: THÔNG TIN

# Có thể có thêm cấu hình ở đây

mcp_endpoint: ws://192.168.1.25:8004/mcp_endpoint/mcp/?token=def
```

Sau khi cấu hình, khởi động một mô-đun sẽ xuất ra nhật ký sau.
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

Như trên, nếu `mcp接入点是` tương tự trong `ws://192.168.1.25:8004/mcp_endpoint/mcp/?token=abc` có thể xuất ra thì cấu hình thành công.

