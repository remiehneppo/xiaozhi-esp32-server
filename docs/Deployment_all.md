#Sơ đồ kiến trúc triển khai
![Vui lòng tham khảo sơ đồ kiến trúc cài đặt mô-đun đầy đủ](../docs/images/deploy2.png)
# Cách 1: Docker chạy full module
Bắt đầu từ phiên bản `0.8.2`, images docker do dự án này phát hành chỉ hỗ trợ `x86架构`. Nếu bạn cần triển khai nó trên CPU của `arm64架构`, bạn có thể làm theo [hướng dẫn này](docker-build.md) để biên dịch `arm64的镜像` cục bộ.

## 1. Cài đặt docker

Nếu docker chưa được cài đặt trên máy tính của bạn, bạn có thể làm theo hướng dẫn tại đây để cài đặt nó: [docker Installation](https://www.runoob.com/docker/ubuntu-docker-install.html)

Có hai cách để cài đặt các mô-đun đầy đủ trong docker. Bạn có thể [sử dụng tập lệnh lười](./Deployment_all.md#11-懒人脚本) (tác giả [@VanillaNahida](https://github.com/VanillaNahida))
Tập lệnh sẽ tự động tải xuống các tệp cần thiết và tệp cấu hình cho bạn. Bạn cũng có thể sử dụng [Triển khai thủ công](./Deployment_all.md#12-手动部署) để xây dựng nó từ đầu.



### 1.1 Kịch bản lười biếng
Triển khai rất dễ dàng, bạn có thể tham khảo [Video Hướng dẫn](https://www.bilibili.com/video/BV17bbvzHExd/), phiên bản văn bản của hướng dẫn như sau:
> [!LƯU Ý]
> Hiện tại, nó chỉ hỗ trợ triển khai máy chủ Ubuntu bằng một cú nhấp chuột. Chúng tôi chưa thử nó trên các hệ thống khác và có thể có một số lỗi lạ.

Sử dụng công cụ SSH để kết nối với máy chủ và thực thi đoạn script sau với quyền root
```bash
sudo bash -c "$(wget -qO- https://ghfast.top/https://raw.githubusercontent.com/xinnan-tech/xiaozhi-esp32-server/main/docker-setup.sh)"
```

Tập lệnh tự động hoàn thành các thao tác sau:
> 1. Cài đặt Docker
> 2. Cấu hình nguồn nhân bản
> 3. Tải xuống/Kéo images
> 4. Tải xuống tệp mô hình nhận dạng giọng nói
> 5. Khởi động và cấu hình máy chủ
>

Sau khi hoàn thành cấu hình đơn giản, hãy tham khảo ba điều quan trọng nhất được đề cập trong [4. Chạy chương trình](#4. 运行程序) và [5. Khởi động lại xiaozhi-esp32-server](#5.重启xiaozhi-esp32-server). Bạn có thể sử dụng nó sau khi hoàn thành ba cấu hình.

### 1.2 Triển khai thủ công

#### 1.2.1 Tạo thư mục

Sau khi cài đặt, bạn cần tìm thư mục chứa file cấu hình cho dự án này. Ví dụ: chúng ta có thể tạo một thư mục mới có tên `xiaozhi-server`.

Sau khi tạo thư mục, bạn cần tạo thư mục `data` và thư mục `models` trong `xiaozhi-server` và thư mục `SenseVoiceSmall` trong `models`.

Cấu trúc thư mục cuối cùng trông như thế này:

```
xiaozhi-server
  ├─ data
  ├─ models
     ├─ SenseVoiceSmall
```

#### 1.2.2 Tải file mô hình nhận dạng giọng nói

Mô hình nhận dạng giọng nói của dự án này sử dụng mô hình `SenseVoiceSmall` theo mặc định để chuyển đổi giọng nói thành văn bản. Vì mô hình lớn nên cần phải tải xuống độc lập. Sau khi tải xuống, hãy đặt `model.pt`
Tệp được đặt trong `models/SenseVoiceSmall`
thư mục. Chọn một trong hai con đường tải xuống bên dưới.

- Dòng 1: Tải xuống Ali Modu [SenseVoiceSmall](https://modelscope.cn/models/iic/SenseVoiceSmall/resolve/master/model.pt)
- Dòng 2: Mã trích xuất [SenseVoiceSmall](https://pan.baidu.com/share/init?surl=QlgM58FHhYv1tFnUT_A8Sg&pwd=qvna) của đĩa mạng Baidu:
  `qvna`


#### 1.2.3 Tải file cấu hình

Bạn cần tải xuống hai tệp cấu hình: `docker-compose_all.yaml` và `config_from_api.yaml`. Hai tệp này cần được tải xuống từ kho dự án.

##### 1.2.3.1 Tải xuống docker-compose_all.yaml

Mở [liên kết này](../main/xiaozhi-server/docker-compose_all.yml) bằng trình duyệt của bạn.

Tìm nút có tên `RAW` ở bên phải trang. Bên cạnh nút `RAW`, hãy tìm biểu tượng tải xuống. Nhấp vào nút tải xuống để tải xuống tệp `docker-compose_all.yml`. Tải tập tin về của bạn
`xiaozhi-server`.

Hoặc thực hiện tải xuống `wget https://raw.githubusercontent.com/xinnan-tech/xiaozhi-esp32-server/refs/heads/main/main/xiaozhi-server/docker-compose_all.yml` trực tiếp.

Sau khi tải xuống, hãy quay lại hướng dẫn này và tiếp tục.

##### 1.2.3.2 Tải config_from_api.yaml

Mở [liên kết này](../main/xiaozhi-server/config_from_api.yaml) bằng trình duyệt của bạn.

Tìm nút có tên `RAW` ở bên phải trang. Bên cạnh nút `RAW`, hãy tìm biểu tượng tải xuống. Nhấp vào nút tải xuống để tải xuống tệp `config_from_api.yaml`. Tải tập tin về của bạn
`xiaozhi-server` trong thư mục `data` rồi đổi tên tệp `config_from_api.yaml` thành `.config.yaml`.

Hoặc trực tiếp thực thi `wget https://raw.githubusercontent.com/xinnan-tech/xiaozhi-esp32-server/refs/heads/main/main/xiaozhi-server/config_from_api.yaml` để tải xuống và lưu.

Sau khi tải xuống tệp cấu hình, chúng tôi xác nhận rằng các tệp trong toàn bộ `xiaozhi-server` như sau:

```
xiaozhi-server
  ├─ docker-compose_all.yml
  ├─ data
    ├─ .config.yaml
  ├─ models
     ├─ SenseVoiceSmall
       ├─ model.pt
```

Nếu cấu trúc thư mục tệp của bạn cũng như trên, hãy tiếp tục bên dưới. Nếu không, hãy xem xét kỹ hơn xem bạn có bỏ sót điều gì không.

## 2. Sao lưu dữ liệu

Nếu trước đây bạn đã chạy thành công bảng điều khiển thông minh và nếu thông tin chính của bạn được lưu trên đó, trước tiên hãy sao chép dữ liệu quan trọng từ bảng điều khiển thông minh. Vì trong quá trình nâng cấp, dữ liệu gốc có thể bị ghi đè.

## 3. Xóa phiên bản lịch sử của images và vùng chứa
Tiếp theo, mở công cụ dòng lệnh, sử dụng công cụ `终端` hoặc `命令行` để nhập `xiaozhi-server` của bạn và thực hiện lệnh sau

```
docker compose -f docker-compose_all.yml down

docker stop xiaozhi-esp32-server
docker rm xiaozhi-esp32-server

docker stop xiaozhi-esp32-server-web
docker rm xiaozhi-esp32-server-web

docker stop xiaozhi-esp32-server-db
docker rm xiaozhi-esp32-server-db

docker stop xiaozhi-esp32-server-redis
docker rm xiaozhi-esp32-server-redis

docker rmi ghcr.nju.edu.cn/xinnan-tech/xiaozhi-esp32-server:server_latest
docker rmi ghcr.nju.edu.cn/xinnan-tech/xiaozhi-esp32-server:web_latest
```

## 4. Chạy chương trình
Thực hiện lệnh sau để khởi động vùng chứa phiên bản mới

```
docker compose -f docker-compose_all.yml up -d
```

Sau khi thực hiện, thực hiện lại lệnh sau để xem thông tin nhật ký.

```
docker logs -f xiaozhi-esp32-server-web
```

Khi bạn nhìn thấy nhật ký đầu ra, điều đó có nghĩa là `智控台` của bạn đã khởi động thành công.

```
2025-xx-xx 22:11:12.445 [main] INFO  c.a.d.s.b.a.DruidDataSourceAutoConfigure - Init DruidDataSource
2025-xx-xx 21:28:53.873 [main] INFO  xiaozhi.AdminApplication - Started AdminApplication in 16.057 seconds (process running for 17.941)
http://localhost:8002/xiaozhi/doc.html
```

Xin lưu ý rằng chỉ `智控台` mới có thể chạy vào lúc này. Nếu có lỗi được báo cáo trên cổng 8000 `xiaozhi-esp32-server`, hãy bỏ qua lỗi đó ngay bây giờ.

Lúc này, bạn cần sử dụng trình duyệt, mở `智控台`, liên kết: http://127.0.0.1:8002 và đăng ký người dùng đầu tiên. Người dùng đầu tiên là quản trị viên cấp cao và những người dùng tiếp theo là người dùng thông thường. Người dùng thông thường chỉ có thể liên kết các thiết bị và cấu hình các tác nhân; quản trị viên cấp cao có thể thực hiện quản lý mô hình, quản lý người dùng, cấu hình tham số và các chức năng khác.

Có ba điều quan trọng cần làm tiếp theo:

###Điều quan trọng đầu tiên

Sử dụng tài khoản quản trị viên cấp cao để đăng nhập vào bảng điều khiển thông minh, tìm `参数管理` ở menu trên cùng, tìm dữ liệu đầu tiên trong danh sách, mã tham số là `server.secret` và sao chép vào `参数值`.

`server.secret` cần được giải thích. `参数值` này rất quan trọng. Chức năng của nó là kết nối thiết bị đầu cuối `Server` của chúng tôi với `manager-api`. `server.secret` là khóa được tạo tự động và ngẫu nhiên mỗi khi mô-đun trình quản lý được triển khai từ đầu.

Sau khi sao chép `参数值`, hãy mở tệp `.config.yaml` trong thư mục `data` trong `xiaozhi-server`. Tại thời điểm này, tệp cấu hình của bạn sẽ trông như thế này:

```
manager-api:
  url:  http://127.0.0.1:8002/xiaozhi
  secret: 你的server.secret值
```
1. Sao chép `参数值` của `server.secret` mà bạn vừa sao chép từ `智控台` sang `secret` trong tệp `.config.yaml`.

2. Vì bạn đang triển khai bằng docker, hãy thay đổi `url` thành `http://xiaozhi-esp32-server-web:8002/xiaozhi` sau

3. Vì bạn đang triển khai bằng docker, hãy thay đổi `url` thành `http://xiaozhi-esp32-server-web:8002/xiaozhi` sau

4. Vì bạn đang triển khai bằng docker, hãy thay đổi `url` thành `http://xiaozhi-esp32-server-web:8002/xiaozhi` sau

Hiệu ứng tương tự
```
manager-api:
  url: http://xiaozhi-esp32-server-web:8002/xiaozhi
  secret: 12345678-xxxx-xxxx-xxxx-123456789000
```

Sau khi lưu lại tiếp tục làm việc quan trọng thứ hai

### Điều quan trọng thứ hai

Sử dụng tài khoản quản trị viên cấp cao để đăng nhập vào bảng điều khiển thông minh, tìm `模型配置` trên menu trên cùng, sau đó nhấp vào `大语言模型` ở cột bên trái, tìm phần dữ liệu đầu tiên `智谱AI` và nhấp vào nút `修改`.
Sau khi hộp sửa đổi bật lên, hãy điền khóa `智谱AI` mà bạn đã đăng ký vào `API密钥`. Sau đó nhấp vào Lưu.

## 5. Khởi động lại xiaozhi-esp32-server

Tiếp theo mở công cụ dòng lệnh và sử dụng công cụ `终端` hoặc `命令行` để nhập
```
docker restart xiaozhi-esp32-server
docker logs -f xiaozhi-esp32-server
```
Nếu bạn có thể thấy nhật ký tương tự như sau thì đó là dấu hiệu cho thấy máy chủ đã khởi động thành công.

```
25-02-23 12:01:09[core.WebSocket_server] - INFO - WebSocket地址是      ws://xxx.xx.xx.xx:8000/xiaozhi/v1/
25-02-23 12:01:09[core.WebSocket_server] - INFO - =======上面的地址是WebSocket协议地址，请勿用浏览器访问=======
25-02-23 12:01:09[core.WebSocket_server] - INFO - 如想测试WebSocket请启动digital-human模块，打开浏览器交互测试
25-02-23 12:01:09[core.WebSocket_server] - INFO - =======================================================
```

Vì bạn đang triển khai một mô-đun đầy đủ nên bạn có hai giao diện quan trọng cần được ghi vào ESP32.

Giao diện OTA:
```
http://你宿主机局域网的ip:8002/xiaozhi/OTA/
```

Giao diện WebSocket:
```
ws://你宿主机的ip:8000/xiaozhi/v1/
```

### Điều quan trọng thứ ba

Sử dụng tài khoản quản trị viên cấp cao để đăng nhập vào bảng điều khiển thông minh, tìm `参数管理` ở menu trên cùng, tìm mã thông số là `server.WebSocket` và nhập `WebSocket接口` của bạn.

Sử dụng tài khoản quản trị viên cấp cao để đăng nhập vào bảng điều khiển thông minh, tìm `参数管理` ở menu trên cùng, tìm mã số là `server.OTA` và nhập `OTA接口` của bạn.

Tiếp theo, bạn có thể bắt đầu vận hành thiết bị ESP32 của mình. Bạn có thể `自行编译esp32固件` hoặc định cấu hình nó để sử dụng `虾哥编译好的1.6.1以上版本的固件`. Chọn một trong hai

1. [Biên dịch phần mềm ESP32 của riêng bạn](firmware-build.md).

2. [Định cấu hình máy chủ tùy chỉnh dựa trên chương trình cơ sở do  biên soạn](firmware-setting.md).


# Cách 2: Chạy toàn bộ module từ mã nguồn cục bộ

## 1. Cài đặt cơ sở dữ liệu MySQL

Nếu MySQL đã được cài đặt trên máy này, bạn có thể trực tiếp tạo cơ sở dữ liệu có tên `xiaozhi_esp32_server` trong cơ sở dữ liệu.

```sql
CREATE DATABASE xiaozhi_esp32_server CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Nếu bạn chưa có MySQL thì có thể cài đặt mysql thông qua docker

```
docker run --name xiaozhi-esp32-server-db -e MYSQL_ROOT_PASSWORD=123456 -p 3306:3306 -e MYSQL_DATABASE=xiaozhi_esp32_server -e MYSQL_INITDB_ARGS="--character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci" -e TZ=Asia/Shanghai -d mysql:latest
```

## 2. Cài đặt redis

Nếu bạn chưa có Redis thì có thể cài đặt redis thông qua docker

```
docker run --name xiaozhi-esp32-server-redis -d -p 6379:6379 redis
```

## 3. Chạy chương trình manager-api

3.1 Cài đặt JDK21 và đặt các biến môi trường JDK

3.2 Cài đặt Maven và thiết lập các biến môi trường Maven

3.3 Sử dụng công cụ lập trình Vscode để cài đặt các plug-in liên quan đến môi trường Java

3.4 Sử dụng công cụ lập trình Vscode để nạp module manager-api

Định cấu hình thông tin kết nối cơ sở dữ liệu trong `src/main/resources/application-dev.yml`

```
spring:
  datasource:
    username: root
    password: 123456
```
Định cấu hình thông tin kết nối Redis trong `src/main/resources/application-dev.yml`
```
spring:
    data:
      redis:
        host: localhost
        port: 6379
        password:
        database: 0
```

3.5 Chạy chương trình chính

Dự án này là một dự án SpringBoot và phương thức khởi động là:
Mở `Application.java` và chạy phương thức `Main` để bắt đầu

```
路径地址：
src/main/java/xiaozhi/AdminApplication.java
```

Khi bạn nhìn thấy nhật ký đầu ra, điều đó có nghĩa là `manager-api` của bạn đã khởi động thành công.

```
2025-xx-xx 22:11:12.445 [main] INFO  c.a.d.s.b.a.DruidDataSourceAutoConfigure - Init DruidDataSource
2025-xx-xx 21:28:53.873 [main] INFO  xiaozhi.AdminApplication - Started AdminApplication in 16.057 seconds (process running for 17.941)
http://localhost:8002/xiaozhi/doc.html
```

## 4. Chạy chương trình quản lý web

4.1 Cài đặt nodejs

4.2 Sử dụng công cụ lập trình Vscode để nạp module quản lý web

Lệnh terminal vào thư mục web quản lý

```
npm install
```
sau đó bắt đầu
```
npm run serve
```

Xin lưu ý rằng nếu giao diện của manager-api của bạn không có trong `http://localhost:8002`, vui lòng sửa đổi nó trong quá trình phát triển.
Đường dẫn trong `main/manager-web/.env.development`

Sau khi chạy thành công, bạn cần sử dụng trình duyệt, mở `智控台`, liên kết: http://127.0.0.1:8001 và đăng ký người dùng đầu tiên. Người dùng đầu tiên là quản trị viên cấp cao và những người dùng tiếp theo là người dùng thông thường. Người dùng thông thường chỉ có thể liên kết các thiết bị và cấu hình các tác nhân; quản trị viên cấp cao có thể thực hiện quản lý mô hình, quản lý người dùng, cấu hình tham số và các chức năng khác.


Quan trọng: Sau khi đăng ký thành công, hãy sử dụng tài khoản quản trị viên cấp cao để đăng nhập vào bảng điều khiển thông minh, tìm `模型配置` ở menu trên cùng, sau đó nhấp vào `大语言模型` ở cột bên trái, tìm phần dữ liệu đầu tiên `智谱AI` và nhấp vào nút `修改`.
Sau khi hộp sửa đổi bật lên, hãy điền khóa `智谱AI` mà bạn đã đăng ký vào `API密钥`. Sau đó nhấp vào Lưu.

Quan trọng: Sau khi đăng ký thành công, hãy sử dụng tài khoản quản trị viên cấp cao để đăng nhập vào bảng điều khiển thông minh, tìm `模型配置` ở menu trên cùng, sau đó nhấp vào `大语言模型` ở cột bên trái, tìm phần dữ liệu đầu tiên `智谱AI` và nhấp vào nút `修改`.
Sau khi hộp sửa đổi bật lên, hãy điền khóa `智谱AI` mà bạn đã đăng ký vào `API密钥`. Sau đó nhấp vào Lưu.

Quan trọng: Sau khi đăng ký thành công, hãy sử dụng tài khoản quản trị viên cấp cao để đăng nhập vào bảng điều khiển thông minh, tìm `模型配置` ở menu trên cùng, sau đó nhấp vào `大语言模型` ở cột bên trái, tìm phần dữ liệu đầu tiên `智谱AI` và nhấp vào nút `修改`.
Sau khi hộp sửa đổi bật lên, hãy điền khóa `智谱AI` mà bạn đã đăng ký vào `API密钥`. Sau đó nhấp vào Lưu.

## 5. Cài đặt môi trường Python

Dự án này sử dụng `conda` để quản lý các môi trường phụ thuộc. Nếu cài đặt `conda` không thuận tiện, bạn cần cài đặt `libopus` và `ffmpeg` theo hệ điều hành thực tế.
Nếu bạn chắc chắn sử dụng `conda`, sau khi cài đặt, hãy bắt đầu thực hiện lệnh sau.

Mẹo quan trọng! Người dùng Windows có thể quản lý môi trường bằng cách cài đặt `Anaconda`. Sau khi cài đặt `Anaconda`, hãy tìm kiếm các từ khóa liên quan đến `anaconda` trong `开始`.
Tìm `Anaconda Prpmpt` và chạy nó với tư cách quản trị viên. Như hình dưới đây.

![conda_prompt](./images/conda_env_1.png)

Sau khi chạy, nếu nhìn thấy chữ (base) trước cửa sổ dòng lệnh nghĩa là bạn đã vào thành công môi trường `conda`. Sau đó, bạn có thể thực hiện lệnh sau.

![conda_env](./images/conda_env_2.png)

```
conda remove -n xiaozhi-esp32-server --all -y
conda create -n xiaozhi-esp32-server python=3.10 -y
conda activate xiaozhi-esp32-server

# Thêm kênh nguồn Thanh Hoa
cấu hình conda --add kênh https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
cấu hình conda --add kênh https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free
cấu hình conda --add kênh https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge

conda install libopus -y
conda install ffmpeg -y

# Khi triển khai trong môi trường Linux, nếu xảy ra lỗi tương tự như thư viện động libiconv.so.2 bị thiếu, vui lòng cài đặt nó thông qua lệnh sau.
conda cài đặt libiconv -y
```

Xin lưu ý rằng lệnh trên sẽ không thành công nếu bạn thực hiện tất cả cùng một lúc. Bạn cần phải thực hiện nó từng bước một. Sau khi thực hiện từng bước, hãy kiểm tra nhật ký đầu ra để xem nó có thành công hay không.

## 6. Cài đặt các phụ thuộc của dự án này

Trước tiên bạn phải tải xuống mã nguồn của dự án này. Mã nguồn có thể được tải xuống thông qua lệnh `git clone`. Nếu bạn chưa quen với lệnh `git clone`.

Bạn có thể mở địa chỉ này bằng trình duyệt `https://github.com/xinnan-tech/xiaozhi-esp32-server.git`

Sau khi mở nó, hãy tìm một nút màu xanh lục trên trang có nội dung `Code`, nhấp vào nút đó và sau đó bạn sẽ thấy nút `Download ZIP`.

Nhấp vào nó để tải xuống gói nén mã nguồn của dự án này. Sau khi tải về máy tính, hãy giải nén nó. Lúc này tên của nó có thể là `xiaozhi-esp32-server-main`
Bạn cần đổi tên nó thành `xiaozhi-esp32-server`. Trong tệp này, hãy chuyển đến thư mục `main` rồi chuyển đến `xiaozhi-server`. Hãy nhớ thư mục này `xiaozhi-server`.

```
# 继续使用conda环境
conda activate xiaozhi-esp32-server
# 进入到你的项目根目录，再进入main/xiaozhi-server
cd main/xiaozhi-server
pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
pip install -r requirements.txt
```

### 7. Tải file mô hình nhận dạng giọng nói

Mô hình nhận dạng giọng nói của dự án này sử dụng mô hình `SenseVoiceSmall` theo mặc định để chuyển đổi giọng nói thành văn bản. Vì mô hình lớn nên cần phải tải xuống độc lập. Sau khi tải xuống, hãy đặt `model.pt`
Tệp được đặt trong `models/SenseVoiceSmall`
thư mục. Chọn một trong hai con đường tải xuống bên dưới.

- Dòng 1: Tải xuống Ali Modu [SenseVoiceSmall](https://modelscope.cn/models/iic/SenseVoiceSmall/resolve/master/model.pt)
- Dòng 2: Mã trích xuất [SenseVoiceSmall](https://pan.baidu.com/share/init?surl=QlgM58FHhYv1tFnUT_A8Sg&pwd=qvna) của đĩa mạng Baidu:
  `qvna`

## 8.Cấu hình file dự án

Sử dụng tài khoản quản trị viên cấp cao để đăng nhập vào bảng điều khiển thông minh, tìm `参数管理` ở menu trên cùng, tìm dữ liệu đầu tiên trong danh sách, mã tham số là `server.secret` và sao chép vào `参数值`.

`server.secret` cần được giải thích. `参数值` này rất quan trọng. Chức năng của nó là kết nối thiết bị đầu cuối `Server` của chúng tôi với `manager-api`. `server.secret` là khóa được tạo tự động và ngẫu nhiên mỗi khi mô-đun trình quản lý được triển khai từ đầu.

Nếu thư mục `xiaozhi-server` của bạn không có `data`, bạn cần tạo thư mục `data`.
Nếu không có tệp `.config.yaml` trong `data` của bạn, bạn có thể sao chép tệp `config_from_api.yaml` trong thư mục `xiaozhi-server` sang `data` và đổi tên thành `.config.yaml`

Sau khi sao chép `参数值`, hãy mở tệp `.config.yaml` trong thư mục `data` trong `xiaozhi-server`. Tại thời điểm này, tệp cấu hình của bạn sẽ trông như thế này:

```
manager-api:
  url: http://127.0.0.1:8002/xiaozhi
  secret: 你的server.secret值
```

Sao chép `参数值` của `server.secret` mà bạn vừa sao chép từ `智控台` sang `secret` trong tệp `.config.yaml`.

Hiệu ứng tương tự
```
manager-api:
  url: http://127.0.0.1:8002/xiaozhi
  secret: 12345678-xxxx-xxxx-xxxx-123456789000
```

## 9. Chạy dự án

```
# 确保在xiaozhi-server目录下执行
conda activate xiaozhi-esp32-server
python app.py
```

Nếu bạn thấy nhật ký tương tự như sau thì đó là dấu hiệu cho thấy dịch vụ dự án đã được khởi động thành công.

```
25-02-23 12:01:09[core.WebSocket_server] - INFO - Server is running at ws://xxx.xx.xx.xx:8000/xiaozhi/v1/
25-02-23 12:01:09[core.WebSocket_server] - INFO - =======上面的地址是WebSocket协议地址，请勿用浏览器访问=======
25-02-23 12:01:09[core.WebSocket_server] - INFO - 如想测试WebSocket请启动digital-human模块，打开浏览器交互测试
25-02-23 12:01:09[core.WebSocket_server] - INFO - =======================================================
```

Vì bạn đang triển khai một mô-đun đầy đủ nên bạn có hai giao diện quan trọng.

Giao diện OTA:
```
http://你电脑局域网的ip:8002/xiaozhi/OTA/
```

Giao diện WebSocket:
```
ws://你电脑局域网的ip:8000/xiaozhi/v1/
```

Hãy nhớ ghi hai địa chỉ giao diện trên vào bảng điều khiển thông minh: chúng sẽ ảnh hưởng đến chức năng cấp địa chỉ WebSocket và nâng cấp tự động.

1. Sử dụng tài khoản quản trị viên cấp cao để đăng nhập vào bảng điều khiển thông minh, tìm `参数管理` ở menu trên cùng, tìm mã thông số là `server.WebSocket` và nhập `WebSocket接口` của bạn.

2. Sử dụng tài khoản quản trị viên cấp cao để đăng nhập vào bảng điều khiển thông minh, tìm `参数管理` ở menu trên cùng, tìm mã số là `server.OTA` và nhập `OTA接口` của bạn.


Tiếp theo, bạn có thể bắt đầu vận hành thiết bị ESP32 của mình. Bạn có thể `自行编译esp32固件` hoặc định cấu hình nó để sử dụng `虾哥编译好的1.6.1以上版本的固件`. Chọn một trong hai

1. [Biên dịch phần mềm ESP32 của riêng bạn](firmware-build.md).

2. [Định cấu hình máy chủ tùy chỉnh dựa trên chương trình cơ sở do  biên soạn](firmware-setting.md).

# Câu hỏi thường gặp
Dưới đây là một số câu hỏi thường gặp để tham khảo:

1. [Tại sao Xiaozhi nhận ra nhiều tiếng Hàn, tiếng Nhật và tiếng Anh khi tôi nói](./FAQ.md)<br/>
2. [Tại sao xuất hiện thông báo "Tệp lỗi tác vụ TTS không tồn tại"? ](./FAQ.md)<br/>
3. [TTS thường xuyên bị lỗi và hết thời gian chờ](./FAQ.md)<br/>
4. [Có thể kết nối với máy chủ tự build bằng Wifi, nhưng không thể kết nối ở chế độ 4G](./FAQ.md)<br/>
5. [Làm cách nào để cải thiện tốc độ phản hồi đối thoại của Xiaozhi? ](./FAQ.md)<br/>
6. [Tôi nói rất chậm và Xiaozhi luôn nắm bắt được cuộc trò chuyện khi tôi tạm dừng](./FAQ.md)<br/>
## Hướng dẫn liên quan đến triển khai
1. [Cách tự động lấy mã mới nhất của dự án này và tự động biên dịch và khởi động nó](./dev-ops-integration.md)<br/>
2. [Cách triển khai cổng MQTT để kích hoạt giao thức MQTT+UDP](./mqtt-gateway-integration.md)<br/>
3. [Cách tích hợp với Nginx](https://github.com/xinnan-tech/xiaozhi-esp32-server/issues/791)<br/>
## Mở rộng các hướng dẫn liên quan
1. [Cách bật bảng điều khiển thông minh đăng ký số điện thoại di động](./ali-sms-integration.md)<br/>
2. [Cách tích hợp HomeAssistant để điều khiển nhà thông minh](./homeassistant-integration.md)<br/>
3. [Cách bật mô hình trực quan để nhận dạng vật thể bằng cách chụp ảnh](./mcp-vision-integration.md)<br/>
4. [Cách triển khai điểm truy cập MCP](./mcp-endpoint-enable.md)<br/>
5. [Cách truy cập điểm truy cập MCP](./mcp-endpoint-integration.md)<br/>
6. [Cách bật nhận dạng giọng nói](./voiceprint-integration.md)<br/>
7. [Hướng dẫn cấu hình nguồn plug-in tin tức](./newsnow_plugin_config.md)<br/>
8. [Hướng dẫn sử dụng plug-in thời tiết](./weather-integration.md)<br/>
## Hướng dẫn liên quan đến nhân bản giọng nói và triển khai giọng nói cục bộ
1. [Cách sao chép âm thanh trên bảng điều khiển thông minh](./huoshan-streamTTS-voice-cloning.md)<br/>
2. [Cách triển khai chỉ mục tích hợp-tts giọng nói cục bộ](./index-stream-integration.md)<br/>
3. [Cách triển khai giọng nói địa phương tích hợp giọng nói cá](./fish-speech-integration.md)<br/>
4. [Cách triển khai và tích hợp giọng nói cục bộ PaddleSpeech](./paddlespeech-deploy.md)<br/>
## Hướng dẫn kiểm tra hiệu năng
1. [Hướng dẫn kiểm tra tốc độ của từng thành phần](./performance_tester.md)<br/>
2. [Kết quả kiểm tra công khai định kỳ](https://github.com/xinnan-tech/xiaozhi-performance-research)<br/>