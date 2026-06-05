# hướng dẫn tích hợp ragflow

Hướng dẫn này chủ yếu được chia thành hai phần

- 1. Cách triển khai ragflow
- 2. Cách cấu hình giao diện ragflow trên bảng điều khiển thông minh

Nếu bạn đã quen với ragflow và đã triển khai ragflow, bạn có thể bỏ qua phần đầu tiên và chuyển thẳng sang phần thứ hai. Nhưng nếu bạn muốn ai đó hướng dẫn bạn triển khai ragflow để có thể sử dụng các dịch vụ cơ bản `mysql` và `redis` cùng với `xiaozhi-esp32-server` để giảm chi phí tài nguyên, bạn cần bắt đầu từ phần đầu tiên.

# Phần 1 Cách triển khai ragflow
## Bước đầu tiên là xác nhận xem mysql và redis có sẵn hay không.

ragflow cần dựa vào cơ sở dữ liệu `mysql`. Nếu bạn đã triển khai `智控台` trước đó thì bạn đã cài đặt `mysql`. Bạn có thể chia sẻ nó.

Bạn có thể thử sử dụng lệnh `telnet` trên máy chủ để xem liệu bạn có thể truy cập cổng `3306` của `mysql` một cách bình thường hay không.
``` vỏ
telnet 127.0.0.1 3306

telnet 127.0.0.1 6379
Cổng ```
如果能访问到`3306`端口和`6379`, vui lòng bỏ qua nội dung sau và chuyển thẳng sang bước thứ hai.

Nếu bạn không thể truy cập nó, bạn cần nhớ lại cách cài đặt `mysql` của bạn.

Nếu mysql của bạn được cài đặt bằng cách sử dụng gói cài đặt, điều đó có nghĩa là `mysql` của bạn đã bị cô lập mạng. Trước tiên, bạn có thể giải quyết vấn đề truy cập vào cổng `3306` của `mysql`.

Nếu bạn đã cài đặt `mysql` đến `docker-compose_all.yml` của dự án này. Bạn cần tìm tệp `docker-compose_all.yml` nơi bạn đã tạo cơ sở dữ liệu và sửa đổi nội dung sau

Trước khi sửa đổi
``` yaml
  xiaozhi-esp32-server-db:
    ...
    networks:
      - default
    expose:
      - "3306:3306"
  xiaozhi-esp32-server-redis:
    ...
    expose:
      - 6379
```

Sau khi sửa đổi
``` yaml
  xiaozhi-esp32-server-db:
    ...
    networks:
      - default
    ports:
      - "3306:3306"
  xiaozhi-esp32-server-redis:
    ...
    ports:
      - "6379:6379"
```

Lưu ý rằng `expose` trong `xiaozhi-esp32-server-db` và `xiaozhi-esp32-server-redis` được đổi thành `ports`. Sau khi sửa đổi, bạn cần phải khởi động lại. Sau đây là lệnh khởi động lại mysql:

``` shell
# 进入你docker-compose_all.yml所在的文件夹，例如我的是xiaozhi-server
cd xiaozhi-server
docker compose -f docker-compose_all.yml down
docker compose -f docker-compose.yml up -d
```

Sau khi khởi động, hãy sử dụng lệnh `telnet` trên máy chủ để xem bạn có thể truy cập cổng `3306` của `mysql` bình thường hay không.
``` vỏ
telnet 127.0.0.1 3306

telnet 127.0.0.1 6379
```
Thông thường bạn có thể truy cập nó theo cách này.

## Bước thứ hai là tạo cơ sở dữ liệu và bảng
Nếu máy chủ của bạn có thể truy cập cơ sở dữ liệu mysql một cách bình thường thì hãy tạo cơ sở dữ liệu có tên `rag_flow` và người dùng `rag_flow` trên mysql bằng mật khẩu `infini_rag_flow`.

``` sql
--Tạo cơ sở dữ liệu
TẠO CƠ SỞ DỮ LIỆU NẾU KHÔNG TỒN TẠI rag_flow CHARACTER SET utf8mb4 THU THẬP utf8mb4_unicode_ci;

--Tạo người dùng và ủy quyền
TẠO NGƯỜI DÙNG NẾU KHÔNG TỒN TẠI 'rag_flow'@'%' ĐƯỢC XÁC ĐỊNH BỞI 'infini_rag_flow';
CẤP TẤT CẢ CÁC ĐẶC QUYỀN TRÊN rag_flow.* CHO 'rag_flow'@'%';

-- Làm mới quyền
ĐẶC QUYỀN FLUSH;
```

## Bước thứ ba là tải xuống dự án ragflow

Bạn cần tìm một thư mục trên máy tính để lưu trữ dự án ragflow. Ví dụ tôi đang ở thư mục `/home/system/xiaozhi`.

Bạn có thể sử dụng lệnh `git` để tải dự án ragflow xuống thư mục này. Hướng dẫn này sử dụng phiên bản `v0.22.0` để cài đặt và triển khai.
```
git clone https://ghfast.top/https://github.com/infiniflow/ragflow.git
cd ragflow
git checkout v0.22.0
```
Sau khi tải xuống, hãy chuyển đến thư mục `docker`.
``` shell
cd docker
```
Sửa đổi tệp `docker-compose.yml` trong thư mục `ragflow/docker` và xóa cấu hình `depends_on` của dịch vụ `ragflow-cpu` và `ragflow-gpu` để xóa sự phụ thuộc của dịch vụ `ragflow-cpu` vào `mysql`.

Đây là trước khi sửa đổi:
``` yaml
  ragflow-cpu:
    depends_on:
      mysql:
        condition: service_healthy
    profiles:
      - cpu
  ...
  ragflow-gpu:
    depends_on:
      mysql:
        condition: service_healthy
    profiles:
      - gpu
```
Đây là sau khi sửa đổi:
``` yaml
  ragflow-cpu:
    profiles:
      - cpu
  ...
  ragflow-gpu:
    profiles:
      - gpu
```

Tiếp theo, sửa đổi tệp `docker-compose-base.yml` trong thư mục `ragflow/docker` và xóa cấu hình của `mysql` và `redis`.

Ví dụ: trước khi xóa:
``` yaml
services:
  minio:
    image: quay.io/minio/minio:RELEASE.2025-06-13T11-33-47Z
    ...
  mysql:
    image: mysql:8.0
    ...
  redis:
    image: redis:6.2-alpine
    ...
```

Sau khi xóa
``` yaml
services:
  minio:
    image: quay.io/minio/minio:RELEASE.2025-06-13T11-33-47Z
    ...
```
## Bước thứ tư là sửa đổi cấu hình biến môi trường

Chỉnh sửa tệp `.env` trong thư mục `ragflow/docker`, tìm các cấu hình sau, tìm kiếm từng cái một và sửa đổi từng cái một! Tìm kiếm từng cái một và sửa đổi từng cái một!

Về việc sửa đổi tệp `.env` bên dưới, 60% mọi người sẽ bỏ qua cấu hình `MYSQL_USER` và khiến ragflow không khởi động được. Vì vậy, cần phải nhấn mạnh ba lần:

Nhấn mạnh lần đầu tiên: Nếu tệp `.env` của bạn không có cấu hình `MYSQL_USER`, vui lòng thêm tệp này vào tệp cấu hình!

Nhấn mạnh lần thứ hai: Nếu tệp `.env` của bạn không có cấu hình `MYSQL_USER`, vui lòng thêm tệp này vào tệp cấu hình!

Nhấn mạnh lần thứ ba: Nếu tệp `.env` của bạn không có cấu hình `MYSQL_USER`, vui lòng thêm tệp này vào tệp cấu hình!

``` env
# Cài đặt cổng
SVR_WEB_HTTP_PORT=8008 # cổng HTTP
SVR_WEB_HTTPS_PORT=8009 # Cổng HTTPS
Cấu hình #MySQL - sửa đổi thông tin MySQL cục bộ của bạn
MYSQL_HOST=host.docker.internal # Sử dụng Host.docker.internal để cho phép container truy cập dịch vụ máy chủ
MYSQL_PORT=3306 # Cổng MySQL cục bộ
MYSQL_USER=rag_flow # Tên người dùng đã tạo ở trên, nếu không có mục đó, hãy thêm mục này
MYSQL_PASSWORD=infini_rag_flow # Mật khẩu đã đặt ở trên
MYSQL_DBNAME=rag_flow # Tên cơ sở dữ liệu

# Cấu hình Redis - sửa đổi nó thành thông tin Redis cục bộ của bạn
REDIS_HOST=host.docker.internal # Sử dụng Host.docker.internal để cho phép container truy cập dịch vụ máy chủ
REDIS_PORT=6379 # Cổng Redis cục bộ
REDIS_PASSWORD= # Nếu Redis của bạn chưa đặt mật khẩu thì điền như thế này, nếu không thì điền mật khẩu
```

Lưu ý rằng nếu Redis của bạn không đặt mật khẩu, bạn cũng phải sửa đổi `service_conf.yaml.template` trong thư mục `ragflow/docker` và thay thế `infini_rag_flow` bằng một chuỗi trống.

Trước khi sửa đổi
``` shell
redis:
  db: 1
  password: '${REDIS_PASSWORD:-infini_rag_flow}'
  host: '${REDIS_HOST:-redis}:6379'
```
Sau khi sửa đổi
``` shell
redis:
  db: 1
  password: '${REDIS_PASSWORD:-}'
  host: '${REDIS_HOST:-redis}:6379'
```

## Bước thứ năm là khởi động dịch vụ ragflow
Thực hiện lệnh:
``` shell
docker-compose -f docker-compose.yml up -d
```
Sau khi thực hiện thành công, bạn có thể sử dụng lệnh `docker logs -n 20 -f docker-ragflow-cpu-1` để xem nhật ký của dịch vụ `docker-ragflow-cpu-1`.

Nếu không có lỗi trong nhật ký, điều đó có nghĩa là dịch vụ ragflow đã được khởi động thành công.

# Bước 5, đăng ký tài khoản
Bạn có thể truy cập `http://127.0.0.1:8008` trong trình duyệt của mình, nhấp vào `Sign Up` và đăng ký tài khoản.

Sau khi đăng ký thành công, bạn có thể nhấp vào `Sign In` để đăng nhập vào dịch vụ ragflow. Nếu bạn muốn tắt dịch vụ đăng ký dịch vụ ragflow và không muốn người khác đăng ký tài khoản, bạn có thể đặt mục cấu hình `REGISTER_ENABLED` thành `0` trong tệp `.env` trong thư mục `ragflow/docker`.

``` dotenv
REGISTER_ENABLED=0
```
Sau khi sửa đổi, khởi động lại dịch vụ ragflow.
``` shell
docker-compose -f docker-compose.yml down
docker-compose -f docker-compose.yml up -d
```

# Bước thứ sáu là định cấu hình mô hình dịch vụ ragflow.
Bạn có thể truy cập `http://127.0.0.1:8008` trong trình duyệt, nhấp vào `Sign In` và đăng nhập vào dịch vụ ragflow. Nhấp vào `头像` ở góc trên bên phải của trang để vào trang cài đặt.
Đầu tiên, nhấp vào `模型供应商` ở thanh điều hướng bên trái để vào trang cấu hình mô hình. Trong hộp tìm kiếm `可选模型` ở bên phải, chọn `LLM`, chọn nhà cung cấp mẫu bạn sử dụng trong danh sách, nhấp vào `添加` và nhập khóa của bạn;
Sau đó, chọn `TEXT EMBEDDING`, chọn nhà cung cấp mô hình bạn đang sử dụng từ danh sách, nhấp vào `添加` và nhập khóa của bạn.
Cuối cùng, làm mới trang, nhấp vào LLM và Nhúng trong danh sách `设置默认模型` rồi chọn mô hình bạn sử dụng. Vui lòng xác nhận rằng chìa khóa của bạn đã kích hoạt dịch vụ tương ứng. Ví dụ: mô hình Nhúng tôi đang sử dụng là của nhà cung cấp xxx. Bạn cần truy cập trang web chính thức của nhà cung cấp này để kiểm tra xem mô hình này có yêu cầu mua gói tài nguyên trước khi có thể sử dụng hay không.


# Phần 2 Cấu hình dịch vụ ragflow

# Bước đầu tiên là đăng nhập vào dịch vụ ragflow
Bạn có thể truy cập `http://127.0.0.1:8008` trong trình duyệt, nhấp vào `Sign In` và đăng nhập vào dịch vụ ragflow.

Sau đó nhấp vào `头像` ở góc trên bên phải để vào trang cài đặt. Trong thanh điều hướng bên trái, hãy nhấp vào chức năng `API`, sau đó nhấp vào nút "Khóa API". Một hộp bật lên xuất hiện.

Trong hộp bật lên, hãy nhấp vào nút "Tạo khóa mới" để tạo Khóa API. Sao chép `API Key` này, sau này bạn sẽ cần nó.

# Bước thứ hai là định cấu hình cho bảng điều khiển thông minh
Đảm bảo phiên bản bảng điều khiển thông minh của bạn là `0.8.7` trở lên. Đăng nhập vào bảng điều khiển thông minh bằng tài khoản quản trị viên cấp cao.

Đầu tiên, bạn cần kích hoạt chức năng cơ sở kiến ​​thức. Trong thanh điều hướng trên cùng, hãy nhấp vào `参数字典` và trong menu thả xuống, hãy nhấp vào trang `系统功能配置`. Kiểm tra `知识库` trên trang và nhấp vào `保存配置`. Bạn có thể thấy hàm `知识库` trong thanh điều hướng.

Trong thanh điều hướng trên cùng, hãy nhấp vào `模型配置` và trong thanh điều hướng bên trái, hãy nhấp vào `知识库`. Tìm `RAG_RAGFlow` trong danh sách và nhấp vào nút `编辑`.

Tại `服务地址`, điền `http://你的ragflow服务的局域网IP:8008`. Ví dụ IP LAN của dịch vụ ragflow của tôi là `192.168.1.100` thì tôi sẽ điền `http://192.168.1.100:8008`.

Trong `API密钥`, điền vào `API Key` đã sao chép trước đó.

Cuối cùng bấm vào nút lưu.

# Bước 2 Tạo cơ sở tri thức
Đăng nhập vào bảng điều khiển thông minh bằng tài khoản quản trị viên cấp cao. Trong thanh điều hướng trên cùng, hãy nhấp vào `知识库` và ở góc dưới bên trái của danh sách, hãy nhấp vào nút `新增`. Điền tên và mô tả của cơ sở kiến ​​thức. Nhấp vào Lưu.

Để nâng cao khả năng hiểu và nhớ lại cơ sở tri thức bằng các mô hình lớn, nên điền tên và mô tả có ý nghĩa khi tạo cơ sở tri thức. Ví dụ: nếu bạn đang tạo cơ sở tri thức về `公司介绍`, tên của cơ sở tri thức có thể là `公司介绍` và mô tả có thể là `关于公司的相关信息例如公司基本信息、服务项目、联系电话、地址等。`.

Sau khi lưu, bạn có thể xem cơ sở kiến ​​thức trong danh sách cơ sở kiến ​​thức. Nhấp vào nút `查看` của cơ sở tri thức bạn vừa tạo để vào trang chi tiết cơ sở tri thức.

Trong trang chi tiết cơ sở tri thức, nhấp vào nút `新增` ở góc dưới bên trái để tải tài liệu lên cơ sở tri thức.

Sau khi tải lên, bạn có thể xem tài liệu đã tải lên trên trang chi tiết cơ sở kiến ​​thức. Tại thời điểm này, bạn có thể nhấp vào nút `解析` của tài liệu để phân tích tài liệu.

Sau khi phân tích cú pháp hoàn tất, bạn có thể xem thông tin lát cắt được phân tích cú pháp. Bạn có thể kiểm tra chức năng thu hồi/truy xuất của cơ sở tri thức bằng cách nhấp vào nút `召回测试` trên trang chi tiết cơ sở tri thức.

# Bước thứ ba là để Xiaozhi sử dụng nền tảng kiến thức ragflow
Đăng nhập vào bảng điều khiển thông minh. Trong thanh điều hướng trên cùng, hãy nhấp vào `智能体`, tìm tác nhân bạn muốn định cấu hình và nhấp vào nút `配置角色`.

Ở phía bên trái của nhận dạng ý định, hãy nhấp vào nút `编辑功能` và một hộp bật lên sẽ bật lên. Chọn cơ sở kiến ​​thức bạn muốn thêm vào trong hộp bật lên. Chỉ cần lưu nó.