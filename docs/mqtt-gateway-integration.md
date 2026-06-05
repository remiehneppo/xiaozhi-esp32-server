#Hướng dẫn triển khai cổng MQTT

Dự án `xiaozhi-esp32-server` có thể được kết hợp với dự án mã nguồn mở [xiaozhi-mqtt-gateway](https://github.com/78/xiaozhi-mqtt-gateway) của Xia Ge để thực hiện các sửa đổi đơn giản nhằm hiện thực hóa kết nối MQTT+UDP phần cứng Xiaozhi.
Hướng dẫn này được chia thành ba phần. Bạn có thể chọn phần tương ứng để truy cập cổng MQTT tùy theo việc bạn đang triển khai một mô-đun đầy đủ hay một mô-đun duy nhất:
- Phần 1: Triển khai MQTT Gateway
- Phần 2: Vận hành mô-đun đầy đủ để hiện thực hóa kết nối MQTT+UDP phần cứng Xiaozhi
- Phần 3: Chạy xiaozhi-server trên một mô-đun duy nhất để hiện thực hóa kết nối MQTT+UDP của phần cứng Xiaozhi

##Giai đoạn chuẩn bị
Chuẩn bị sẵn địa chỉ kết nối `xiaozhi-server` và `mqtt-WebSocket` của bạn. Dựa trên `WebSocket地址` ban đầu của bạn, hãy thêm các ký tự `?from=mqtt_gateway` để lấy địa chỉ kết nối `mqtt-WebSocket`

1. Nếu bạn đang triển khai mã nguồn, địa chỉ `mqtt-WebSocket` của bạn là:
```
ws://127.0.0.1:8000/xiaozhi/v1/?from=mqtt_gateway
```

2. Nếu bạn đang triển khai bằng docker, địa chỉ `mqtt-WebSocket` của bạn là
```
ws://你宿主机局域网IP:8000/xiaozhi/v1/?from=mqtt_gateway
```

## LƯU Ý QUAN TRỌNG

Nếu bạn đang triển khai trên máy chủ, bạn cần đảm bảo rằng các cổng `1883`, `8884` và `8007` của máy chủ được mở với thế giới bên ngoài. Loại giao thức được `8884` chọn là `UDP` và các loại giao thức khác là `TCP`.

Nếu bạn đang triển khai trên máy chủ, bạn cần đảm bảo rằng các cổng `1883`, `8884` và `8007` của máy chủ được mở với thế giới bên ngoài. Loại giao thức được `8884` chọn là `UDP` và các loại giao thức khác là `TCP`.

Nếu bạn đang triển khai trên máy chủ, bạn cần đảm bảo rằng các cổng `1883`, `8884` và `8007` của máy chủ được mở với thế giới bên ngoài. Loại giao thức được `8884` chọn là `UDP` và các loại giao thức khác là `TCP`.


## Phần 1: Triển khai MQTT Gateway

1. Bản sao [dự án xiaozhi-mqtt-gateway đã sửa đổi](https://github.com/xinnan-tech/xiaozhi-mqtt-gateway.git):
```bash
git clone https://ghfast.top/https://github.com/xinnan-tech/xiaozhi-mqtt-gateway.git
cd xiaozhi-mqtt-gateway
```

2. Cài đặt phụ thuộc:
```bash
npm install
npm install -g pm2
```

3. Cấu hình `config.json`:
```bash
cp config/mqtt.json.example config/mqtt.json
```

4. Chỉnh sửa tệp cấu hình config/mqtt.json và thay thế địa chỉ `mqtt-WebSocket` của bạn trong `本文准备阶段` bằng `chat_servers`. Ví dụ: mã nguồn được triển khai `xiaozhi-server` được định cấu hình như sau:

``` 
{
    "production": {
        "chat_servers": [
            "ws://127.0.0.1:8000/xiaozhi/v1/?from=mqtt_gateway"
        ]
    },
    "debug": false,
    "max_mqtt_payload_size": 8192,
    "mcp_client": {
        "capabilities": {
        },
        "client_info": {
            "name": "xiaozhi-mqtt-client",
            "version": "1.0.0"
        },
        "max_tools_count": 128
    }
}
```
5. Tạo tệp `.env` trong thư mục gốc của dự án và đặt các biến môi trường sau:
```
PUBLIC_IP=your-ip         # 服务器公网IP
MQTT_PORT=1883            # MQTT服务器端口
UDP_PORT=8884             # UDP服务器端口
API_PORT=8007             # 管理API端口
MQTT_SIGNATURE_KEY=test   # MQTT签名密钥
SERVER_SECRET=Te1st12134  # 服务器密钥，请保持和智控台（server.secret）一致或者和xiaozhi-server里（server.auth_key）保持一致
```
Vui lòng chú ý đến cấu hình `PUBLIC_IP` và đảm bảo nó phù hợp với IP mạng công cộng thực tế. Nếu có tên miền thì điền tên miền vào.

`MQTT_SIGNATURE_KEY` là khóa được sử dụng để xác thực kết nối MQTT. Tốt nhất là đặt nó thành một cái gì đó phức tạp hơn. Tốt nhất nên đặt nó nhiều hơn 8 ký tự và chứa cả chữ hoa và chữ thường. Chìa khóa này sẽ được sử dụng sau này.

- Cẩn thận không sử dụng các mật khẩu đơn giản, chẳng hạn như `123456`, `test`, v.v.
- Cẩn thận không sử dụng các mật khẩu đơn giản, chẳng hạn như `123456`, `test`, v.v.
- Cẩn thận không sử dụng các mật khẩu đơn giản, chẳng hạn như `123456`, `test`, v.v.

`SERVER_SECRET` được sử dụng để tạo thông tin xác thực cho các kết nối WebSocket.

1. Nếu bạn triển khai một mô-đun đầy đủ và `server.auth.enabled` được đặt thành `true` trong phần quản lý tham số của bảng điều khiển thông minh thì `SERVER_SECRET` cần phải nhất quán với bảng điều khiển thông minh (`server.secret`).

2. Nếu bạn đang triển khai một mô-đun duy nhất và bạn đặt `server.auth.enabled` thành `true` trong tệp cấu hình thì `SERVER_SECRET` cần phải nhất quán với tệp cấu hình (`server.auth_key`).


6. Khởi động cổng MQTT
```
# Bắt đầu dịch vụ
pm2 bắt đầu hệ sinh thái.config.js

# Xem nhật ký
nhật ký pm2 xz-mqtt
```

Khi bạn thấy nhật ký sau, điều đó có nghĩa là cổng MQTT đã được khởi động thành công:
```
0|xz-mqtt  | 2025-09-11T12:14:48: MQTT 服务器正在监听端口 1883
0|xz-mqtt  | 2025-09-11T12:14:48: UDP 服务器正在监听 x.x.x.x:8884
```

Nếu bạn cần khởi động lại cổng MQTT, hãy thực hiện lệnh sau:
```
pm2 restart xz-mqtt
```

## Phần 2: Vận hành mô-đun đầy đủ để triển khai kết nối MQTT+UDP phần cứng Xiaozhi

Kiểm tra số phiên bản ở cuối trang chủ bảng điều khiển thông minh của bạn để xác nhận xem phiên bản bảng điều khiển thông minh của bạn là `0.7.7` trở lên. Nếu không, bạn cần nâng cấp bảng điều khiển thông minh.

1. Ở đầu bảng điều khiển thông minh, hãy nhấp vào `参数管理`, tìm kiếm `server.mqtt_gateway`, nhấp vào Chỉnh sửa và điền `PUBLIC_IP`+`:`+`MQTT_PORT` mà bạn đặt trong tệp `.env`. một cái gì đó như thế này
```
192.168.0.7:1883
```
2. Ở đầu bảng điều khiển thông minh, hãy nhấp vào `参数管理`, tìm kiếm `server.mqtt_signature_key`, nhấp vào Chỉnh sửa và điền `MQTT_SIGNATURE_KEY` mà bạn đặt trong tệp `.env`.

3. Ở đầu bảng điều khiển thông minh, hãy nhấp vào `参数管理`, tìm kiếm `server.udp_gateway`, nhấp vào Chỉnh sửa và điền `PUBLIC_IP`+`:`+`UDP_PORT` mà bạn đặt trong tệp `.env`. một cái gì đó như thế này
```
192.168.0.7:8884
```
4. Ở đầu bảng điều khiển thông minh, hãy nhấp vào `参数管理`, tìm kiếm `server.mqtt_manager_api`, nhấp vào Chỉnh sửa và điền `PUBLIC_IP`+`:`+`API_PORT` mà bạn đặt trong tệp `.env`. một cái gì đó như thế này
```
192.168.0.7:8007
```

Sau khi hoàn tất cấu hình ở trên, bạn có thể sử dụng lệnh cuộn tròn để xác minh xem địa chỉ OTA của bạn có cung cấp cấu hình mqtt hay không và thay đổi `http://localhost:8002/xiaozhi/OTA/` sau thành địa chỉ OTA của bạn.
```
curl 'http://localhost:8002/xiaozhi/OTA/' \
  -H 'Content-Type: application/json' \
  -H 'Client-Id: 7b94d69a-9808-4c59-9c9b-704333b38aff' \
  -H 'Device-Id: 11:22:33:44:55:66' \
  --data-raw $'{\n  "application": {\n    "version": "1.0.1",\n    "elf_sha256": "1"\n  },\n  "board": {\n    "mac": "11:22:33:44:55:66"\n  }\n}'
```

Nếu nội dung trả về chứa cấu hình liên quan đến `mqtt` thì cấu hình thành công. một cái gì đó như thế này

```
{"server_time":{"timestamp":1757567894012,"timeZone":"Asia/Shanghai","timezone_offset":480},"activation":{"code":"460609","message":"http://xiaozhi.server.com\n460609","challenge":"11:22:33:44:55:66"},"firmware":{"version":"1.0.1","url":"http://xiaozhi.server.com:8002/xiaozhi/otaMag/download/NOT_ACTIVATED_FIRMWARE_THIS_IS_A_INVALID_URL"},"websocket":{"url":"ws://192.168.4.23:8000/xiaozhi/v1/"},"mqtt":{"endpoint":"192.168.0.7:1883","client_id":"GID_default@@@11_22_33_44_55_66@@@7b94d69a-9808-4c59-9c9b-704333b38aff","username":"eyJpcCI6IjA6MDowOjA6MDowOjA6MSJ9","password":"Y8XP9xcUhVIN9OmbCHT9ETBiYNE3l3Z07Wk46wV9PE8=","publish_topic":"device-server","subscribe_topic":"devices/p2p/11_22_33_44_55_66"}}
```

Vì thông tin MQTT cần được gửi bằng địa chỉ OTA nên chỉ bạn mới có thể đảm bảo rằng mình có thể kết nối với địa chỉ OTA của máy chủ một cách bình thường và khởi động lại để đánh thức nó.

Sau khi thức dậy, hãy chú ý đến nhật ký của mqtt-gateway để xác nhận xem có nhật ký kết nối thành công hay không.
```
pm2 logs xz-mqtt
```

## Phần 3: Mô-đun đơn chạy xiaozhi-server để nhận ra kết nối MQTT+UDP phần cứng Xiaozhi

Mở tệp `data/.config.yaml` của bạn, tìm `mqtt_gateway` trong `server` và điền vào `PUBLIC_IP`+`:`+`MQTT_PORT` bạn đặt trong tệp `.env`. một cái gì đó như thế này
```
192.168.0.7:1883
```
Tìm `mqtt_signature_key` trong `server` và điền `MQTT_SIGNATURE_KEY` bạn đặt trong tệp `.env`.

Tìm `udp_gateway` trong `server` và điền vào `PUBLIC_IP`+`:`+`UDP_PORT` bạn đặt trong tệp `.env`. một cái gì đó như thế này
```
192.168.0.7:8884
```

Sau khi hoàn tất cấu hình ở trên, bạn có thể sử dụng lệnh cuộn tròn để xác minh xem địa chỉ OTA của bạn có cung cấp cấu hình mqtt hay không và thay đổi `http://localhost:8002/xiaozhi/OTA/` sau thành địa chỉ OTA của bạn.
```
curl 'http://localhost:8002/xiaozhi/OTA/' \
  -H 'Device-Id: 11:22:33:44:55:66' \
  --data-raw $'{\n  "application": {\n    "version": "1.0.1",\n    "elf_sha256": "1"\n  },\n  "board": {\n    "mac": "11:22:33:44:55:66"\n  }\n}'
```

Nếu nội dung trả về chứa cấu hình liên quan đến `mqtt` thì cấu hình thành công. một cái gì đó như thế này
```
{"server_time":{"timestamp":1758781561083,"timeZone":"GMT+08:00","timezone_offset":480},"activation":{"code":"527111","message":"http://xiaozhi.server.com\n527111","challenge":"11:22:33:44:55:66"},"firmware":{"version":"1.0.1","url":"http://xiaozhi.server.com:8002/xiaozhi/OTAMag/download/NOT_ACTIVATED_FIRMWARE_THIS_IS_A_INVALID_URL"},"WebSocket":{"url":"ws://192.168.1.15:8000/xiaozhi/v1/"},"mqtt":{"endpoint":"192.168.1.15:1883","client_id":"GID_default@@@11_22_33_44_55_66@@@11_22_33_44_55_66","username":"eyJpcCI6IjE5Mi4xNjguMS4xNSJ9","password":"fjAYs49zTJecWqJ3jBt+kqxVn/x7vkXRAc85ak/va7Y=","publish_topic":"device-server","subscribe_topic":"devices/p2p/11_22_33_44_55_66"}}
```

Vì thông tin MQTT cần được gửi bằng địa chỉ OTA nên chỉ bạn mới có thể đảm bảo rằng mình có thể kết nối với địa chỉ OTA của máy chủ một cách bình thường và khởi động lại để đánh thức nó.

Sau khi thức dậy, hãy chú ý đến nhật ký của mqtt-gateway để xác nhận xem có nhật ký kết nối thành công hay không.
```
pm2 logs xz-mqtt
```