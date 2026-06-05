# biên dịch phần mềm ESP32

## Bước 1 Chuẩn bị địa chỉ OTA của bạn

Nếu bạn đang sử dụng phiên bản 0.3.12 của dự án này, cho dù đó là triển khai máy chủ đơn giản hay triển khai mô-đun đầy đủ, sẽ có địa chỉ OTA.

Do các phương pháp cài đặt địa chỉ OTA để triển khai máy chủ đơn giản và triển khai mô-đun đầy đủ là khác nhau, vui lòng chọn phương pháp cụ thể sau:

### Nếu bạn đang sử dụng triển khai Máy chủ đơn giản
Tại thời điểm này, vui lòng sử dụng trình duyệt của bạn để mở địa chỉ OTA của bạn, ví dụ: địa chỉ OTA của tôi
```
http://192.168.1.25:8003/xiaozhi/OTA/
```
Nếu hiển thị "Giao diện OTA đang chạy bình thường thì địa chỉ WebSocket gửi tới thiết bị là: ws://xxx:8000/xiaozhi/v1/

Bạn có thể khởi động mô-đun `digital-human` rồi mở `index.html` để kiểm tra xem bạn có thể kết nối với đầu ra địa chỉ WebSocket của trang OTA hay không.

Nếu không thể truy cập được, bạn cần sửa đổi địa chỉ của `server.WebSocket` trong tệp cấu hình `.config.yaml`, khởi động lại rồi kiểm tra lại cho đến khi `index.html` có thể truy cập bình thường.

Sau khi thành công, vui lòng chuyển sang bước 2.

### Nếu bạn đang sử dụng triển khai mô-đun đầy đủ
Tại thời điểm này, vui lòng sử dụng trình duyệt của bạn để mở địa chỉ OTA của bạn, ví dụ: địa chỉ OTA của tôi
```
http://192.168.1.25:8002/xiaozhi/OTA/
```

Nếu "Giao diện OTA đang chạy bình thường, số cụm WebSocket: X" được hiển thị. Sau đó tiến hành 2 bước tiếp theo.

Nếu thông báo "Giao diện OTA không hoạt động bình thường" thì có thể là do bạn chưa định cấu hình địa chỉ `WebSocket` trong `智控台`. Sau đó:

- 1. Sử dụng quản trị viên cấp cao để đăng nhập vào bảng điều khiển thông minh

- 2. Nhấp vào `参数管理` ở menu trên cùng

- 3. Tìm mục `server.WebSocket` trong danh sách và nhập địa chỉ `WebSocket` của bạn. Ví dụ, của tôi là

```
ws://192.168.1.25:8000/xiaozhi/v1/
```

Sau khi cấu hình xong, bạn dùng trình duyệt để làm mới địa chỉ giao diện OTA của mình xem có bình thường không. Nếu vẫn không bình thường, hãy kiểm tra lại xem WebSocket có khởi động bình thường không và địa chỉ WebSocket đã được định cấu hình chưa.

## Bước 2 Cấu hình môi trường
Trước tiên, hãy làm theo hướng dẫn này để định cấu hình môi trường dự án ["Xây dựng môi trường phát triển ESP IDF 5.3.2 và biên dịch Xiaozhi trên Windows"](https://icnynnzcwou8.feishu.cn/wiki/JEYDwTTALi5s2zkGlFGcDiRknXf)

## Bước 3 Mở file cấu hình
Sau khi định cấu hình môi trường biên dịch, hãy tải xuống mã nguồn của dự án xiaozhi-esp32.

Tải xuống  [mã nguồn dự án xiaozhi-esp32](https://github.com/78/xiaozhi-esp32) từ đây.

Sau khi tải xuống, hãy mở tệp `xiaozhi-esp32/main/Kconfig.projbuild`.

## Bước 4 Chỉnh sửa địa chỉ OTA

Tìm nội dung `default` của `OTA_URL` và đặt `https://api.tenclass.net/xiaozhi/OTA/`
   Thay đổi nó thành địa chỉ của riêng bạn. Ví dụ: nếu địa chỉ giao diện của tôi là `http://192.168.1.25:8002/xiaozhi/OTA/`, hãy thay đổi nội dung thành địa chỉ này.

Trước khi sửa đổi:
```
config OTA_URL
    string "Default OTA URL"
    default "https://api.tenclass.net/xiaozhi/OTA/"
    help
        The application will access this URL to check for new firmwares and server address.
```
Sau khi sửa đổi:
```
config OTA_URL
    string "Default OTA URL"
    default "http://192.168.1.25:8002/xiaozhi/OTA/"
    help
        The application will access this URL to check for new firmwares and server address.
```

## Bước 4 Thiết lập tham số biên dịch

Đặt tham số biên dịch

```
# 终端命令行进入xiaozhi-esp32的根目录
cd xiaozhi-esp32
# 例如我使用的板子是esp32s3，所以设置编译目标为esp32s3，如果你的板子是其他型号，请替换成对应的型号
idf.py set-target esp32s3
# 进入菜单配置
idf.py menuconfig
```

Sau khi vào cấu hình menu, hãy nhập `Xiaozhi Assistant` và đặt `BOARD_TYPE` cho kiểu bo mạch cụ thể của bạn.
Lưu và thoát và quay lại dòng lệnh terminal.

## Bước 5 Biên dịch firmware

```
idf.py build
```

## Bước 6 Firmware thùng gói

```
cd scripts
python release.py
```

Sau khi lệnh đóng gói ở trên được thực thi, tệp chương trình cơ sở `merged-binary.bin` sẽ được tạo trong thư mục `build` trong thư mục gốc của dự án.
`merged-binary.bin` này là tệp chương trình cơ sở được ghi vào phần cứng.

Lưu ý: Nếu xảy ra lỗi liên quan đến "zip" sau khi thực hiện lệnh thứ hai, vui lòng bỏ qua lỗi này và chỉ tạo tệp chương trình cơ sở `merged-binary.bin` trong thư mục `build`.
, nó sẽ không ảnh hưởng nhiều đến bạn đâu, vui lòng tiếp tục.

## Bước 7 Ghi firmware
   Kết nối thiết bị ESP32 với máy tính, sử dụng trình duyệt Chrome và mở URL sau

```
https://espressif.github.io/esp-launchpad/
```

Mở hướng dẫn này, [Công cụ Flash/Phần mềm ghi đĩa phía web (không có môi trường phát triển IDF)](https://ccnphfhqs21z.feishu.cn/wiki/Zpz4wXBtdimBrLk25WdcXzxcnNS).
Chuyển sang: `方式二：ESP-Launchpad 浏览器WEB端烧录`, bắt đầu từ `3. 烧录固件/下载到开发板` và làm theo hướng dẫn.

Sau khi ghi thành công và kết nối mạng thành công, hãy đánh thức Xiaozhi thông qua từ đánh thức và chú ý đến thông tin bảng điều khiển do máy chủ xuất ra.

## Câu hỏi thường gặp
Dưới đây là một số câu hỏi thường gặp để tham khảo:

[1. Tại sao Xiaozhi nhận ra nhiều tiếng Hàn, tiếng Nhật và tiếng Anh khi tôi nói](./FAQ.md)

[2. Tại sao lại xuất hiện thông báo "Tệp lỗi tác vụ TTS không tồn tại"? ](./FAQ.md)

[3. TTS thường bị lỗi và hết thời gian chờ](./FAQ.md)

[4. Bạn có thể kết nối với máy chủ tự xây dựng bằng Wifi, nhưng không thể kết nối ở chế độ 4G](./FAQ.md)

[5. Làm cách nào để cải thiện tốc độ phản hồi đối thoại của Xiaozhi? ](./FAQ.md)

[6. Tôi nói rất chậm và Xiaozhi luôn nắm bắt được cuộc trò chuyện khi tôi tạm dừng](./FAQ.md)

[7. Tôi muốn điều khiển đèn, điều hòa, bật/tắt từ xa và các hoạt động khác thông qua Xiaozhi](./FAQ.md)