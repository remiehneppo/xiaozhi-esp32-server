# mô tả thanh tab

`tabbar` được chia thành trường hợp `4 种`:

- 0 `无 tabbar`, chỉ có một mục trang, không có `tabbar` hiển thị ở cuối; trang hoạt động tạm thời cho các cụm từ phổ biến.
- 1 `原生 tabbar`, dùng `switchTab` để chuyển tabbar, trang `tabbar` được lưu vào bộ nhớ đệm.
  - Ưu điểm: Thanh tab gốc được hiển thị đầu tiên và được lưu vào bộ nhớ đệm.
  - Nhược điểm: Chỉ có thể sử dụng 2 bộ ảnh để chuyển đổi trạng thái đã chọn và không được chọn. Để sửa đổi màu sắc, bạn chỉ có thể thay đổi lại images (hoặc sử dụng iconfont).
- 2 `有缓存自定义 tabbar`, dùng `switchTab` để chuyển tabbar, trang `tabbar` được lưu vào bộ nhớ cache. Thành phần `tabbar` của thư viện giao diện người dùng bên thứ ba được sử dụng và hiển thị `tabbar` gốc bị ẩn.
  - Ưu điểm: Bạn có thể định cấu hình `svg icon` mà bạn muốn theo ý muốn và dễ dàng chuyển đổi màu phông chữ. Có một bộ đệm. Có thể đạt được nhiều images động lạ mắt.
  - Nhược điểm: tababr sẽ nhấp nháy khi nhấn vào lần đầu tiên.
- 3 `无缓存自定义 tabbar`, sử dụng `navigateTo` để chuyển các trang `tabbar`, `tabbar` không được lưu vào bộ nhớ đệm. Sử dụng thành phần `tabbar` của thư viện giao diện người dùng bên thứ ba.
  - Ưu điểm: Bạn có thể cấu hình biểu tượng svg theo ý muốn và dễ dàng chuyển đổi màu chữ. Có thể đạt được nhiều images động lạ mắt.
  - Nhược điểm: `tababr` sẽ nhấp nháy khi nhấp vào lần đầu tiên và không có bộ đệm.


> Lưu ý: Các hiệu ứng lạ mắt cần phải do bạn tự thực hiện, mẫu này không cung cấp.