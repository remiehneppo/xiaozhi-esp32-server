# get_news_from_newsnow Hướng dẫn cấu hình nguồn tin tức Plug-in

## Tổng quan

`get_news_from_newsnow` Plug-in hiện hỗ trợ cấu hình động các nguồn tin tức thông qua giao diện quản lý web, không còn yêu cầu sửa đổi mã. Người dùng có thể định cấu hình các nguồn tin tức khác nhau cho từng tác nhân trong bảng điều khiển thông minh.

## Phương thức cấu hình

### 1. Cấu hình thông qua giao diện quản lý web (khuyến nghị)

1. Đăng nhập vào bảng điều khiển thông minh
2. Nhập trang "Cấu hình vai trò"
3. Chọn tác nhân để cấu hình
4. Nhấp vào nút "Chỉnh sửa tính năng"
5. Tìm plug-in "newsnow tổng hợp tin tức" trong khu vực cấu hình tham số bên phải
6. Nhập tên tiếng Trung cách nhau bằng dấu chấm phẩy vào trường "Cấu hình nguồn tin tức"

### 2. Phương thức file cấu hình

Định cấu hình trong `config.yaml`:

```yaml
plugins:
  get_news_from_newsnow:
    url: "https://newsnow.busiyi.world/api/s?id="
    news_sources: "澎湃新闻;百度热搜;财联社;微博;抖音"
```

## Định dạng cấu hình nguồn tin tức

Cấu hình nguồn tin tức sử dụng tên tiếng Trung được phân tách bằng dấu chấm phẩy theo định dạng:

```
中文名称1;中文名称2;中文名称3
```

### Ví dụ về cấu hình

```
澎湃新闻;百度热搜;财联社;微博;抖音;知乎;36氪
```

## Nguồn tin được hỗ trợ

Plug-in hỗ trợ tên tiếng Trung của các nguồn tin tức sau:

- Giấy
- Tìm kiếm nóng của Baidu
- Báo chí liên kết tài chính
-Weibo
- TikTok
- Chí hổ
- 36 krypton
- Thông tin chi tiết về Phố Wall
- Trang chủ CNTT
- Tiêu đề của ngày hôm nay
- Hủu
- Mật độ
- Kuaishou
- Quả cầu tuyết
- Gelonghui
- Tài chính Fab
- Dữ liệu Thập Vàng
- Niuke
- thiểu số
- Cốm đất hiếm
-ifeng.com
- Bộ lạc lỗi
- Liên Hà Zaobao
- Làm mát
- Diễn đàn tầm nhìn
- Thông báo tham khảo
- Thông tấn xã vệ tinh
- Baidu Tieba
- Tin tức đáng tin cậy
- và hơn thế nữa...

##Cấu hình mặc định

Nếu nguồn tin tức không được định cấu hình, plugin sẽ sử dụng cấu hình mặc định sau:

```
澎湃新闻;百度热搜;财联社
```

##Hướng dẫn sử dụng

1. **Cấu hình nguồn tin**: Đặt tên tiếng Trung của nguồn tin trong giao diện web hoặc file cấu hình, phân cách bằng dấu chấm phẩy
2. **Gọi plug-in**: Người dùng có thể nói "báo cáo tin tức" hoặc "nhận tin tức"
3. **Chỉ định nguồn tin tức**: Người dùng có thể nói "Báo cáo bài báo" hoặc "Nhận các tìm kiếm nóng trên Baidu"
4. **Nhận thông tin chi tiết**: Người dùng có thể nói "Thông tin chi tiết về tin tức này"

## Nguyên tắc làm việc

1. Plug-in chấp nhận tên tiếng Trung làm tham số (chẳng hạn như "The Paper")
2. Theo danh sách nguồn tin tức đã định cấu hình, chuyển đổi tên tiếng Trung thành ID tiếng Anh tương ứng (chẳng hạn như "thepaper")
3. Sử dụng ID tiếng Anh để gọi API lấy dữ liệu tin tức
4. Trả lại nội dung tin tức cho người dùng

## Ghi chú

1. Tên tiếng Trung được định cấu hình phải giống hệt với tên được xác định trong CHANNEL_MAP
2. Sau khi thay đổi cấu hình, bạn cần khởi động lại dịch vụ hoặc tải lại cấu hình.
3. Nếu nguồn tin tức được định cấu hình không hợp lệ, plug-in sẽ tự động sử dụng nguồn tin tức mặc định
4. Sử dụng dấu chấm phẩy tiếng Anh (;) để phân tách nhiều nguồn tin, không sử dụng dấu chấm phẩy tiếng Trung (;)