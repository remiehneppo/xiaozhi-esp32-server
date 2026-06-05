# Hướng dẫn kích hoạt nhận dạng giọng nói

Hướng dẫn này bao gồm 3 phần
- 1. Cách triển khai dịch vụ nhận dạng giọng nói
- 2. Làm cách nào để định cấu hình giao diện nhận dạng giọng nói khi triển khai toàn bộ mô-đun?
- 3. Cách cấu hình nhận dạng giọng nói khi triển khai đơn giản nhất

#1. Cách triển khai dịch vụ nhận dạng giọng nói

## Bước đầu tiên là tải xuống mã nguồn dự án nhận dạng giọng nói

Mở trình duyệt [Địa chỉ dự án nhận dạng giọng nói](https://github.com/xinnan-tech/voiceprint-api)

Sau khi mở nó, hãy tìm một nút màu xanh lục trên trang có nội dung `Code`, nhấp vào nút đó và sau đó bạn sẽ thấy nút `Download ZIP`.

Nhấp vào nó để tải xuống gói nén mã nguồn của dự án này. Sau khi tải về máy tính, hãy giải nén nó. Lúc này tên của nó có thể là `voiceprint-api-main`
Bạn cần đổi tên nó thành `voiceprint-api`.

## Bước thứ hai là tạo cơ sở dữ liệu và bảng

Nhận dạng giọng nói dựa trên cơ sở dữ liệu `mysql`. Nếu bạn đã triển khai `智控台` trước đó thì bạn đã cài đặt `mysql`. Bạn có thể chia sẻ nó.

Bạn có thể thử sử dụng lệnh `telnet` trên máy chủ để xem liệu bạn có thể truy cập cổng `3306` của `mysql` một cách bình thường hay không.
```
telnet 127.0.0.1 3306
```
Nếu bạn có thể truy cập cổng 3306, vui lòng bỏ qua nội dung sau và chuyển thẳng đến bước ba.

Nếu bạn không thể truy cập nó, bạn cần nhớ lại cách cài đặt `mysql` của bạn.

Nếu mysql của bạn được cài đặt bằng cách sử dụng gói cài đặt, điều đó có nghĩa là `mysql` của bạn đã bị cô lập mạng. Trước tiên, bạn có thể giải quyết vấn đề truy cập vào cổng `3306` của `mysql`.

Nếu bạn đã cài đặt `mysql` đến `docker-compose_all.yml` của dự án này. Bạn cần tìm tệp `docker-compose_all.yml` nơi bạn đã tạo cơ sở dữ liệu và sửa đổi nội dung sau

Trước khi sửa đổi
```
  xiaozhi-esp32-server-db:
    ...
    networks:
      - default
    expose:
      - "3306:3306"
```

Sau khi sửa đổi
```
  xiaozhi-esp32-server-db:
    ...
    networks:
      - default
    ports:
      - "3306:3306"
```

Lưu ý rằng `expose` trong `xiaozhi-esp32-server-db` được đổi thành `ports`. Sau khi sửa đổi, bạn cần phải khởi động lại. Sau đây là lệnh khởi động lại mysql:

```
# 进入你docker-compose_all.yml所在的文件夹，例如我的是xiaozhi-server
cd xiaozhi-server
docker compose -f docker-compose_all.yml down
docker compose -f docker-compose.yml up -d
```

Sau khi khởi động, hãy sử dụng lệnh `telnet` trên máy chủ để xem bạn có thể truy cập cổng `3306` của `mysql` bình thường hay không.
```
telnet 127.0.0.1 3306
```
Thông thường bạn có thể truy cập nó theo cách này.

## Bước thứ ba là tạo cơ sở dữ liệu và bảng
Nếu máy chủ của bạn có thể truy cập cơ sở dữ liệu mysql một cách bình thường, hãy tạo cơ sở dữ liệu có tên `voiceprint_db` và bảng `voiceprints` trên mysql.

```
CREATE DATABASE voiceprint_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE voiceprint_db;

CREATE TABLE voiceprints (
    id INT AUTO_INCREMENT PRIMARY KEY,
    speaker_id VARCHAR(255) NOT NULL UNIQUE,
    feature_vector LONGBLOB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_speaker_id (speaker_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

## Bước 4, cấu hình kết nối cơ sở dữ liệu

Nhập thư mục `voiceprint-api` và tạo thư mục có tên `data`.

Sao chép `voiceprint.yaml` trong thư mục gốc `voiceprint-api` vào thư mục `data` và đổi tên thành `.voiceprint.yaml`

Tiếp theo, bạn cần tập trung vào việc định cấu hình kết nối cơ sở dữ liệu trong `.voiceprint.yaml`.

```
mysql:
  host: "127.0.0.1"
  port: 3306
  user: "root"
  password: "your_password"
  database: "voiceprint_db"
```

Để ý! Vì dịch vụ nhận dạng giọng nói của bạn được triển khai bằng docker nên `host` cần được điền là `mysql所在机器的局域网ip` của bạn.

Để ý! Vì dịch vụ nhận dạng giọng nói của bạn được triển khai bằng docker nên `host` cần được điền là `mysql所在机器的局域网ip` của bạn.

Để ý! Vì dịch vụ nhận dạng giọng nói của bạn được triển khai bằng docker nên `host` cần được điền là `mysql所在机器的局域网ip` của bạn.

## Bước 5, khởi động chương trình
Dự án này rất đơn giản và nên sử dụng docker để chạy nó. Tuy nhiên, nếu bạn không muốn sử dụng docker để chạy thì có thể tham khảo [trang này](https://github.com/xinnan-tech/voiceprint-api/blob/main/README.md) để chạy bằng mã nguồn. Đây là cách docker chạy

```
# Nhập thư mục gốc mã nguồn của dự án này
cd voiceprint-api

# Xóa bộ nhớ đệm
docker soạn -f docker-compose.yml xuống
docker dừng voiceprint-api
docker rm voiceprint-api
docker rmi ghcr.nju.edu.cn/xinnan-tech/voiceprint-api:latest

# Khởi động vùng chứa docker
docker soạn -f docker-compose.yml lên -d
# Xem nhật ký
nhật ký docker -f voiceprint-api
```

Tại thời điểm này, nhật ký sẽ xuất ra nội dung tương tự như sau:
```
250711 INFO-🚀 开始: 生产环境服务启动（Uvicorn），监听地址: 0.0.0.0:8005
250711 INFO-============================================================
250711 INFO-声纹接口地址: http://127.0.0.1:8005/voiceprint/health?key=abcd
250711 INFO-============================================================
```

Vui lòng sao chép địa chỉ giao diện voiceprint:

Vì bạn đang triển khai bằng docker nên bạn không được sử dụng trực tiếp địa chỉ trên!

Vì bạn đang triển khai bằng docker nên bạn không được sử dụng trực tiếp địa chỉ trên!

Vì bạn đang triển khai bằng docker nên bạn không được sử dụng trực tiếp địa chỉ trên!

Đầu tiên bạn sao chép địa chỉ và viết nó vào bản nháp. Bạn cần biết IP LAN của máy tính là gì. Ví dụ: IP LAN của máy tính của tôi là `192.168.1.25`, thì
Hóa ra địa chỉ giao diện của tôi
```
http://127.0.0.1:8005/voiceprint/health?key=abcd

```
就要改成
```
http://192.168.1.25:8005/voiceprint/health?key=abcd
```

Sau khi sửa đổi, vui lòng sử dụng trình duyệt của bạn để truy cập trực tiếp `声纹接口地址`. Khi mã tương tự xuất hiện trên trình duyệt, điều đó có nghĩa là thành công.
```
{"tOTAl_voiceprints":0,"status":"healthy"}
```

Vui lòng giữ lại `声纹接口地址` đã sửa đổi, nó sẽ được sử dụng trong bước tiếp theo.

# 2. Làm cách nào để định cấu hình nhận dạng giọng nói khi triển khai toàn bộ mô-đun?

## Bước đầu tiên là cấu hình giao diện
Đầu tiên bạn cần bật chức năng nhận dạng giọng nói. Trong bảng điều khiển thông minh, nhấp vào `参数字典` ở trên cùng và trong menu thả xuống, nhấp vào trang `系统功能配置`. Kiểm tra `声纹识别` trên trang và nhấp vào `保存配置`. Bạn có thể thấy nút `声纹识别` trên thẻ của đại lý mới.

Nếu bạn đang triển khai tất cả các mô-đun, hãy sử dụng tài khoản quản trị viên để đăng nhập vào bảng điều khiển thông minh, nhấp vào `参数字典` ở trên cùng và chọn chức năng `参数管理`.

Sau đó tìm kiếm tham số `server.voice_print`. Tại thời điểm này, giá trị của nó phải là giá trị `null`.
Nhấp vào nút sửa đổi và dán `声纹接口地址` thu được ở bước trước vào `参数值`. Sau đó lưu lại.

Nếu có thể lưu thành công nghĩa là mọi thứ đang diễn ra tốt đẹp và bạn có thể đến đại lý để kiểm tra hiệu quả. Nếu không thành công, điều đó có nghĩa là bảng điều khiển thông minh không thể truy cập tính năng nhận dạng giọng nói. Rất có thể là do tường lửa mạng hoặc địa chỉ IP LAN chính xác chưa được điền.

## Bước 2 Thiết lập chế độ bộ nhớ tác nhân

Nhập cấu hình vai trò của đại lý của bạn, đặt bộ nhớ thành `本地短期记忆` và nhớ bật `上报文字+语音`.

## Bước 3 Trò chuyện với đại lý của bạn

Hãy bật nguồn thiết bị của bạn và trò chuyện với anh ấy bằng tốc độ và giọng nói bình thường.

## Bước 4: Đặt giọng nói

Trong bảng điều khiển thông minh, trên trang `智能体管理`, trong bảng điều khiển của tác nhân thông minh, có nút `声纹识别`, hãy nhấp vào nút đó. Có `新增按钮` ở phía dưới. Bạn có thể đăng ký giọng nói của những gì ai đó nói.
Trong hộp bật lên, bạn nên điền thuộc tính `描述`, có thể là nghề nghiệp, tính cách và sở thích của một người. Sẽ thuận tiện cho đại lý phân tích và hiểu người nói.

## Bước 3 Trò chuyện với đại lý của bạn

Hãy bật nguồn thiết bị của bạn và hỏi nó, bạn có biết tôi là ai không? Nếu anh ta có thể trả lời được thì có nghĩa là chức năng nhận dạng giọng nói vẫn bình thường.

# 3. Làm cách nào để định cấu hình nhận dạng giọng nói trong quá trình triển khai đơn giản nhất?

## Bước đầu tiên là cấu hình giao diện
Mở tệp `xiaozhi-server/data/.config.yaml` (tạo nếu không cần tạo) và thêm/sửa đổi các mục sau:

```
# 声纹识别配置
voiceprint:
  # 声纹接口地址
  url: 你的声纹接口地址
  # 说话人配置：speaker_id,名称,描述
  speakers:
    - "test1,张三,张三是一个程序员"
    - "test2,李四,李四是一个产品经理"
    - "test3,王五,王五是一个设计师"
```

Dán `声纹接口地址` thu được ở bước trước vào `url`. Sau đó lưu lại.

Tham số `speakers` được thêm vào theo yêu cầu. Bạn cần chú ý đến tham số `speaker_id` ở đây, tham số này sẽ được dùng để đăng ký voiceprint sau này.

## Bước 2 Đăng ký giọng nói
Nếu bạn đã kích hoạt dịch vụ giọng nói, bạn có thể xem tài liệu API bằng cách truy cập `http://localhost:8005/voiceprint/docs` trong trình duyệt cục bộ của mình. Ở đây chúng tôi chỉ giải thích cách sử dụng API đăng ký giọng nói.

Địa chỉ API để đăng ký giọng nói là `http://localhost:8005/voiceprint/register` và phương thức yêu cầu là POST.

Tiêu đề yêu cầu cần chứa xác thực Mã thông báo ghi tên và mã thông báo là phần sau `?key=` trong `声纹接口地址`. Ví dụ: nếu địa chỉ đăng ký giọng nói của tôi là `http://127.0.0.1:8005/voiceprint/health?key=abcd` thì mã thông báo của tôi là `abcd`.

Nội dung yêu cầu chứa ID loa (loa_id) và tệp âm thanh WAV (tệp). Ví dụ yêu cầu như sau:

```
curl -X POST \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "speaker_id=your_speaker_id_here" \
  -F "file=@/path/to/your/file" \
  http://localhost:8005/voiceprint/register
```

Ở đây `file` là tệp âm thanh của loa sẽ được đăng ký và `speaker_id` cần phải nhất quán với `speaker_id` của bước đầu tiên để định cấu hình giao diện. Ví dụ: nếu tôi cần đăng ký giọng nói của Zhang San và `speaker_id` của Zhang San được điền vào `.config.yaml` là `test1`, thì khi tôi đăng ký giọng nói của Zhang San, `speaker_id` được điền trong nội dung yêu cầu là `test1` và `file` được điền vào là tệp âm thanh bài phát biểu của Zhang San.

## Bước 3 Khởi động dịch vụ

Khởi động máy chủ Xiaozhi và dịch vụ giọng nói và bạn có thể sử dụng nó bình thường.