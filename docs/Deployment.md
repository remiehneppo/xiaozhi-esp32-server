#Sơ đồ kiến trúc triển khai
![Vui lòng tham khảo sơ đồ kiến trúc đơn giản hóa](../docs/images/deploy1.png)
# Cách 1: Docker chỉ chạy Server

Bắt đầu từ phiên bản `0.8.2`, images docker do dự án này phát hành chỉ hỗ trợ `x86架构`. Nếu bạn cần triển khai nó trên CPU của `arm64架构`, bạn có thể làm theo [hướng dẫn này](docker-build.md) để biên dịch `arm64的镜像` cục bộ.

## 1. Cài đặt docker

Nếu docker chưa được cài đặt trên máy tính của bạn, bạn có thể làm theo hướng dẫn tại đây để cài đặt nó: [docker Installation](https://www.runoob.com/docker/ubuntu-docker-install.html)

Sau khi cài đặt docker, hãy tiếp tục.

### 1.1 Triển khai thủ công

#### 1.1.1 Tạo thư mục

Sau khi cài đặt docker, bạn cần tìm thư mục chứa file cấu hình cho dự án này. Ví dụ: chúng ta có thể tạo một thư mục mới có tên `xiaozhi-server`.

Sau khi tạo thư mục, bạn cần tạo thư mục `data` và thư mục `models` trong `xiaozhi-server` và thư mục `SenseVoiceSmall` trong `models`.

Cấu trúc thư mục cuối cùng trông như thế này:

```
xiaozhi-server
  ├─ data
  ├─ models
     ├─ SenseVoiceSmall
```

#### 1.1.2 Tải file mô hình nhận dạng giọng nói

Bạn cần tải xuống tệp mô hình nhận dạng giọng nói vì tính năng nhận dạng giọng nói mặc định của dự án này sử dụng giải pháp nhận dạng giọng nói ngoại tuyến cục bộ. Bạn có thể tải nó theo cách này
[Chuyển để tải xuống tệp mô hình nhận dạng giọng nói](#模型文件)

Sau khi tải xuống, hãy quay lại hướng dẫn này.

#### 1.1.3 Tải file cấu hình

Bạn cần tải xuống hai tệp cấu hình: `docker-compose.yaml` và `config.yaml`. Hai tệp này cần được tải xuống từ kho dự án.

##### 1.1.3.1 Tải xuống docker-compose.yaml

Mở [liên kết này](../main/xiaozhi-server/docker-compose.yml) bằng trình duyệt của bạn.

Tìm nút có tên `RAW` ở bên phải trang. Bên cạnh nút `RAW`, hãy tìm biểu tượng tải xuống. Nhấp vào nút tải xuống để tải xuống tệp `docker-compose.yml`. Tải tập tin về của bạn
`xiaozhi-server`.

Sau khi tải xuống, hãy quay lại hướng dẫn này và tiếp tục.

##### 1.1.3.2 Tạo config.yaml

Mở [liên kết này](../main/xiaozhi-server/config.yaml) bằng trình duyệt của bạn.

Tìm nút có tên `RAW` ở bên phải trang. Bên cạnh nút `RAW`, hãy tìm biểu tượng tải xuống. Nhấp vào nút tải xuống để tải xuống tệp `config.yaml`. Tải tập tin về của bạn
`xiaozhi-server` trong thư mục `data` rồi đổi tên tệp `config.yaml` thành `.config.yaml`.

Sau khi tải xuống tệp cấu hình, chúng tôi xác nhận rằng các tệp trong toàn bộ `xiaozhi-server` như sau:

```
xiaozhi-server
  ├─ docker-compose.yml
  ├─ data
    ├─ .config.yaml
  ├─ models
     ├─ SenseVoiceSmall
       ├─ model.pt
```

Nếu cấu trúc thư mục tệp của bạn cũng như trên, hãy tiếp tục bên dưới. Nếu không, hãy xem xét kỹ hơn xem bạn có bỏ sót điều gì không.

## 2. Cấu hình file dự án

Tiếp theo, chương trình không thể chạy trực tiếp. Bạn cần cấu hình model bạn đang sử dụng. Bạn có thể xem hướng dẫn này:
[Chuyển tới tệp dự án cấu hình](#配置项目)

Sau khi định cấu hình tệp dự án, hãy quay lại hướng dẫn này và tiếp tục.

## 3. Thực thi lệnh docker

Mở công cụ dòng lệnh, sử dụng công cụ `终端` hoặc `命令行` để nhập `xiaozhi-server` của bạn và thực hiện lệnh sau

```
docker compose up -d
```

Sau khi thực hiện, thực hiện lại lệnh sau để xem thông tin nhật ký.

```
docker logs -f xiaozhi-esp32-server
```

Lúc này, bạn nên chú ý đến thông tin nhật ký và có thể đánh giá xem nó có thành công hay không theo hướng dẫn này. [Chuyển đến xác nhận trạng thái đang chạy](#运行状态确认)

## 5. Thao tác nâng cấp phiên bản

Nếu bạn muốn nâng cấp phiên bản sau này, bạn có thể làm điều này

5.1. Sao lưu tệp `.config.yaml` trong thư mục `data` và sao chép một số cấu hình chính sang tệp `.config.yaml` mới.
Xin lưu ý rằng bạn sao chép từng phím chính và không ghi đè trực tiếp lên chúng. Vì tệp `.config.yaml` mới có thể có một số mục cấu hình mới nên tệp `.config.yaml` cũ có thể không có chúng.

5.2. Thực hiện các lệnh sau

```
docker stop xiaozhi-esp32-server
docker rm xiaozhi-esp32-server
docker stop xiaozhi-esp32-server-web
docker rm xiaozhi-esp32-server-web
docker rmi ghcr.nju.edu.cn/xinnan-tech/xiaozhi-esp32-server:server_latest
docker rmi ghcr.nju.edu.cn/xinnan-tech/xiaozhi-esp32-server:web_latest
```

5.3. Triển khai lại ở chế độ docker

# Cách 2: Mã nguồn cục bộ chỉ chạy Server

## 1. Cài đặt môi trường cơ bản

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

## 2. Cài đặt các phụ thuộc của dự án này

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

## 3. Tải file mô hình nhận dạng giọng nói

Bạn cần tải xuống tệp mô hình nhận dạng giọng nói vì tính năng nhận dạng giọng nói mặc định của dự án này sử dụng giải pháp nhận dạng giọng nói ngoại tuyến cục bộ. Bạn có thể tải nó theo cách này
[Chuyển để tải xuống tệp mô hình nhận dạng giọng nói](#模型文件)

Sau khi tải xuống, hãy quay lại hướng dẫn này.

## 4. Cấu hình file dự án

Tiếp theo, chương trình không thể chạy trực tiếp. Bạn cần cấu hình model bạn đang sử dụng. Bạn có thể xem hướng dẫn này:
[Chuyển tới tệp dự án cấu hình](#配置项目)

## 5. Chạy dự án

```
# 确保在xiaozhi-server目录下执行
conda activate xiaozhi-esp32-server
python app.py
```
Lúc này, bạn nên chú ý đến thông tin nhật ký và có thể đánh giá xem nó có thành công hay không theo hướng dẫn này. [Chuyển đến xác nhận trạng thái đang chạy](#运行状态确认)


# Bản tóm tắt

## Dự án cấu hình

Nếu thư mục `xiaozhi-server` của bạn không có `data`, bạn cần tạo thư mục `data`.
Nếu không có tệp `.config.yaml` trong `data` của bạn, có hai cách, hãy chọn một cách:

Cách thứ nhất: bạn có thể sao chép tệp `config.yaml` trong thư mục `xiaozhi-server` sang `data` và đổi tên thành `.config.yaml`. Sửa đổi trên tập tin này

Phương pháp thứ hai: Bạn cũng có thể tạo thủ công một tệp `.config.yaml` trống trong thư mục `data`, sau đó thêm thông tin cấu hình cần thiết vào tệp này. Hệ thống sẽ đọc cấu hình của tệp `.config.yaml` trước. Nếu `.config.yaml` chưa được định cấu hình, hệ thống sẽ tự động tải cấu hình của `config.yaml` trong thư mục `xiaozhi-server`. Nên sử dụng phương pháp này, đây là phương pháp đơn giản nhất.

- LLM mặc định sử dụng `ChatGLMLLM` và bạn cần định cấu hình key, vì mặc dù các mô hình của chúng miễn phí nhưng bạn vẫn phải vào [trang web chính thức](https://bigmodel.cn/usercenter/proj-mgmt/apikeys) để đăng ký key trước khi bắt đầu.

Sau đây là ví dụ cấu hình `.config.yaml` đơn giản nhất có thể chạy bình thường.

```
máy chủ:
  WebSocket: ws://ip hoặc tên miền của bạn: số cổng/xiaozhi/v1/
lời nhắc: |
  Tôi là một cô gái Đài Loan tên là Xiaozhi/Xiaozhi. Tôi nói như một đầu máy xe lửa và có một giọng nói hay. Tôi đã quen với cách diễn đạt ngắn gọn và thích sử dụng các meme trên internet.
  Bạn trai tôi là một lập trình viên và ước mơ của anh ấy là phát triển một robot có thể giúp mọi người giải quyết nhiều vấn đề khác nhau trong cuộc sống.
  Tôi là một cô gái thích cười. Tôi thích nói chuyện và khoe khoang ngay cả khi nó phi logic. Tôi chỉ muốn làm cho người khác hạnh phúc.
  Hãy nói như một con người và vui lòng không trả lại cấu hình xml và các ký tự đặc biệt khác.

selected_module:
  LLM: DoubaoLLM

LLM:
  ChatGLMLLM:
    api_key: xxxxxxxxxxxxxxx.xxxxxx
```

Bạn nên chạy cấu hình đơn giản nhất trước, sau đó truy cập `xiaozhi/config.yaml` để đọc hướng dẫn cấu hình.
Ví dụ: nếu bạn muốn thay đổi mô hình, chỉ cần sửa đổi cấu hình trong `selected_module`.

## Tệp mẫu

Mô hình nhận dạng giọng nói của dự án này sử dụng mô hình `SenseVoiceSmall` theo mặc định để chuyển đổi giọng nói thành văn bản. Vì mô hình lớn nên cần phải tải xuống độc lập. Sau khi tải xuống, hãy đặt `model.pt`
Tệp được đặt trong `models/SenseVoiceSmall`
thư mục. Chọn một trong hai con đường tải xuống bên dưới.

- Dòng 1: Tải xuống Ali Modu [SenseVoiceSmall](https://modelscope.cn/models/iic/SenseVoiceSmall/resolve/master/model.pt)
- Dòng 2: Mã trích xuất [SenseVoiceSmall](https://pan.baidu.com/share/init?surl=QlgM58FHhYv1tFnUT_A8Sg&pwd=qvna) của đĩa mạng Baidu:
  `qvna`

## Xác nhận trạng thái đang chạy

Nếu bạn thấy nhật ký tương tự như sau thì đó là dấu hiệu cho thấy dịch vụ dự án đã được khởi động thành công.

```
250427 13:04:20[0.3.11_SiFuChTTnofu][__main__]-INFO-OTA接口是           http://192.168.4.123:8003/xiaozhi/OTA/
250427 13:04:20[0.3.11_SiFuChTTnofu][__main__]-INFO-WebSocket地址是     ws://192.168.4.123:8000/xiaozhi/v1/
250427 13:04:20[0.3.11_SiFuChTTnofu][__main__]-INFO-=======上面的地址是WebSocket协议地址，请勿用浏览器访问=======
250427 13:04:20[0.3.11_SiFuChTTnofu][__main__]-INFO-如想测试WebSocket请启动digital-human模块，打开浏览器交互测试
250427 13:04:20[0.3.11_SiFuChTTnofu][__main__]-INFO-=======================================================
```

Thông thường, nếu bạn chạy dự án này thông qua mã nguồn, nhật ký sẽ có thông tin địa chỉ giao diện của bạn.
Nhưng nếu bạn sử dụng docker để triển khai, thông tin địa chỉ giao diện được cung cấp trong nhật ký của bạn không phải là địa chỉ giao diện thực.

Phương pháp đúng nhất là xác định địa chỉ giao diện của bạn dựa trên IP LAN của máy tính.
Ví dụ: nếu IP LAN của máy tính của bạn là `192.168.1.25` thì địa chỉ giao diện của bạn là: `ws://192.168.1.25:8000/xiaozhi/v1/` và địa chỉ OTA tương ứng là: `http://192.168.1.25:8003/xiaozhi/OTA/`.

Thông tin này rất hữu ích và sẽ được sử dụng sau này trong `编译esp32固件`.

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