# Hướng dẫn tích hợp SMS trên nền tảng đám mây của Alibaba

Đăng nhập vào bảng điều khiển Đám mây của Alibaba và vào trang "Dịch vụ SMS": https://dysms.console.aliyun.com/overview

## Bước 1: Thêm chữ ký
![Bước](images/alisms/sms-01.png)
![Bước](images/alisms/sms-02.png)

Sau các bước trên, bạn sẽ nhận được chữ ký. Hãy ghi nó vào các thông số của bảng điều khiển thông minh, `aliyun.sms.sign_name`

## Bước 2 Thêm mẫu
![Bước](images/alisms/sms-11.png)

Sau các bước trên, bạn sẽ nhận được mã mẫu. Hãy ghi nó vào các thông số của bảng điều khiển thông minh, `aliyun.sms.sms_code_template_code`

Lưu ý chữ ký sẽ mất 7 ngày làm việc mới được gửi thành công sau khi tổng đài báo thành công.

Lưu ý chữ ký sẽ mất 7 ngày làm việc mới được gửi thành công sau khi tổng đài báo thành công.

Lưu ý chữ ký sẽ mất 7 ngày làm việc mới được gửi thành công sau khi tổng đài báo thành công.

Bạn có thể đợi cho đến khi báo cáo thành công trước khi tiếp tục.

## Bước 3: Tạo tài khoản SMS và kích hoạt quyền

Đăng nhập vào bảng điều khiển Alibaba Cloud và vào trang "Kiểm soát truy cập": https://ram.console.aliyun.com/overview?activeTab=overview

![Bước](images/alisms/sms-21.png)
![Bước](images/alisms/sms-22.png)
![Bước](images/alisms/sms-23.png)
![Bước](images/alisms/sms-24.png)
![Bước](images/alisms/sms-25.png)

Ở các bước trên, bạn sẽ nhận được access_key_id và access_key_secret. Hãy ghi chúng vào các thông số của bảng điều khiển thông minh, `aliyun.sms.access_key_id`, `aliyun.sms.access_key_secret`
## Bước 4: Khởi động chức năng đăng ký điện thoại di động

1. Thông thường sau khi điền các thông tin trên sẽ có hiện tượng này. Nếu không, có thể thiếu một bước nào đó.

![Bước](images/alisms/sms-31.png)

2. Cho phép người dùng không phải quản trị viên đăng ký và đặt tham số `server.allow_user_register` thành `true`

3. Kích hoạt chức năng đăng ký điện thoại di động và đặt tham số `server.enable_mobile_register` thành `true`
![Bước](images/alisms/sms-32.png)