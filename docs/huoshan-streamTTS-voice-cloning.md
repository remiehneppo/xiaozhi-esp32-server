# Bảng điều khiển thông minh Tổng hợp giọng nói hai luồng Volcano + hướng dẫn cấu hình nhân bản giai điệu

Hướng dẫn này được chia thành 4 giai đoạn: giai đoạn chuẩn bị, giai đoạn cấu hình, giai đoạn nhân bản và giai đoạn sử dụng. Nó chủ yếu giới thiệu quy trình định cấu hình tổng hợp giọng nói dòng kép + nhân bản âm thanh của Volcano thông qua bảng điều khiển thông minh.

## Giai đoạn đầu tiên: giai đoạn chuẩn bị
Quản trị viên cấp cao trước tiên sẽ kích hoạt trước dịch vụ Volcano Engine và lấy ID ứng dụng và Mã thông báo truy cập. Theo mặc định, Huoshang Engine sẽ cung cấp tài nguyên âm thanh. Tài nguyên âm thanh này cần được sao chép vào dự án này.

Nếu bạn muốn sao chép nhiều âm sắc, bạn cần mua và kích hoạt nhiều tài nguyên âm sắc. Chỉ cần sao chép ID âm thanh (S_xxxxx) của từng tài nguyên âm thanh vào dự án này. Sau đó sử dụng tài khoản được gán cho hệ thống. Dưới đây là các bước chi tiết:

### 1. Kích hoạt dịch vụ động cơ núi lửa
Truy cập https://console.volcengine.com/speech/app, tạo một ứng dụng trong quản lý ứng dụng và kiểm tra mô hình tổng hợp giọng nói cũng như mô hình tái tạo âm thanh.

### 2. Lấy ID tài nguyên âm sắc
Truy cập https://console.volcengine.com/speech/service/9999 và sao chép ba mục, đó là Id ứng dụng, Mã thông báo truy cập và ID âm thanh (S_xxxxx). Như thể hiện trong images

![Nhận tài nguyên âm thanh](images/image-clone-integration-01.png)

## Giai đoạn 2: Cấu hình Volcano Engine Service

### 1. Điền cấu hình động cơ núi lửa

Sử dụng tài khoản quản trị viên cấp cao để đăng nhập vào bảng điều khiển thông minh, nhấp vào [Cấu hình mô hình] ở trên cùng, sau đó nhấp vào [Tổng hợp giọng nói] ở bên trái của trang cấu hình mô hình, tìm kiếm "Tổng hợp giọng nói hai luồng Volcano", nhấp vào Sửa đổi, điền `App Id` của công cụ Volcano của bạn vào trường [ID ứng dụng] và điền `Access Token` vào trường [Mã thông báo truy cập]. Sau đó lưu lại.

### 2. Gán ID tài nguyên âm sắc cho tài khoản hệ thống

Sử dụng tài khoản quản trị viên cấp cao để đăng nhập vào bảng điều khiển thông minh, nhấp vào `参数字典` ở trên cùng và trong menu thả xuống, nhấp vào trang `系统功能配置`. Kiểm tra `音色克隆` trên trang và nhấp vào Lưu cấu hình. Bạn có thể thấy nút `音色克隆` ở menu trên cùng.

Đăng nhập vào bảng điều khiển thông minh bằng tài khoản quản trị viên cấp cao và nhấp vào [Bản sao giai điệu] và [Tài nguyên giai điệu] ở trên cùng.

Nhấp vào nút Thêm và chọn "Tổng hợp giọng nói hai luồng núi lửa" trong [Tên nền tảng];

Điền ID tài nguyên âm thanh (S_xxxxx) của động cơ núi lửa của bạn vào [ID tài nguyên âm thanh], điền và nhấn Enter;

Trong [Tài khoản phân bổ], chọn tài khoản hệ thống bạn muốn chỉ định. Bạn có thể gán nó cho chính mình. Sau đó bấm lưu

## Giai đoạn thứ ba: giai đoạn nhân bản

Nếu sau khi đăng nhập, nhấp vào [Bản sao âm] và [Bản sao âm] ở trên cùng và nó hiển thị [Tài khoản của bạn hiện không có tài nguyên âm, vui lòng liên hệ với quản trị viên để phân bổ tài nguyên âm], điều đó có nghĩa là bạn chưa chỉ định ID tài nguyên âm cho tài khoản này trong giai đoạn thứ hai. Tức là quay lại giai đoạn thứ hai và phân bổ tài nguyên âm sắc cho các tài khoản tương ứng.

Nếu bạn đăng nhập, hãy nhấp vào [Tone Clone] và [Tone Clone] ở trên cùng để xem danh sách âm tương ứng. Hãy tiếp tục.

Bạn sẽ thấy danh sách âm tương ứng trong danh sách. Chọn một trong các tài nguyên âm thanh và nhấp vào nút [Tải lên âm thanh]. Sau khi tải lên, bạn có thể nghe âm thanh hoặc chặn một đoạn âm thanh nhất định. Sau khi xác nhận, hãy nhấp vào nút [Tải lên âm thanh].
![Tải âm thanh lên](images/image-clone-integration-02.png)

Sau khi tải âm thanh lên, bạn sẽ thấy trong danh sách âm sắc tương ứng sẽ trở thành "được tái tạo". Nhấp vào nút [Sao chép ngay]. Đợi 1~2 giây để trả về kết quả.

Nếu sao chép không thành công, vui lòng đặt chuột vào biểu tượng "Thông báo lỗi" và lý do thất bại sẽ được hiển thị.

Nếu sao chép thành công, bạn sẽ thấy âm báo tương ứng trong danh sách sẽ chuyển sang trạng thái "Đào tạo thành công". Tại thời điểm này, bạn có thể nhấp vào nút sửa đổi trong cột [Tên âm thanh] để sửa đổi tên của tài nguyên âm thanh nhằm thuận tiện cho việc lựa chọn và sử dụng sau này.

## Giai đoạn thứ tư: giai đoạn sử dụng

Nhấp vào [Quản lý đại lý] ở trên cùng, chọn bất kỳ đại lý nào và nhấp vào nút [Cấu hình vai trò].

Để tổng hợp giọng nói (TTS), chọn "Tổng hợp giọng nói hai luồng núi lửa". Trong danh sách, tìm tài nguyên âm thanh có tên "Clone Sound" (như trong hình), chọn tài nguyên đó và nhấp vào Lưu.
![Chọn âm](images/image-clone-integration-03.png)

Tiếp theo, bạn có thể đánh thức Xiaozhi và nói chuyện với nó.