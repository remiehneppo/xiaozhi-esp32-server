# Định cấu hình máy chủ tùy chỉnh dựa trên phần sụn do Xiago biên soạn

## Bước 1 Xác nhận phiên bản
Ghi phiên bản đã biên dịch của Xia Ge [phiên bản firmware 1.6.1 trở lên](https://github.com/78/xiaozhi-esp32/releases)

## Bước 2 Chuẩn bị địa chỉ OTA của bạn
Nếu bạn làm theo hướng dẫn và sử dụng triển khai mô-đun đầy đủ thì sẽ có địa chỉ OTA.

Tại thời điểm này, vui lòng sử dụng trình duyệt của bạn để mở địa chỉ OTA của bạn, ví dụ: địa chỉ OTA của tôi
```
https://2662r3426b.vicp.fun/xiaozhi/OTA/
```

Nếu "Giao diện OTA đang chạy bình thường, số cụm WebSocket: X" được hiển thị. Sau đó đi xuống.

Nếu thông báo "Giao diện OTA không hoạt động bình thường" thì có thể là do bạn chưa định cấu hình địa chỉ `WebSocket` trong `智控台`. Sau đó:

- 1. Sử dụng quản trị viên cấp cao để đăng nhập vào bảng điều khiển thông minh

- 2. Nhấp vào `参数管理` ở menu trên cùng

- 3. Tìm mục `server.WebSocket` trong danh sách và nhập địa chỉ `WebSocket` của bạn. Ví dụ, của tôi là

```
wss://2662r3426b.vicp.fun/xiaozhi/v1/
```

Sau khi cấu hình xong, bạn dùng trình duyệt để làm mới địa chỉ giao diện OTA của mình xem có bình thường không. Nếu vẫn không bình thường, hãy kiểm tra lại xem WebSocket có khởi động bình thường không và địa chỉ WebSocket đã được định cấu hình chưa.

## Bước 3 Vào chế độ phân phối mạng
Nhập chế độ cấu hình mạng của máy, nhấp vào "Tùy chọn nâng cao" ở đầu trang, nhập địa chỉ `OTA` máy chủ của bạn và nhấp vào Lưu. Khởi động lại thiết bị
![Vui lòng tham khảo cài đặt địa chỉ-OTA](../docs/images/firmware-setting-OTA.png)

## Bước 4 Đánh thức Xiaozhi và kiểm tra đầu ra nhật ký

Hãy đánh thức Xiaozhi và xem nhật ký có xuất ra bình thường không.


## Câu hỏi thường gặp
Dưới đây là một số câu hỏi thường gặp để tham khảo:

[1. Tại sao Xiaozhi nhận ra nhiều tiếng Hàn, tiếng Nhật và tiếng Anh khi tôi nói](./FAQ.md)

[2. Tại sao lại xuất hiện thông báo "Tệp lỗi tác vụ TTS không tồn tại"? ](./FAQ.md)

[3. TTS thường bị lỗi và hết thời gian chờ](./FAQ.md)

[4. Bạn có thể kết nối với máy chủ tự xây dựng bằng Wifi, nhưng không thể kết nối ở chế độ 4G](./FAQ.md)

[5. Làm cách nào để cải thiện tốc độ phản hồi đối thoại của Xiaozhi? ](./FAQ.md)

[6. Tôi nói rất chậm và Xiaozhi luôn nắm bắt được cuộc trò chuyện khi tôi tạm dừng](./FAQ.md)

[7. Tôi muốn điều khiển đèn, điều hòa, bật/tắt từ xa và các hoạt động khác thông qua Xiaozhi](./FAQ.md)