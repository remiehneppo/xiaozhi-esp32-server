# Phương pháp nâng cấp tự động triển khai mã nguồn mô-đun đầy đủ

Hướng dẫn này dành cho những người yêu thích triển khai mã nguồn toàn mô-đun, cách tự động kéo mã nguồn, tự động biên dịch và tự động bắt đầu vận hành cổng thông qua các lệnh tự động. Nâng cấp hệ thống để đạt hiệu quả tối đa.

Nền tảng thử nghiệm của dự án này, `https://2662r3426b.vicp.fun`, đã sử dụng phương pháp này kể từ khi bắt đầu và cho kết quả tốt.

Để biết hướng dẫn, vui lòng tham khảo video hướng dẫn do `毕乐labs`, một blogger tại Bilibili phát hành: ["Cập nhật tự động máy chủ Xiaozhi mã nguồn mở xiaozhi-server và phiên bản mới nhất của hướng dẫn cấu hình điểm truy cập MCP"](https://www.bilibili.com/video/BV15H37zHE7Q)

#Điều kiện bắt đầu
- Máy tính/server của bạn là hệ điều hành linux
- Bạn đã trải qua toàn bộ quá trình
- Bạn muốn cập nhật các tính năng mới nhất, nhưng bạn thấy việc triển khai thủ công luôn gặp chút rắc rối. Bạn đang mong chờ một phương pháp cập nhật tự động.

Điều kiện thứ hai phải được đáp ứng vì một số tệp liên quan đến hướng dẫn này, chẳng hạn như JDK, môi trường Node.js, môi trường Conda, v.v., yêu cầu bạn phải chạy qua toàn bộ quá trình. Nếu bạn chưa xem qua nó, khi tôi nói về một tập tin nào đó, bạn có thể không biết nó có nghĩa gì.

# Hiệu ứng hướng dẫn
- Giải quyết vấn đề không lấy được mã nguồn dự án mới nhất tại Trung Quốc
- Tự động pull code và biên dịch file front-end
- Tự động pull code và biên dịch file java, tự động kill port 8002, tự động start port 8002
- Tự động pull code python, tự động kill port 8000, tự động start port 8000

# Bước đầu tiên là chọn thư mục dự án của bạn

Ví dụ: tôi đã lên kế hoạch cho thư mục dự án của mình là một thư mục trống mới. Nếu không muốn mắc sai lầm, bạn cũng có thể làm như tôi.
```
/home/system/xiaozhi
```

# Bước thứ hai là sao chép dự án này
Tại thời điểm này, bạn cần thực thi câu đầu tiên và lấy mã nguồn. Lệnh này được áp dụng cho máy chủ và máy tính mạng trong nước và không cần phải vượt qua tường lửa.

```
cd /home/system/xiaozhi
git clone https://ghproxy.net/https://github.com/xinnan-tech/xiaozhi-esp32-server.git
```

Sau khi thực thi sẽ có thêm một thư mục `xiaozhi-esp32-server` trong thư mục dự án của bạn. Đây là mã nguồn của dự án.

# Bước thứ ba là sao chép các tập tin cơ bản

Nếu bạn đã trải qua toàn bộ quá trình trước đó, bạn sẽ quen với tệp mô hình funasr `xiaozhi-server/models/SenseVoiceSmall/model.pt` và tệp cấu hình riêng của bạn `xiaozhi-server/data/.config.yaml`.

Tại thời điểm này, bạn cần sao chép tệp `model.pt` vào thư mục mới. Bạn có thể làm điều này
```
#Tạo các thư mục cần thiết
mkdir -p /home/system/xiaozhi/xiaozhi-esp32-server/main/xiaozhi-server/data/

cp Đường dẫn đầy đủ .config.yaml ban đầu của bạn /home/system/xiaozhi/xiaozhi-esp32-server/main/xiaozhi-server/data/.config.yaml
cp Đường dẫn đầy đủ của model.pt ban đầu của bạn /home/system/xiaozhi/xiaozhi-esp32-server/main/xiaozhi-server/models/SenseVoiceSmall/model.pt
```

# Bước 4: Tạo 3 file biên dịch tự động

## 4.1 Tự động biên dịch module quản lý web
Trong thư mục `/home/system/xiaozhi/`, tạo một tệp có tên `update_8001.sh` với nội dung sau

```
cd /home/system/xiaozhi/xiaozhi-esp32-server
git fetch --all
git reset --hard
git pull origin main


cd /home/system/xiaozhi/xiaozhi-esp32-server/main/manager-web
npm install
npm run build
rm -rf /home/system/xiaozhi/manager-web
mv /home/system/xiaozhi/xiaozhi-esp32-server/main/manager-web/dist /home/system/xiaozhi/manager-web
```

Sau khi lưu, thực hiện lệnh ủy quyền
```
chmod 777 update_8001.sh
```
Sau khi thực hiện, hãy tiếp tục bên dưới

## 4.2 Tự động biên dịch và chạy module manager-api
Trong thư mục `/home/system/xiaozhi/`, tạo một tệp có tên `update_8002.sh` với nội dung sau

```
cd /home/system/xiaozhi/xiaozhi-esp32-server
git pull origin main


cd /home/system/xiaozhi/xiaozhi-esp32-server/main/manager-api
rm -rf target
mvn clean package -Dmaven.test.skip=true
cd /home/system/xiaozhi/

# Tìm ID tiến trình chiếm cổng 8002
PID=$(sudo netstat -tulnp | grep 8002 | awk '{print $7}' | cut -d'/' -f1)

rm -rf /home/system/xiaozhi/xiaozhi-esp32-api.jar
mv /home/system/xiaozhi/xiaozhi-esp32-server/main/manager-api/target/xiaozhi-esp32-api.jar /home/system/xiaozhi/xiaozhi-esp32-api.jar

# Kiểm tra xem có tìm thấy số tiến trình không
nếu [ -z "$PID" ]; sau đó
  echo "Không tìm thấy quá trình chiếm cổng 8002"
khác
  echo "Tìm tiến trình chiếm cổng 8002, số tiến trình là: $PID"
  # Giết tiến trình
  giết -9 $PID
  giết -9 $PID
  echo "Tiến trình bị hủy $PID"
fi

nohup java -jar xiaozhi-esp32-api.jar --spring.profiles.active=dev &

tail tail -f nohup.out
```

Sau khi lưu, thực hiện lệnh ủy quyền
```
chmod 777 update_8002.sh
```
Sau khi thực hiện, hãy tiếp tục bên dưới

## 4.3 Tự động biên dịch và chạy các dự án Python
Trong thư mục `/home/system/xiaozhi/`, tạo một tệp có tên `update_8000.sh` với nội dung sau

```
cd /home/system/xiaozhi/xiaozhi-esp32-server
git pull origin main

# Tìm ID tiến trình chiếm cổng 8000
PID=$(sudo netstat -tulnp | grep 8000 | awk '{print $7}' | cut -d'/' -f1)

# Kiểm tra xem có tìm thấy số tiến trình không
nếu [ -z "$PID" ]; sau đó
  echo "Không tìm thấy tiến trình nào chiếm cổng 8000"
khác
  echo "Tìm tiến trình chiếm cổng 8000, số tiến trình là: $PID"
  # Giết tiến trình
  giết -9 $PID
  giết -9 $PID
  echo "Tiến trình bị hủy $PID"
fi
cd chính/máy chủ xiaozhi
#Khởi tạo môi trường conda
nguồn ~/.bashrc
conda kích hoạt xiaozhi-esp32-server
cài đặt pip -r require.txt
nohup python app.py >/dev/null &
tail -f /home/system/xiaozhi/xiaozhi-esp32-server/main/xiaozhi-server/tmp/server.log
```

Sau khi lưu, thực hiện lệnh ủy quyền
```
chmod 777 update_8000.sh
```
Sau khi thực hiện, hãy tiếp tục bên dưới

# Cập nhật hàng ngày

Sau khi tạo xong các script trên, để cập nhật hàng ngày, chúng ta chỉ cần thực hiện các lệnh sau để tự động cập nhật và bắt đầu

```
cd /home/system/xiaozhi
# Cập nhật và khởi động chương trình Java
./update_8001.sh
# Cập nhật chương trình web
./update_8002.sh
# Cập nhật và khởi động chương trình python
./update_8000.sh


# Nếu bạn muốn xem nhật ký java sau, hãy thực hiện lệnh sau
đuôi -f Nohup.out
# Nếu bạn muốn xem nhật ký python sau, hãy thực hiện lệnh sau
tail -f /home/system/xiaozhi/xiaozhi-esp32-server/main/xiaozhi-server/tmp/server.log
```

# Ghi chú
Nền tảng thử nghiệm `https://2662r3426b.vicp.fun` sử dụng nginx làm proxy ngược. Cấu hình chi tiết của nginx.conf có thể tìm thấy [tham khảo tại đây](https://github.com/xinnan-tech/xiaozhi-esp32-server/issues/791)

## Câu hỏi thường gặp

### 1. Tại sao bạn không thấy cổng 8001?
Trả lời: 8001 là cổng được môi trường phát triển sử dụng để chạy giao diện người dùng. Nếu bạn đang triển khai trên máy chủ, không nên sử dụng `npm run serve` để khởi động cổng 8001 để chạy giao diện người dùng. Thay vào đó, hãy biên dịch nó thành tệp html như hướng dẫn này, sau đó sử dụng nginx để quản lý quyền truy cập.

### 2. Tôi có cần cập nhật các câu lệnh SQL thủ công cho mỗi lần cập nhật không?
Trả lời: Không, vì dự án sử dụng **Liquibase** để quản lý phiên bản cơ sở dữ liệu và sẽ tự động thực thi các tập lệnh sql mới.